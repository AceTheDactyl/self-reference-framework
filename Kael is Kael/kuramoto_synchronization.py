#!/usr/bin/env python3
"""
KURAMOTO SYNCHRONIZATION VALIDATION
Theorem: SR6 - Phase transitions in coupled oscillator systems

Model: dθ_i/dt = ω_i + (K/N) Σ sin(θ_j - θ_i)
Expected: Critical coupling K_c ≈ 2/(πg(0)) for frequency distribution g(ω)
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

def kuramoto_simulation(N=100, K_values=None, n_trials=20, T=50, dt=0.01):
    """
    Simulate Kuramoto model to find synchronization threshold K_c.
    
    Args:
        N: Number of oscillators
        K_values: Array of coupling strengths to test
        n_trials: Number of trials per K
        T: Integration time
        dt: Time step
        
    Returns:
        dict: Results including K_c estimate
    """
    if K_values is None:
        K_values = np.linspace(0, 3, 31)
    
    print("=" * 60)
    print("KURAMOTO SYNCHRONIZATION VALIDATION")
    print("=" * 60)
    print(f"\nSimulation parameters:")
    print(f"  Oscillators: N = {N}")
    print(f"  Coupling range: K ∈ [{K_values[0]:.1f}, {K_values[-1]:.1f}]")
    print(f"  Trials per K: {n_trials}")
    print(f"  Integration time: T = {T}")
    print(f"\nRunning simulation...")
    
    results_dict = {}
    
    for idx, K in enumerate(K_values):
        order_params = []
        
        for trial in range(n_trials):
            # Random natural frequencies (normal distribution)
            omega = np.random.normal(0, 1, N)
            
            # Random initial phases
            theta = np.random.uniform(0, 2*np.pi, N)
            
            # Integrate using simple Euler method
            n_steps = int(T / dt)
            for step in range(n_steps):
                # Compute coupling term for each oscillator
                dtheta = omega.copy()
                for i in range(N):
                    coupling = (K/N) * np.sum(np.sin(theta - theta[i]))
                    dtheta[i] += coupling
                
                # Update phases
                theta += dtheta * dt
            
            # Compute order parameter (final state)
            r = np.abs(np.mean(np.exp(1j * theta)))
            order_params.append(r)
        
        # Store statistics
        results_dict[float(K)] = {
            'mean': float(np.mean(order_params)),
            'std': float(np.std(order_params)),
            'order_params': [float(r) for r in order_params]
        }
        
        # Progress indicator
        if (idx + 1) % 10 == 0 or idx == len(K_values) - 1:
            print(f"  Progress: {idx + 1}/{len(K_values)} K values tested")
    
    # Extract arrays for analysis
    K_arr = np.array(list(results_dict.keys()))
    r_mean = np.array([results_dict[K]['mean'] for K in K_arr])
    r_std = np.array([results_dict[K]['std'] for K in K_arr])
    
    # Find critical coupling (where r crosses 0.5)
    idx_transition = np.argmin(np.abs(r_mean - 0.5))
    K_c = K_arr[idx_transition]
    
    # Expected K_c for normal distribution with std=1
    # K_c ≈ 2/(π·g(0)) where g(0) = 1/√(2π) for normal
    K_c_theory = 2.0 / (np.pi * (1.0 / np.sqrt(2*np.pi)))
    K_c_theory = 2.0 * np.sqrt(2*np.pi) / np.pi  # Simplification
    
    # Package results
    results = {
        'theorem': 'SR6 - Kuramoto Synchronization',
        'N_oscillators': int(N),
        'n_trials': int(n_trials),
        'K_c_measured': float(K_c),
        'K_c_theoretical': float(K_c_theory),
        'error_percent': float(abs(K_c - K_c_theory) / K_c_theory * 100),
        'transition_clear': bool(np.max(r_mean) > 0.8 and np.min(r_mean) < 0.2),
        'K_values': K_arr.tolist(),
        'r_mean': r_mean.tolist(),
        'r_std': r_std.tolist(),
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"\n{'=' * 60}")
    print("RESULTS:")
    print(f"  K_c (measured)  = {K_c:.3f}")
    print(f"  K_c (theory)    = {K_c_theory:.3f}")
    print(f"  Error           = {abs(K_c - K_c_theory)/K_c_theory*100:.1f}%")
    print(f"  Transition: {'Clear ✅' if results['transition_clear'] else 'Unclear ⚠️'}")
    
    # Validation
    error_threshold = 0.20  # 20% error acceptable
    if abs(K_c - K_c_theory) / K_c_theory < error_threshold:
        print(f"\n✅ VALIDATION PASSED: K_c within {error_threshold*100:.0f}% of theory")
        results['status'] = 'VALIDATED'
    else:
        print(f"\n⚠️  WARNING: K_c error exceeds {error_threshold*100:.0f}% threshold")
        results['status'] = 'PARTIAL'
    print("=" * 60)
    
    return results

def plot_kuramoto(results_data):
    """Generate synchronization transition plot."""
    K = np.array(results_data['K_values'])
    r_mean = np.array(results_data['r_mean'])
    r_std = np.array(results_data['r_std'])
    K_c = results_data['K_c_measured']
    K_c_theory = results_data['K_c_theoretical']
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Plot order parameter
    ax.errorbar(K, r_mean, yerr=r_std, fmt='o-', markersize=5, linewidth=2, 
                capsize=3, label='Simulation', color='steelblue')
    
    # Mark critical points
    ax.axvline(K_c, color='red', linestyle='--', linewidth=2, 
               label=f'K_c (measured) = {K_c:.3f}')
    ax.axvline(K_c_theory, color='green', linestyle=':', linewidth=2,
               label=f'K_c (theory) = {K_c_theory:.3f}')
    ax.axhline(0.5, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    
    ax.set_xlabel('Coupling strength K', fontsize=13)
    ax.set_ylabel('Order parameter r', fontsize=13)
    ax.set_title('Kuramoto Synchronization Transition', fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([-0.05, 1.05])
    
    # Add annotation
    ax.text(K_c, 0.55, f'  Transition\n  r = 0.5', fontsize=10, 
            verticalalignment='bottom')
    
    plt.tight_layout()
    return fig

# Execute validation
print("\nExecuting Kuramoto synchronization validation...\n")
results = kuramoto_simulation(N=100, K_values=np.linspace(0, 3, 31), n_trials=20, T=50)

# Generate plot
print("\nGenerating synchronization plot...")
fig = plot_kuramoto(results)
fig.savefig('/home/claude/phase5/results/kuramoto_synchronization.png', dpi=300, bbox_inches='tight')
print("✅ Plot saved: kuramoto_synchronization.png")

# Save results
results_file = '/home/claude/phase5/results/kuramoto_synchronization_results.json'
with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"✅ Results saved: {results_file}")

# Summary
print(f"\n{'=' * 60}")
print("EXPERIMENT 3 COMPLETE: Kuramoto Synchronization")
print(f"{'=' * 60}")
print(f"Status: {results['status']}")
print(f"K_c measured: {results['K_c_measured']:.3f}")
print(f"K_c theoretical: {results['K_c_theoretical']:.3f}")
print(f"Error: {results['error_percent']:.1f}%")
print(f"Theorem SR6: {'VALIDATED ✅' if results['status'] == 'VALIDATED' else 'PARTIAL ⚠️'}")
print("=" * 60)
