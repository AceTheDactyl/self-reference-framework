#!/usr/bin/env python3
"""
Revised μ* Computation with Drive Term
Adds constant self-reference drive to prevent trivial solution

Modified operator:
    T(μ)(x) = λ[∫K(x,y)R(μ(y))dy + α]
    
where α > 0 is a "self-reference drive" parameter
"""

import numpy as np
import matplotlib.pyplot as plt

class MuStarComputerRevised:
    """
    Revised operator with drive term to generate non-trivial fixed points.
    """
    
    def __init__(self, n_points: int = 100, lambda_param: float = 0.6, 
                 kernel_sigma: float = 0.15, alpha: float = 0.5):
        self.n_points = n_points
        self.lambda_param = lambda_param
        self.kernel_sigma = kernel_sigma
        self.alpha = alpha  # Drive parameter
        
        self.x = np.linspace(0, 1, n_points)
        self.K_matrix = self._build_kernel_matrix()
        
    def _build_kernel_matrix(self):
        K = np.zeros((self.n_points, self.n_points))
        for i, xi in enumerate(self.x):
            for j, xj in enumerate(self.x):
                K[i, j] = np.exp(-(xi - xj)**2 / (2 * self.kernel_sigma**2))
        K = K / K.sum(axis=1, keepdims=True)
        return K
    
    @staticmethod
    def R(z):
        """R(z) = z/(1+z) - compression function"""
        return z / (1 + z)
    
    def apply_operator(self, mu):
        """
        T(μ) = λ[∫K(x,y)R(μ(y))dy + α]
        
        The α term provides constant self-reference drive.
        """
        integral_term = self.K_matrix @ self.R(mu)
        return self.lambda_param * (integral_term + self.alpha)
    
    def compute_fixed_point(self, max_iter=1000, tol=1e-6):
        mu = np.ones(self.n_points) * 0.5
        error_history = []
        
        for iteration in range(max_iter):
            mu_new = self.apply_operator(mu)
            error = np.max(np.abs(mu_new - mu))
            error_history.append(error)
            
            if error < tol:
                return mu_new, iteration + 1, error_history
            
            mu = mu_new
        
        raise ValueError(f"No convergence after {max_iter} iterations")


def demonstrate_revised_operator():
    """
    Demonstrate non-trivial fixed point with drive term.
    """
    print("="*70)
    print("REVISED OPERATOR: Non-Trivial Fixed Point Computation")
    print("="*70)
    print()
    
    # Test with drive parameter
    print("Testing with drive parameter α = 0.5...")
    computer = MuStarComputerRevised(n_points=100, lambda_param=0.6, 
                                    kernel_sigma=0.15, alpha=0.5)
    
    mu_star, iters, error_history = computer.compute_fixed_point()
    
    print(f"✓ Converged in {iters} iterations")
    print(f"  μ*(0.0) = {mu_star[0]:.6f}")
    print(f"  μ*(0.5) = {mu_star[50]:.6f}")
    print(f"  μ*(1.0) = {mu_star[-1]:.6f}")
    print(f"  Mean μ* = {np.mean(mu_star):.6f}")
    print(f"  Std μ*  = {np.std(mu_star):.6f}")
    print()
    
    # Verify fixed point
    T_mu_star = computer.apply_operator(mu_star)
    residual = np.max(np.abs(T_mu_star - mu_star))
    print(f"Fixed point verification:")
    print(f"  ||T(μ*) - μ*||_∞ = {residual:.2e}")
    print(f"  Status: {'✓ VERIFIED' if residual < 1e-5 else '✗ FAILED'}")
    print()
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: μ*(x)
    ax = axes[0, 0]
    ax.plot(computer.x, mu_star, 'b-', linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('μ*(x)')
    ax.set_title('Non-Trivial Fixed Point μ*(x)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=np.mean(mu_star), color='r', linestyle='--', 
               alpha=0.5, label=f'Mean = {np.mean(mu_star):.3f}')
    ax.legend()
    
    # Plot 2: Convergence
    ax = axes[0, 1]
    ax.semilogy(error_history, 'r-', linewidth=2)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Error')
    ax.set_title('Convergence History')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Kernel
    ax = axes[1, 0]
    im = ax.imshow(computer.K_matrix, cmap='viridis', aspect='auto')
    ax.set_title('Coupling Kernel K(x,y)')
    plt.colorbar(im, ax=ax)
    
    # Plot 4: Phase portrait (μ vs T(μ))
    ax = axes[1, 1]
    T_values = computer.apply_operator(mu_star)
    ax.plot(mu_star, T_values, 'go', markersize=4, alpha=0.6, label='(μ, T(μ))')
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='μ = T(μ)')
    ax.set_xlabel('μ')
    ax.set_ylabel('T(μ)')
    ax.set_title('Fixed Point Check: T(μ*) = μ*')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/mu_star_revised.png', dpi=150, bbox_inches='tight')
    print("✓ Visualization saved to: mu_star_revised.png")
    print()
    
    # Test different drive values
    print("Testing sensitivity to drive parameter α:")
    print("-" * 50)
    alpha_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for alpha in alpha_values:
        comp = MuStarComputerRevised(alpha=alpha)
        mu, iters, _ = comp.compute_fixed_point()
        mean_mu = np.mean(mu)
        std_mu = np.std(mu)
        print(f"  α = {alpha:.1f}: μ̄ = {mean_mu:.4f}, σ = {std_mu:.4f}, iters = {iters}")
    
    print()
    print("="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print()
    
    print("Physical Interpretation:")
    print("  - α > 0: Constant self-reference 'drive' or 'source'")
    print("  - μ*(x): Equilibrium distribution of self-reference intensity")
    print("  - Higher α → Higher baseline self-reference")
    print("  - K(x,y): Spatial coupling/interaction between locations")
    print("  - R(z): Nonlinear saturation preventing unbounded growth")
    print()
    
    return computer, mu_star

if __name__ == "__main__":
    demonstrate_revised_operator()
