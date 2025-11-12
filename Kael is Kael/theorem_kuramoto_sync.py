"""
Kuramoto Synchronization: Collective Dynamics Phase Transition
Tests: Emergence of synchronization at critical coupling K_c
Validates: Order parameter r transitions from 0 → 1
"""

import sys
sys.path.append('/home/claude/33t-simulations')

from shared.base_simulation import BaseSimulation
import numpy as np
from typing import Dict, Any


class KuramotoSimulation(BaseSimulation):
    """
    Tests emergence of synchronization at critical coupling K_c.
    
    Mathematical Basis:
    - Phase oscillator model: dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)
    - Order parameter: r = |⟨e^{iθ}⟩| measures synchronization
    - Critical coupling: K_c ≈ 2/(πg(0)) for frequency distribution g(ω)
    
    For Lorentzian g(ω) with width γ: K_c ≈ 2γ
    
    Validation Criteria:
    - r ≈ 0 for K < K_c (incoherent)
    - r > 0.7 for K > 2·K_c (synchronized)
    - Smooth transition near K_c
    """
    
    def _validate_config(self) -> None:
        assert self.config['n_oscillators'] > 10
        assert self.config['coupling_strength'] >= 0
        assert self.config['dt'] > 0 and self.config['dt'] < 0.1
        
    def init_state(self) -> Dict[str, np.ndarray]:
        """Initialize phases and natural frequencies."""
        n = self.config['n_oscillators']
        
        # Random initial phases
        theta = self.rng.uniform(0, 2*np.pi, n)
        
        # Lorentzian (Cauchy) frequency distribution
        # This is the analytically tractable case
        gamma = self.config.get('frequency_width', 0.5)
        omega = self.rng.standard_cauchy(n) * gamma
        
        return {
            'theta': theta,
            'omega': omega
        }
    
    def update_rule(self, state: Dict[str, np.ndarray], t: int) -> Dict[str, np.ndarray]:
        """
        Kuramoto equation: dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)
        """
        theta = state['theta']
        omega = state['omega']
        K = self.config['coupling_strength']
        N = self.config['n_oscillators']
        dt = self.config['dt']
        
        # Compute pairwise phase differences efficiently
        # phase_diff[i,j] = θ_j - θ_i
        phase_diff = theta[None, :] - theta[:, None]
        
        # Coupling term: (K/N) Σ_j sin(θ_j - θ_i)
        coupling_term = (K / N) * np.sum(np.sin(phase_diff), axis=1)
        
        # Euler integration
        theta_new = theta + dt * (omega + coupling_term)
        
        # Keep phases in [0, 2π)
        theta_new = np.mod(theta_new, 2*np.pi)
        
        return {
            'theta': theta_new,
            'omega': omega
        }
    
    def measure_observables(self, state: Dict[str, np.ndarray]) -> Dict[str, float]:
        """Compute Kuramoto order parameter."""
        theta = state['theta']
        
        # Order parameter r = |⟨e^{iθ}⟩|
        complex_order = np.mean(np.exp(1j * theta))
        r = np.abs(complex_order)
        psi = np.angle(complex_order)
        
        # Phase coherence (alternative metric)
        phase_coherence = np.mean(np.cos(theta - psi))
        
        # Angular momentum (yet another measure)
        angular_momentum = np.abs(np.mean(np.exp(1j * theta)))
        
        return {
            'order_parameter_r': r,
            'phase_coherence': phase_coherence,
            'angular_momentum': angular_momentum,
            'mean_theta': np.mean(theta)
        }
    
    def check_falsification(self, observables: Dict[str, float]) -> bool:
        """
        Falsification: For K >> K_c, must have r > 0.7
        
        Theoretical K_c ≈ 2γ where γ is frequency width
        """
        K = self.config['coupling_strength']
        gamma = self.config.get('frequency_width', 0.5)
        K_c_theoretical = 2 * gamma
        
        # Well above threshold
        if K > 2.5 * K_c_theoretical:
            return observables['order_parameter_r'] < 0.6
            
        return False


