#!/usr/bin/env python3
"""
Parameter Exploration for μ* Fixed Point
Tests different λ and σ values to find non-trivial solutions
"""

import numpy as np
import sys
sys.path.append('/home/claude')
from mu_star_computation import MuStarComputer

def explore_parameters():
    """Test different parameter combinations."""
    
    print("="*70)
    print("PARAMETER EXPLORATION: Finding Non-Trivial Fixed Points")
    print("="*70)
    print()
    
    # Test different coupling strengths
    lambda_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    sigma_values = [0.05, 0.1, 0.2, 0.3]
    
    results = []
    
    for lam in lambda_values:
        for sig in sigma_values:
            try:
                computer = MuStarComputer(n_points=100, lambda_param=lam, 
                                        kernel_sigma=sig)
                mu_star, iters, _ = computer.compute_fixed_point(max_iter=500)
                
                # Compute statistics
                mean_val = np.mean(mu_star)
                max_val = np.max(mu_star)
                min_val = np.min(mu_star)
                variance = np.var(mu_star)
                
                results.append({
                    'lambda': lam,
                    'sigma': sig,
                    'mean': mean_val,
                    'max': max_val,
                    'min': min_val,
                    'var': variance,
                    'iters': iters
                })
                
                print(f"λ={lam:.1f}, σ={sig:.2f}: "
                      f"μ̄={mean_val:.6f}, max={max_val:.6f}, "
                      f"var={variance:.2e}, iters={iters}")
                
            except Exception as e:
                print(f"λ={lam:.1f}, σ={sig:.2f}: FAILED ({str(e)[:30]})")
    
    print()
    print("="*70)
    
    # Find most interesting (non-trivial) solution
    non_trivial = [r for r in results if r['mean'] > 0.01]
    
    if non_trivial:
        best = max(non_trivial, key=lambda r: r['var'])
        print("Most interesting non-trivial solution:")
        print(f"  λ = {best['lambda']}")
        print(f"  σ = {best['sigma']}")
        print(f"  Mean μ* = {best['mean']:.6f}")
        print(f"  Variance = {best['var']:.2e}")
        print()
        
        # Recompute with visualization
        print("Recomputing for visualization...")
        computer = MuStarComputer(n_points=100, 
                                lambda_param=best['lambda'],
                                kernel_sigma=best['sigma'])
        mu_star, iters, error_history = computer.compute_fixed_point()
        
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(computer.x, mu_star, 'b-', linewidth=2)
        plt.xlabel('x', fontsize=12)
        plt.ylabel('μ*(x)', fontsize=12)
        plt.title(f'Non-Trivial Fixed Point (λ={best["lambda"]}, σ={best["sigma"]})', 
                  fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.savefig('/mnt/user-data/outputs/mu_star_nontrivial.png', 
                   dpi=150, bbox_inches='tight')
        print(f"  Saved to: mu_star_nontrivial.png")
        plt.close()
    else:
        print("WARNING: All solutions converged to trivial (near-zero) fixed point.")
        print("This may indicate:")
        print("  1. The compression function R(z)=z/(1+z) is too strong")
        print("  2. Need different operator formulation")
        print("  3. Physical interpretation: equilibrium at minimal self-reference")

if __name__ == "__main__":
    explore_parameters()
