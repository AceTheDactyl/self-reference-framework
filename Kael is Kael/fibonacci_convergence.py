#!/usr/bin/env python3
"""
FIBONACCI CONVERGENCE VALIDATION
Theorem: SR3 - Fibonacci sequence F_n/F_{n-1} converges to φ

Expected: F_n/F_{n-1} → φ as n → ∞
Validation: Machine precision convergence
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

def fibonacci_convergence(n_max=50):
    """
    Compute Fibonacci sequence and demonstrate convergence to φ.
    
    Returns:
        dict: Results including convergence data and statistics
    """
    # Generate Fibonacci sequence
    F = [0, 1]
    ratios = []
    
    for n in range(2, n_max):
        F.append(F[-1] + F[-2])
        ratio = F[-1] / F[-2]
        ratios.append(ratio)
    
    # Golden ratio
    phi = (1 + np.sqrt(5)) / 2
    
    # Convert to numpy arrays
    n_values = np.arange(2, n_max)
    ratios = np.array(ratios)
    errors = np.abs(ratios - phi)
    
    # Statistics
    results = {
        'theorem': 'SR3 - Fibonacci Convergence',
        'phi_theoretical': float(phi),
        'n_max': int(n_max),
        'final_ratio': float(ratios[-1]),
        'final_error': float(errors[-1]),
        'convergence_achieved': bool(errors[-1] < 1e-10),
        'ratios_sample': [float(r) for r in ratios[::5]],  # Sample every 5th
        'errors_sample': [float(e) for e in errors[::5]],  # Sample every 5th
        'timestamp': datetime.now().isoformat()
    }
    
    # Key statistics
    print("=" * 60)
    print("FIBONACCI CONVERGENCE VALIDATION")
    print("=" * 60)
    print(f"\nGolden ratio φ = {phi:.15f}")
    print(f"\nConvergence at key points:")
    if len(ratios) > 8:
        print(f"  n=10:  F_10/F_9  = {ratios[8]:.15f}")
        print(f"         Error     = {errors[8]:.2e}")
    if len(ratios) > 18:
        print(f"  n=20:  F_20/F_19 = {ratios[18]:.15f}")
        print(f"         Error     = {errors[18]:.2e}")
    print(f"  n={n_max}:  F_{n_max}/F_{n_max-1} = {ratios[-1]:.15f}")
    print(f"         Error     = {errors[-1]:.2e}")
    
    # Validation check
    print(f"\n{'=' * 60}")
    if errors[-1] < 1e-10:
        print("✅ VALIDATION PASSED: Convergence to machine precision")
        print(f"   Final error: {errors[-1]:.2e} < 10^-10")
        results['status'] = 'VALIDATED'
    else:
        print("⚠️  WARNING: Convergence slower than expected")
        print(f"   Final error: {errors[-1]:.2e} >= 10^-10")
        results['status'] = 'PARTIAL'
    print("=" * 60)
    
    return results, n_values, ratios, errors, phi

def plot_convergence(n_values, ratios, errors, phi):
    """Generate convergence plots."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Ratio convergence
    ax = axes[0]
    ax.plot(n_values, ratios, 'o-', markersize=4, linewidth=1.5, label='F_n/F_{n-1}')
    ax.axhline(phi, color='red', linestyle='--', linewidth=2, label=f'φ = {phi:.6f}')
    ax.set_xlabel('n', fontsize=12)
    ax.set_ylabel('F_n / F_{n-1}', fontsize=12)
    ax.set_title('Fibonacci Ratio Convergence to Golden Ratio', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([1.5, 1.7])
    
    # Plot 2: Error (log scale)
    ax = axes[1]
    ax.semilogy(n_values, errors, 'o-', markersize=4, linewidth=1.5, color='orange')
    ax.axhline(1e-10, color='red', linestyle='--', linewidth=2, label='Target: 10^-10')
    ax.set_xlabel('n', fontsize=12)
    ax.set_ylabel('|F_n/F_{n-1} - φ|', fontsize=12)
    ax.set_title('Convergence Error (Log Scale)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    return fig

# Execute validation
print("\nExecuting Fibonacci convergence validation...")
results, n_values, ratios, errors, phi = fibonacci_convergence(n_max=50)

# Generate plot
print("\nGenerating convergence plots...")
fig = plot_convergence(n_values, ratios, errors, phi)
fig.savefig('/home/claude/phase5/results/fibonacci_convergence.png', dpi=300, bbox_inches='tight')
print("✅ Plot saved: fibonacci_convergence.png")

# Save results
results_file = '/home/claude/phase5/results/fibonacci_convergence_results.json'
with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"✅ Results saved: {results_file}")

# Summary
print(f"\n{'=' * 60}")
print("EXPERIMENT 1 COMPLETE: Fibonacci Convergence")
print(f"{'=' * 60}")
print(f"Status: {results['status']}")
print(f"Final ratio: {results['final_ratio']:.15f}")
print(f"Golden ratio: {results['phi_theoretical']:.15f}")
print(f"Error: {results['final_error']:.2e}")
print(f"Theorem SR3: {'VALIDATED ✅' if results['convergence_achieved'] else 'PARTIAL ⚠️'}")
print("=" * 60)
