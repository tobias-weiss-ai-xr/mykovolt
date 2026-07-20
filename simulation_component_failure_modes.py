import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class ComponentFailureAnalyzer:
    """
    Analyzes component failure modes and their impact on system performance.
    
    This class provides tools to model, simulate, and analyze failure scenarios
    for bio-battery components, helping to identify critical failure points
    and develop mitigation strategies.
    """
    
    def __init__(self):
        self.components = {}
        self.failure_modes = {}
        self.simulation_results = {}
        
    def add_component(self, name: str, parameters: Dict):
        """
        Add a component to the analysis with its parameters.
        
        Args:
            name: Component name (e.g., 'nfc_controller', 'microcontroller')
            parameters: Dictionary containing component parameters
        """
        self.components[name] = {
            'name': name,
            'parameters': parameters,
            'failure_probability': parameters.get('failure_probability', 0.01),
            'failure_impact': parameters.get('failure_impact', 1.0),
            'mtbf': parameters.get('mtbf', 10000),  # Mean Time Between Failures
            'repair_time': parameters.get('repair_time', 24),  # hours
            'redundancy_level': parameters.get('redundancy_level', 1)
        }
        
    def add_failure_mode(self, component_name: str, mode: str, probability: float, impact: float):
        """
        Add a specific failure mode for a component.
        
        Args:
            component_name: Name of the component
            mode: Description of failure mode
            probability: Probability of this failure mode occurring
            impact: Impact on system performance (0-1 scale)
        """
        if component_name not in self.failure_modes:
            self.failure_modes[component_name] = []
            
        self.failure_modes[component_name].append({
            'mode': mode,
            'probability': probability,
            'impact': impact,
            'severity': probability * impact
        })
        
    def monte_carlo_simulation(self, num_simulations: int = 10000) -> Dict:
        """
        Run Monte Carlo simulation to analyze system reliability.
        
        Args:
            num_simulations: Number of simulation iterations
            
        Returns:
            Dictionary containing simulation results
        """
        results = {
            'system_failures': [],
            'component_failures': {},
            'downtime_hours': [],
            'performance_degradation': []
        }
        
        for i in range(num_simulations):
            system_ok = True
            component_failures = {}
            downtime = 0
            performance_impact = 0
            
            for comp_name, comp_data in self.components.items():
                # Simulate component failure
                failure_occurs = np.random.random() < comp_data['failure_probability']
                
                if failure_occurs:
                    system_ok = False
                    component_failures[comp_name] = True
                    downtime += comp_data['repair_time']
                    performance_impact += comp_data['failure_impact']
                    
                    # Check for failure modes
                    if comp_name in self.failure_modes:
                        for failure_mode in self.failure_modes[comp_name]:
                            if np.random.random() < failure_mode['probability']:
                                performance_impact += failure_mode['impact']
                else:
                    component_failures[comp_name] = False
            
            results['system_failures'].append(not system_ok)
            results['component_failures'] = component_failures
            results['downtime_hours'].append(downtime)
            results['performance_degradation'].append(performance_impact)
        
        # Calculate statistics
        results['system_failure_rate'] = np.mean(results['system_failures'])
        results['average_downtime'] = np.mean(results['downtime_hours'])
        results['max_downtime'] = np.max(results['downtime_hours'])
        results['average_performance_impact'] = np.mean(results['performance_degradation'])
        
        return results
        
    def sensitivity_analysis(self, parameter_sensitivity: Dict) -> Dict:
        """
        Perform sensitivity analysis on key parameters.
        
        Args:
            parameter_sensitivity: Dictionary with parameter ranges to test
            
        Returns:
            Dictionary containing sensitivity analysis results
        """
        results = {}
        
        for param_name, param_range in parameter_sensitivity.items():
            parameter_values = np.linspace(param_range['min'], param_range['max'], 20)
            failure_rates = []
            
            for value in parameter_values:
                # Temporarily modify parameter
                original_value = self.components[param_name]['parameters'].get(param_name)
                self.components[param_name]['parameters'][param_name] = value
                
                # Run simulation
                sim_results = self.monte_carlo_simulation(1000)
                failure_rates.append(sim_results['system_failure_rate'])
                
                # Restore original value
                if original_value is not None:
                    self.components[param_name]['parameters'][param_name] = original_value
                else:
                    del self.components[param_name]['parameters'][param_name]
            
            # Calculate sensitivity metrics
            correlation = np.corrcoef(parameter_values, failure_rates)[0, 1]
            max_impact = np.max(np.abs(np.array(failure_rates) - np.mean(failure_rates)))
            
            results[param_name] = {
                'correlation': correlation,
                'max_impact': max_impact,
                'parameter_values': parameter_values.tolist(),
                'failure_rates': failure_rates
            }
        
        return results
        
    def generate_failure_report(self) -> str:
        """
        Generate a comprehensive failure analysis report.
        
        Returns:
            Formatted report string
        """
        report = "COMPONENT FAILURE ANALYSIS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # System reliability summary
        sim_results = self.monte_carlo_simulation(5000)
        
        report += "SYSTEM RELIABILITY SUMMARY\n"
        report += "-" * 30 + "\n"
        report += f"System Failure Rate: {sim_results['system_failure_rate']:.2%}\n"
        report += f"Average Downtime: {sim_results['average_downtime']:.1f} hours\n"
        report += f"Maximum Downtime: {sim_results['max_downtime']:.1f} hours\n"
        report += f"Average Performance Impact: {sim_results['average_performance_impact']:.2%}\n\n"
        
        # Component failure analysis
        report += "COMPONENT FAILURE ANALYSIS\n"
        report += "-" * 30 + "\n"
        
        for comp_name, comp_data in self.components.items():
            failure_count = sum(1 for sim in sim_results['component_failures'] 
                              if sim.get(comp_name, False))
            failure_rate = failure_count / len(sim_results['component_failures'])
            
            report += f"{comp_name.replace('_', ' ').title()}:\n"
            report += f"  Failure Rate: {failure_rate:.2%}\n"
            report += f"  MTBF: {comp_data['mtbf']} hours\n"
            report += f"  Redundancy Level: {comp_data['redundancy_level']}\n"
            
            if comp_name in self.failure_modes:
                report += f"  Critical Failure Modes:\n"
                for mode in self.failure_modes[comp_name]:
                    report += f"    - {mode['mode']}: {mode['probability']:.2%} probability, "
                    report += f"{mode['impact']:.1%} impact\n"
            
            report += "\n"
        
        # Recommendations
        report += "RECOMMENDATIONS\n"
        report += "-" * 30 + "\n"
        
        # Identify components needing attention
        high_risk_components = []
        for comp_name, comp_data in self.components.items():
            if comp_data['failure_probability'] > 0.05 or comp_data['failure_impact'] > 0.3:
                high_risk_components.append(comp_name)
        
        if high_risk_components:
            report += "High-Risk Components Requiring Attention:\n"
            for comp in high_risk_components:
                report += f"- {comp.replace('_', ' ').title()}\n"
            
            report += "\nMitigation Strategies:\n"
            report += "1. Increase redundancy for critical components\n"
            report += "2. Implement predictive maintenance programs\n"
            report += "3. Develop alternative supplier agreements\n"
            report += "4. Establish component monitoring systems\n"
        else:
            report += "All components within acceptable risk levels.\n"
        
        return report
        
    def visualize_failure_impact(self):
        """
        Create visualizations of failure impact analysis.
        
        Returns:
            Dictionary containing visualization data
        """
        sim_results = self.monte_carlo_simulation(5000)
        
        # Component failure frequency
        component_failure_freq = {}
        for comp_name in self.components.keys():
            failure_count = sum(1 for sim in sim_results['component_failures'] 
                              if sim.get(comp_name, False))
            component_failure_freq[comp_name] = failure_count / len(sim_results['component_failures'])
        
        # Performance degradation distribution
        perf_impact = sim_results['performance_degradation']
        
        visualizations = {
            'component_failure_frequency': component_failure_freq,
            'performance_impact_histogram': {
                'data': perf_impact,
                'mean': np.mean(perf_impact),
                'std': np.std(perf_impact)
            },
            'downtime_distribution': {
                'data': sim_results['downtime_hours'],
                'mean': np.mean(sim_results['downtime_hours']),
                'max': np.max(sim_results['downtime_hours'])
            }
        }
        
        return visualizations

