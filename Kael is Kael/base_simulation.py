"""
Base Simulation Framework for 33-Theorem Validation
Provides abstract template for all theorem simulations
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import numpy as np
import time


@dataclass
class SimulationMetadata:
    """Immutable simulation configuration."""
    theorem_id: int
    theorem_name: str
    random_seed: int
    n_trials: int
    parameters: Dict[str, Any]
    
    
@dataclass
class SimulationResult:
    """Standardized output format."""
    metadata: SimulationMetadata
    observables: Dict[str, np.ndarray]  # Time series or distributions
    statistics: Dict[str, float]         # Mean, std, CI
    validation_status: str               # PASS, FAIL, INCONCLUSIVE
    falsification_triggered: bool
    runtime_seconds: float
    

class BaseSimulation(ABC):
    """
    Abstract simulation template.
    All theorem simulations must inherit from this class.
    """
    
    def __init__(self, config: Dict[str, Any], seed: int = 42):
        self.config = config
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self._validate_config()
        
    @abstractmethod
    def _validate_config(self) -> None:
        """
        Check parameter bounds and dimensional consistency.
        Raise AssertionError if configuration is invalid.
        """
        pass
    
    @abstractmethod
    def init_state(self) -> Any:
        """
        Initialize system state.
        Returns: Initial state representation (can be dict, array, object)
        """
        pass
    
    @abstractmethod
    def update_rule(self, state: Any, t: int) -> Any:
        """
        Single time step evolution.
        Args:
            state: Current system state
            t: Time step index
        Returns: Updated state
        """
        pass
    
    @abstractmethod
    def measure_observables(self, state: Any) -> Dict[str, float]:
        """
        Extract measurable quantities from current state.
        Returns: Dictionary of observable_name -> value
        """
        pass
    
    @abstractmethod
    def check_falsification(self, observables: Dict[str, float]) -> bool:
        """
        Check if theorem prediction is violated.
        Returns: True if falsification criterion triggered
        """
        pass
    
    def run(self, n_steps: int) -> SimulationResult:
        """
        Execute simulation with full instrumentation.
        Args:
            n_steps: Number of time steps to simulate
        Returns: SimulationResult with full trajectory and statistics
        """
        start_time = time.time()
        
        state = self.init_state()
        trajectory = []
        
        for t in range(n_steps):
            obs = self.measure_observables(state)
            trajectory.append(obs)
            
            # Check falsification
            if self.check_falsification(obs):
                return self._build_result(
                    trajectory, 
                    time.time() - start_time, 
                    validation_status="FAIL", 
                    falsified=True
                )
            
            # Update state
            state = self.update_rule(state, t)
        
        return self._build_result(
            trajectory, 
            time.time() - start_time,
            validation_status="PASS", 
            falsified=False
        )
    
    def run_ensemble(self, n_trials: int = 100) -> List[SimulationResult]:
        """
        Run multiple trials with different seeds.
        Args:
            n_trials: Number of independent runs
        Returns: List of simulation results
        """
        results = []
        base_seed = self.config.get('base_seed', 42)
        
        for trial in range(n_trials):
            self.seed = base_seed + trial
            self.rng = np.random.default_rng(self.seed)
            results.append(self.run(self.config['n_steps']))
            
        return results
    
    def _build_result(
        self, 
        trajectory: List[Dict[str, float]], 
        runtime: float, 
        validation_status: str, 
        falsified: bool
    ) -> SimulationResult:
        """
        Aggregate trajectory into result object.
        Computes statistics across trajectory.
        """
        # Convert list of dicts to dict of arrays
        observables = {
            key: np.array([obs[key] for obs in trajectory])
            for key in trajectory[0].keys()
        }
        
        # Compute statistics
        statistics = {}
        for key, values in observables.items():
            statistics[f"{key}_mean"] = float(np.mean(values))
            statistics[f"{key}_std"] = float(np.std(values))
            statistics[f"{key}_final"] = float(values[-1])
            statistics[f"{key}_min"] = float(np.min(values))
            statistics[f"{key}_max"] = float(np.max(values))
        
        # Build metadata
        metadata = SimulationMetadata(
            theorem_id=self.config['theorem_id'],
            theorem_name=self.config['theorem_name'],
            random_seed=self.seed,
            n_trials=1,
            parameters=self.config
        )
        
        return SimulationResult(
            metadata=metadata,
            observables=observables,
            statistics=statistics,
            validation_status=validation_status,
            falsification_triggered=falsified,
            runtime_seconds=runtime
        )


class NullSimulation(BaseSimulation):
    """
    Minimal implementation for testing infrastructure.
    Does nothing but satisfy abstract interface.
    """
    
    def _validate_config(self) -> None:
        pass
    
    def init_state(self) -> Dict[str, float]:
        return {"x": 0.0}
    
    def update_rule(self, state: Dict[str, float], t: int) -> Dict[str, float]:
        return {"x": state["x"] + 0.1}
    
    def measure_observables(self, state: Dict[str, float]) -> Dict[str, float]:
        return {"x": state["x"]}
    
    def check_falsification(self, observables: Dict[str, float]) -> bool:
        return False


if __name__ == "__main__":
    # Test infrastructure
    print("Testing base simulation infrastructure...")
    
    config = {
        'theorem_id': 0,
        'theorem_name': 'Null Test',
        'n_steps': 10
    }
    
    sim = NullSimulation(config, seed=42)
    result = sim.run(n_steps=10)
    
    print(f"✓ Single run completed")
    print(f"  Status: {result.validation_status}")
    print(f"  Runtime: {result.runtime_seconds:.4f}s")
    print(f"  Final x: {result.statistics['x_final']:.2f}")
    
    print("\n✓ Base simulation infrastructure operational")