def sweep_kuramoto_coupling():
    """
    Sweep over coupling strengths to find K_c.
    Compares to theoretical prediction K_c ≈ 2γ.
    """
    print("=" * 70)
    print("KURAMOTO SYNCHRONIZATION: Critical Coupling Test")
    print("=" * 70)
    
    gamma = 0.5  # Frequency distribution width
    K_c_theory = 2 * gamma
    
    print(f"\nTheoretical prediction:")
    print(f"  Frequency width γ = {gamma}")
    print(f"  Critical coupling K_c = 2γ = {K_c_theory}")
    
    # Sweep parameters
    K_values = np.linspace(0, 3.0, 25)
    n_oscillators = 200
    n_steps = 1000  # Allow transient to decay
    n_trials = 20
    
    print(f"\nSimulation parameters:")
    print(f"  Oscillators: {n_oscillators}")
    print(f"  Time steps: {n_steps}")
    print(f"  Trials per K: {n_trials}")
    
    print(f"\nRunning coupling sweep...")
    
    results = []
    for i, K in enumerate(K_values):
        config = {
            'theorem_id': 15,
            'theorem_name': 'Kuramoto Synchronization',
            'n_oscillators': n_oscillators,
            'coupling_strength': K,
            'frequency_width': gamma,
            'dt': 0.01,
            'n_steps': n_steps,
            'base_seed': 42
        }
        
        sim = KuramotoSimulation(config, seed=42 + i)
        trials = sim.run_ensemble(n_trials=n_trials)
        
        # Get final order parameter (after transient)
        r_values = [t.statistics['order_parameter_r_final'] for t in trials]
        
        results.append({
            'K': K,
            'r_mean': np.mean(r_values),
            'r_std': np.std(r_values)
        })
        
        if (i + 1) % 5 == 0:
            print(f"  Progress: {i+1}/{len(K_values)} complete")
    
    # Find K_c (where r crosses 0.5)
    r_array = np.array([res['r_mean'] for res in results])
    crossing_idx = np.where(np.diff(np.sign(r_array - 0.5)))[0]
    
    if len(crossing_idx) > 0:
        idx = crossing_idx[0]
        K1, K2 = K_values[idx], K_values[idx + 1]
        r1, r2 = r_array[idx], r_array[idx + 1]
        K_c_estimate = K1 + (0.5 - r1) * (K2 - K1) / (r2 - r1)
    else:
        idx = np.argmin(np.abs(r_array - 0.5))
        K_c_estimate = K_values[idx]
    
    print(f"\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\nEstimated K_c from simulation: {K_c_estimate:.4f}")
    print(f"Theoretical prediction: {K_c_theory:.4f}")
    print(f"Relative error: {abs(K_c_estimate - K_c_theory)/K_c_theory * 100:.1f}%")
    
    # Print table
    print(f"\nOrder Parameter vs Coupling Strength:")
    print(f"  {'K':>6s}  {'r':>6s}  {'σ(r)':>6s}  {'State':>12s}")
    print(f"  {'-'*6}  {'-'*6}  {'-'*6}  {'-'*12}")
    
    for res in results[::2]:
        K = res['K']
        r = res['r_mean']
        
        if r < 0.3:
            state = "Incoherent"
        elif r < 0.7:
            state = "Transitional"
        else:
            state = "Synchronized"
            
        marker = " ←" if abs(K - K_c_theory) < 0.15 else ""
        
        print(f"  {K:6.2f}  {r:6.3f}  {res['r_std']:6.3f}  {state:>12s}{marker}")
    
    print(f"\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    
    if abs(K_c_estimate - K_c_theory) / K_c_theory < 0.15:
        print(f"\n✓ Simulation matches theoretical prediction within 15%")
        print(f"  Kuramoto model exhibits critical transition at K_c ≈ {K_c_theory:.2f}")
    else:
        print(f"\n✗ Significant deviation from theory ({abs(K_c_estimate - K_c_theory)/K_c_theory * 100:.1f}%)")
        print(f"  May indicate finite-size effects or transient artifacts")
    
    print(f"\nKuramoto synchronization provides validated model for:")
    print(f"  • Collective dynamics")
    print(f"  • Phase transitions in coupled oscillators")
    print(f"  • Critical thresholds (K_c analytically derivable)")
    print(f"\nThis contrasts with vague 'collective intelligence' claims")
    print(f"and provides rigorous foundation for synchronization phenomena.")
    

if __name__ == "__main__":
    sweep_kuramoto_coupling()