# Example usage and testing
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = ComponentFailureAnalyzer()
    
    # Add components with realistic parameters
    analyzer.add_component('nfc_controller', {
        'failure_probability': 0.02,
        'failure_impact': 0.8,
        'mtbf': 50000,
        'repair_time': 4,
        'redundancy_level': 2
    })
    
    analyzer.add_component('microcontroller', {
        'failure_probability': 0.01,
        'failure_impact': 0.9,
        'mtbf': 100000,
        'repair_time': 8,
        'redundancy_level': 1
    })
    
    analyzer.add_component('power_management', {
        'failure_probability': 0.03,
        'failure_impact': 0.7,
        'mtbf': 75000,
        'repair_time': 6,
        'redundancy_level': 2
    })
    
    # Add failure modes
    analyzer.add_failure_mode('nfc_controller', 'communication_failure', 0.005, 0.9)
    analyzer.add_failure_mode('microcontroller', 'processor_error', 0.003, 0.8)
    analyzer.add_failure_mode('power_management', 'voltage_regulation_failure', 0.008, 0.6)
    
    # Run analysis
    results = analyzer.monte_carlo_simulation(10000)
    
    print("Component Failure Analysis Results:")
    print(f"System Failure Rate: {results['system_failure_rate']:.2%}")
    print(f"Average Downtime: {results['average_downtime']:.1f} hours")
    print(f"Average Performance Impact: {results['average_performance_impact']:.2%}")
    
    # Generate report
    report = analyzer.generate_failure_report()
    print("\n" + report)
    
    # Sensitivity analysis
    sensitivity_params = {
        'failure_probability': {'min': 0.001, 'max': 0.1},
        'failure_impact': {'min': 0.1, 'max': 1.0}
    }
    
    sensitivity_results = analyzer.sensitivity_analysis(sensitivity_params)
    print("\nSensitivity Analysis Results:")
    for param, results in sensitivity_results.items():
        print(f"{param}: Correlation = {results['correlation']:.3f}, Max Impact = {results['max_impact']:.3f}")