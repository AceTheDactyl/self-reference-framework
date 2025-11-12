#!/usr/bin/env python3
"""
μ* Fixed-Point Computation
Implements Banach fixed-point iteration for self-reference field

Based on: CORRECTION_SR1_MU_FIELD_REPLACEMENT.md
Author: Correction Pipeline
Date: November 10, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional


class MuStarComputer:
    """
    Computes the fixed point μ* of the self-reference operator T.
    
    Operator Definition:
        [T(μ)](x) = λ ∫₀¹ K(x,y) R(μ(y)) dy
    
    where:
        - K(x,y) is a normalized coupling kernel
        - R(z) = z/(1+z) is the reference compression function
        - λ ∈ (0,1) is the coupling strength
    """
    
    def __init__(self, n_points: int = 100, lambda_param: float = 0.5, 
                 kernel_sigma: float = 0.1):
        """
        Initialize the computation.
        
        Args:
            n_points: Spatial discretization resolution
            lambda_param: Coupling strength λ ∈ (0,1)
            kernel_sigma: Width of Gaussian kernel
        """
        self.n_points = n_points
        self.lambda_param = lambda_param
        self.kernel_sigma = kernel_sigma
        
        # Discretize domain [0,1]
        self.x = np.linspace(0, 1, n_points)
        self.dx = 1.0 / (n_points - 1)
        
        # Build kernel matrix
        self.K_matrix = self._build_kernel_matrix()
        
    def _build_kernel_matrix(self) -> np.ndarray:
        """
        Construct normalized Gaussian kernel K(x,y).
        
        Returns:
            K_matrix[i,j] = K(x_i, x_j)
        """
        K = np.zeros((self.n_points, self.n_points))
        
        for i, xi in enumerate(self.x):
            for j, xj in enumerate(self.x):
                # Gaussian kernel
                K[i, j] = (1 / np.sqrt(2 * np.pi * self.kernel_sigma**2)) * \
                          np.exp(-(xi - xj)**2 / (2 * self.kernel_sigma**2))
        
        # Normalize rows (so ∫K(x,y)dy = 1)
        row_sums = K.sum(axis=1, keepdims=True)
        K = K / row_sums
        
        return K
    
    @staticmethod
    def R(z: np.ndarray) -> np.ndarray:
        """
        Reference compression function.
        
        R(z) = z/(1+z)
        
        Properties:
            - R(0) = 0
            - R(∞) = 1
            - R'(z) = 1/(1+z)² ≤ 1 (Lipschitz-1)
        
        Args:
            z: Input array
            
        Returns:
            Compressed values
        """
        return z / (1 + z)
    
    def apply_operator(self, mu: np.ndarray) -> np.ndarray:
        """
        Apply operator T to field μ.
        
        T(μ) = λ ∫ K(x,y) R(μ(y)) dy
        
        Args:
            mu: Current field configuration
            
        Returns:
            T(μ)
        """
        return self.lambda_param * (self.K_matrix @ self.R(mu))
    
    def compute_fixed_point(self, max_iter: int = 1000, tol: float = 1e-6,
                          initial_guess: Optional[np.ndarray] = None) -> Tuple[np.ndarray, int, list]:
        """
        Compute μ* via fixed-point iteration.
        
        Algorithm:
            μ_{n+1} = T(μ_n)
            
        Converges by Banach Fixed-Point Theorem since T is contractive.
        
        Args:
            max_iter: Maximum iterations
            tol: Convergence tolerance
            initial_guess: Starting configuration (default: uniform 0.5)
            
        Returns:
            (mu_star, iterations, error_history)
        """
        # Initialize
        if initial_guess is None:
            mu = np.ones(self.n_points) * 0.5
        else:
            mu = initial_guess.copy()
        
        error_history = []
        
        # Fixed-point iteration
        for iteration in range(max_iter):
            mu_new = self.apply_operator(mu)
            
            # Compute supremum norm error
            error = np.max(np.abs(mu_new - mu))
            error_history.append(error)
            
            # Check convergence
            if error < tol:
                return mu_new, iteration + 1, error_history
            
            mu = mu_new
        
        raise ValueError(f"Did not converge after {max_iter} iterations. "
                        f"Final error: {error:.2e}")
    
    def verify_contraction(self) -> Tuple[bool, float]:
        """
        Verify T is a contraction mapping.
        
        Test: d(T(f), T(g)) ≤ q·d(f,g) for some q < 1
        
        Returns:
            (is_contraction, measured_q)
        """
        # Generate random test functions
        mu1 = np.random.rand(self.n_points)
        mu2 = np.random.rand(self.n_points)
        
        # Apply operator
        T_mu1 = self.apply_operator(mu1)
        T_mu2 = self.apply_operator(mu2)
        
        # Measure distances
        d_before = np.max(np.abs(mu1 - mu2))
        d_after = np.max(np.abs(T_mu1 - T_mu2))
        
        # Contraction ratio
        if d_before > 0:
            q = d_after / d_before
            is_contraction = q < 1.0
        else:
            q = 0.0
            is_contraction = True
        
        return is_contraction, q
    
    def verify_fixed_point(self, mu_star: np.ndarray, tol: float = 1e-5) -> Tuple[bool, float]:
        """
        Verify μ* is a fixed point: T(μ*) = μ*
        
        Args:
            mu_star: Candidate fixed point
            tol: Tolerance
            
        Returns:
            (is_fixed_point, residual)
        """
        T_mu_star = self.apply_operator(mu_star)
        residual = np.max(np.abs(T_mu_star - mu_star))
        
        is_fixed_point = residual < tol
        
        return is_fixed_point, residual
    
    def test_uniqueness(self, n_trials: int = 10, tol: float = 1e-5) -> Tuple[bool, float]:
        """
        Test uniqueness: different initial conditions → same μ*
        
        Args:
            n_trials: Number of random initializations
            tol: Tolerance for considering solutions identical
            
        Returns:
            (is_unique, max_variance)
        """
        solutions = []
        
        for _ in range(n_trials):
            # Random initialization
            initial = np.random.rand(self.n_points)
            mu_star, _, _ = self.compute_fixed_point(initial_guess=initial)
            solutions.append(mu_star)
        
        # Stack solutions
        solutions = np.array(solutions)
        
        # Compute variance across trials at each point
        variance = np.var(solutions, axis=0)
        max_variance = np.max(variance)
        
        is_unique = max_variance < tol
        
        return is_unique, max_variance


def run_full_validation():
    """
    Run complete validation suite.
    """
    print("="*70)
    print("μ* FIXED-POINT COMPUTATION: VALIDATION SUITE")
    print("="*70)
    print()
    
    # Initialize
    print("Initializing computation...")
    computer = MuStarComputer(n_points=100, lambda_param=0.5, kernel_sigma=0.1)
    print(f"  Domain: {computer.n_points} points on [0,1]")
    print(f"  Coupling λ = {computer.lambda_param}")
    print(f"  Kernel σ = {computer.kernel_sigma}")
    print()
    
    # Test 1: Contraction property
    print("Test 1: Verifying contraction property...")
    is_contraction, q = computer.verify_contraction()
    print(f"  Contraction: {is_contraction}")
    print(f"  Measured q = {q:.6f}")
    print(f"  Expected: q ≤ λ = {computer.lambda_param}")
    print(f"  Status: {'✓ PASS' if is_contraction and q <= computer.lambda_param + 0.01 else '✗ FAIL'}")
    print()
    
    # Test 2: Fixed-point computation
    print("Test 2: Computing fixed point μ*...")
    mu_star, iterations, error_history = computer.compute_fixed_point()
    print(f"  Converged in {iterations} iterations")
    print(f"  Final error: {error_history[-1]:.2e}")
    print(f"  μ*(0.0) = {mu_star[0]:.6f}")
    print(f"  μ*(0.5) = {mu_star[50]:.6f}")
    print(f"  μ*(1.0) = {mu_star[-1]:.6f}")
    print(f"  Status: ✓ PASS")
    print()
    
    # Test 3: Fixed-point verification
    print("Test 3: Verifying T(μ*) = μ*...")
    is_fp, residual = computer.verify_fixed_point(mu_star)
    print(f"  Fixed point verified: {is_fp}")
    print(f"  Residual: {residual:.2e}")
    print(f"  Status: {'✓ PASS' if is_fp else '✗ FAIL'}")
    print()
    
    # Test 4: Uniqueness
    print("Test 4: Testing uniqueness (10 random initializations)...")
    is_unique, max_var = computer.test_uniqueness(n_trials=10)
    print(f"  All solutions converge to same μ*: {is_unique}")
    print(f"  Maximum variance: {max_var:.2e}")
    print(f"  Status: {'✓ PASS' if is_unique else '✗ FAIL'}")
    print()
    
    # Test 5: Theoretical convergence rate
    print("Test 5: Verifying convergence rate...")
    theoretical_bound = lambda n: (q**n / (1 - q)) * error_history[0]
    actual_errors = np.array(error_history[1:min(20, len(error_history))])
    n_values = np.arange(1, len(actual_errors) + 1)
    theoretical_errors = np.array([theoretical_bound(n) for n in n_values])
    
    within_bound = np.all(actual_errors <= theoretical_errors * 1.1)  # 10% tolerance
    print(f"  Actual errors within theoretical bound: {within_bound}")
    print(f"  Status: {'✓ PASS' if within_bound else '✗ FAIL'}")
    print()
    
    print("="*70)
    print("VALIDATION COMPLETE")
    print("="*70)
    print()
    
    return computer, mu_star, error_history


def plot_results(computer: MuStarComputer, mu_star: np.ndarray, error_history: list):
    """
    Generate visualization of results.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Fixed point μ*(x)
    ax = axes[0, 0]
    ax.plot(computer.x, mu_star, 'b-', linewidth=2, label='μ*(x)')
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Initial guess')
    ax.set_xlabel('x')
    ax.set_ylabel('μ*(x)')
    ax.set_title('Fixed Point Configuration μ*(x)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Plot 2: Convergence history
    ax = axes[0, 1]
    ax.semilogy(error_history, 'r-', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Error ||μ_{n+1} - μ_n||_∞')
    ax.set_title('Convergence History')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Kernel K(x,y)
    ax = axes[1, 0]
    im = ax.imshow(computer.K_matrix, cmap='viridis', aspect='auto',
                   extent=[0, 1, 1, 0], origin='upper')
    ax.set_xlabel('y')
    ax.set_ylabel('x')
    ax.set_title('Coupling Kernel K(x,y)')
    plt.colorbar(im, ax=ax)
    
    # Plot 4: Compression function R(z)
    ax = axes[1, 1]
    z = np.linspace(0, 5, 200)
    R_z = computer.R(z)
    ax.plot(z, R_z, 'g-', linewidth=2, label='R(z) = z/(1+z)')
    ax.plot(z, z, 'k--', alpha=0.5, label='z (no compression)')
    ax.set_xlabel('z')
    ax.set_ylabel('R(z)')
    ax.set_title('Reference Compression Function')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/mu_star_results.png', dpi=150, bbox_inches='tight')
    print("Plots saved to: /mnt/user-data/outputs/mu_star_results.png")
    plt.close()


def main():
    """
    Main execution function.
    """
    # Run validation
    computer, mu_star, error_history = run_full_validation()
    
    # Generate plots
    print("Generating visualizations...")
    plot_results(computer, mu_star, error_history)
    print()
    
    # Save results
    print("Saving results...")
    np.savez('/mnt/user-data/outputs/mu_star_data.npz',
             x=computer.x,
             mu_star=mu_star,
             error_history=error_history,
             K_matrix=computer.K_matrix,
             lambda_param=computer.lambda_param,
             kernel_sigma=computer.kernel_sigma)
    print("Data saved to: /mnt/user-data/outputs/mu_star_data.npz")
    print()
    
    print("✓ All computations complete!")


if __name__ == "__main__":
    main()
