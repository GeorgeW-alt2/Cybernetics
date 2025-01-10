"""Cybernetics System Simulation"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
from pprint import pprint
"""Enhanced Cybernetics System with Customizable Statement Generation"""
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import random
from abc import ABC, abstractmethod


@dataclass
class GenerationRule:
    """Defines rules for generating new statements"""
    name: str
    conditions: List[Callable[[Dict[str, Any]], bool]]  # Functions that take context and return bool
    templates: List[str]  # Statement templates with placeholders
    variables: Dict[str, List[str]]  # Possible values for each placeholder
    weight: float = 1.0  # Probability weight for rule selection

    def should_apply(self, context: Dict[str, Any]) -> bool:
        """Check if all conditions are met for this rule"""
        return all(condition(context) for condition in self.conditions)

    def generate_statement(self, context: Dict[str, Any]) -> str:
        """Generate a statement using this rule's templates and variables"""
        template = random.choice(self.templates)
        
        # Replace placeholders with random choices from variables
        for var_name, values in self.variables.items():
            if f"{{{var_name}}}" in template:
                template = template.replace(f"{{{var_name}}}", random.choice(values))
                
        return template

@dataclass
class StatementGenerator:
    """Handles customizable statement generation"""
    rules: List[GenerationRule] = field(default_factory=list)
    
    def add_rule(self, rule: GenerationRule) -> None:
        """Add a new generation rule"""
        self.rules.append(rule)
    
    def generate(self, context: Dict[str, Any]) -> Optional[str]:
        """Generate a statement based on applicable rules"""
        applicable_rules = [rule for rule in self.rules if rule.should_apply(context)]
        if not applicable_rules:
            return None
            
        # Select rule based on weights
        total_weight = sum(rule.weight for rule in applicable_rules)
        random_val = random.uniform(0, total_weight)
        cumulative_weight = 0
        
        for rule in applicable_rules:
            cumulative_weight += rule.weight
            if random_val <= cumulative_weight:
                return rule.generate_statement(context)
        
        return None

class SystemPrimitive:
    """Enhanced SystemPrimitive with customizable statement generation"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.adaptation_threshold = 0.7
        self.adaptation_history = []
        self.metrics = {
            "reliability": 0.9,
            "complexity": 0.6,
            "maintainability": 0.8,
            "adaptation_rate": 0.0
        }
        self.generator = self._create_generator()
    
    def _create_generator(self) -> StatementGenerator:
        """Create and configure the statement generator with rules"""
        generator = StatementGenerator()
        
        # Efficiency improvement rule
        generator.add_rule(GenerationRule(
            name="efficiency_improvement",
            conditions=[
                lambda ctx: ctx.get("feedback_score", 0) > 0.7,
                lambda ctx: "efficiency" in self.name.lower()
            ],
            templates=[
                "Optimize {resource} allocation using {algorithm}",
                "Implement {technique} for improved {aspect} efficiency",
                "Deploy {strategy} to enhance {resource} utilization"
            ],
            variables={
                "resource": ["CPU", "memory", "network", "storage", "compute"],
                "algorithm": ["adaptive algorithms", "machine learning", "predictive models", "dynamic allocation"],
                "technique": ["load balancing", "caching", "parallel processing", "resource pooling"],
                "aspect": ["system", "runtime", "operational", "resource"],
                "strategy": ["automated scaling", "dynamic provisioning", "intelligent routing", "adaptive optimization"]
            },
            weight=1.5
        ))
        
        # Security enhancement rule
        generator.add_rule(GenerationRule(
            name="security_enhancement",
            conditions=[
                lambda ctx: "security" in self.name.lower(),
                lambda ctx: ctx.get("system_state", {}).get("stability", 1.0) < 0.8
            ],
            templates=[
                "Implement {security_measure} to protect against {threat}",
                "Enhance {component} security using {technique}",
                "Deploy {security_system} for improved {protection_type}"
            ],
            variables={
                "security_measure": ["encryption", "authentication", "access control", "intrusion detection"],
                "threat": ["unauthorized access", "data breaches", "malicious attacks", "system vulnerabilities"],
                "component": ["network", "data", "system", "application"],
                "technique": ["AI-powered monitoring", "blockchain", "zero-trust architecture", "behavioral analysis"],
                "security_system": ["anomaly detection", "threat prevention", "security validation", "compliance monitoring"],
                "protection_type": ["data protection", "system security", "access management", "threat prevention"]
            },
            weight=1.2
        ))
        
        # Reliability improvement rule
        generator.add_rule(GenerationRule(
            name="reliability_improvement",
            conditions=[
                lambda ctx: "reliability" in self.name.lower() or ctx.get("system_state", {}).get("stability", 1.0) < 0.6
            ],
            templates=[
                "Implement {mechanism} for improved {aspect} reliability",
                "Deploy {system} to ensure {component} stability",
                "Enhance {service} using {technique} for better reliability"
            ],
            variables={
                "mechanism": ["failover", "redundancy", "load distribution", "health monitoring"],
                "aspect": ["system", "service", "operational", "component"],
                "system": ["automated recovery", "fault tolerance", "service resilience", "stability control"],
                "component": ["critical services", "core functions", "system components", "key operations"],
                "service": ["system monitoring", "error handling", "performance tracking", "health checks"],
                "technique": ["predictive maintenance", "automated recovery", "distributed redundancy", "adaptive failover"]
            },
            weight=1.0
        ))
        
        # Adaptation rule
        generator.add_rule(GenerationRule(
            name="adaptation_improvement",
            conditions=[
                lambda ctx: ctx.get("adaptation_rate", 0) > 0.5
            ],
            templates=[
                "Implement {adaptation_type} for {component} adaptation",
                "Enhance {aspect} using {technique} adaptation",
                "Deploy {system} for improved {target} adaptability"
            ],
            variables={
                "adaptation_type": ["dynamic", "intelligent", "automated", "predictive"],
                "component": ["system", "service", "resource", "process"],
                "aspect": ["performance", "efficiency", "reliability", "operation"],
                "technique": ["machine learning", "feedback-driven", "context-aware", "adaptive"],
                "system": ["learning algorithms", "adaptation mechanisms", "dynamic controls", "adaptive systems"],
                "target": ["system", "operational", "performance", "resource"]
            },
            weight=0.8
        ))
        
        return generator

    def adapt(self, feedback: float, context: dict) -> Optional[str]:
        """Enhanced adapt method with customizable statement generation"""
        if abs(feedback) > self.adaptation_threshold:
            # Update metrics as before
            adaptation = {
                "timestamp": datetime.now(),
                "feedback": feedback,
                "context": context,
                "previous_metrics": self.metrics.copy()
            }
            
            learning_rate = 0.1
            self.metrics["adaptation_rate"] = (
                self.metrics["adaptation_rate"] * (1 - learning_rate) +
                abs(feedback) * learning_rate
            )
            
            for metric in ["reliability", "complexity", "maintainability"]:
                if feedback > 0:
                    self.metrics[metric] = min(1.0, self.metrics[metric] * (1 + learning_rate * feedback))
                else:
                    self.metrics[metric] = max(0.0, self.metrics[metric] * (1 + learning_rate * feedback))
            
            self.adaptation_history.append(adaptation)
            
            # Generate new statement using the generator
            generation_context = {
                "feedback_score": feedback,
                "system_state": context.get("system_state", {}),
                "adaptation_rate": self.metrics["adaptation_rate"],
                "cycle": context.get("cycle", 0)
            }
            
            return self.generator.generate(generation_context)
            
        return None

class FeedbackType(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class Statement:
    content: str
    system_primitives: List['SystemPrimitive'] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    feedback_history: List[tuple[FeedbackType, float]] = field(default_factory=list)
    generated_from: Optional[str] = None  # Track what generated this statement
    
    def add_feedback(self, feedback_type: FeedbackType, strength: float) -> None:
        self.feedback_history.append((feedback_type, strength))
    
    def get_feedback_score(self) -> float:
        if not self.feedback_history:
            return 0.0
        total_weight = 0.0
        weighted_sum = 0.0
        for i, (feedback_type, strength) in enumerate(self.feedback_history):
            weight = math.exp(i / len(self.feedback_history))
            if feedback_type == FeedbackType.POSITIVE:
                weighted_sum += strength * weight
            elif feedback_type == FeedbackType.NEGATIVE:
                weighted_sum -= strength * weight
            total_weight += weight
        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _generate_improvement_statement(self) -> str:
        improvements = {
            "Efficiency": [
                "Optimize resource allocation for improved efficiency",
                "Implement automated performance tuning mechanisms",
                "Enhance system throughput with adaptive algorithms"
            ],
            "Security": [
                "Strengthen security measures with advanced protocols",
                "Implement additional layer of security validation",
                "Enhance threat detection capabilities"
            ],
            "Reliability": [
                "Implement redundant failover systems",
                "Enhance error recovery mechanisms",
                "Add automated system health monitoring"
            ],
            "Generic": [
                "Implement adaptive feedback mechanisms",
                "Enhance system monitoring capabilities",
                "Optimize resource utilization patterns"
            ]
        }
        category = next((k for k in improvements.keys() if k.lower() in self.name.lower()), "Generic")
        return improvements[category][hash(str(datetime.now())) % len(improvements[category])]

    def _generate_correction_statement(self) -> str:
        corrections = {
            "Efficiency": [
                "Revise resource allocation strategy to address performance bottlenecks",
                "Implement emergency resource management protocols",
                "Add performance degradation safeguards"
            ],
            "Security": [
                "Address identified security vulnerabilities",
                "Implement additional security validation layers",
                "Enhance breach detection mechanisms"
            ],
            "Reliability": [
                "Implement additional error handling mechanisms",
                "Add system stability safeguards",
                "Enhance recovery protocols"
            ],
            "Generic": [
                "Implement correction feedback loops",
                "Add system stabilization mechanisms",
                "Enhance error detection capabilities"
            ]
        }
        category = next((k for k in corrections.keys() if k.lower() in self.name.lower()), "Generic")
        return corrections[category][hash(str(datetime.now())) % len(corrections[category])]

class CyberneticSystem:
    def __init__(self):
        self.statements: List[Statement] = []
        self.feedback_threshold: float = 0.6
        self.adaptation_cycles: int = 0
        self.system_state: Dict[str, Any] = {
            "stability": 1.0,
            "complexity": 0.0,
            "adaptation_rate": 0.0
        }
        self.new_statements: List[tuple[int, Statement]] = []  # (cycle, statement)
    
    def add_statement(self, content: str, generated_from: Optional[str] = None) -> Statement:
        statement = Statement(content, generated_from=generated_from)
        primitive = self._create_primitive_for_statement(content)
        statement.system_primitives.append(primitive)
        self.statements.append(statement)
        return statement
    
    def _create_primitive_for_statement(self, content: str) -> SystemPrimitive:
        keywords = {
            "efficiency": ("Efficiency_Primitive", "Optimizes system efficiency"),
            "security": ("Security_Primitive", "Enhances system security"),
            "reliability": ("Reliability_Primitive", "Improves system reliability"),
            "adaptation": ("Adaptation_Primitive", "Handles system adaptation")
        }
        
        for keyword, (name, desc) in keywords.items():
            if keyword in content.lower():
                return SystemPrimitive(name, desc)
        return SystemPrimitive("Generic_Primitive", "Handles general system operations")
    
    def process_feedback_cycle(self) -> dict:
        cycle_metrics = {
            "processed_statements": 0,
            "adaptations": 0,
            "average_feedback": 0.0,
            "primitive_metrics": {}
        }
        
        total_feedback = 0.0
        
        for statement in self.statements.copy():  # Use copy to allow modification during iteration
            feedback_score = statement.get_feedback_score()
            
            if abs(feedback_score) > self.feedback_threshold:
                context = {
                    "system_state": self.system_state.copy(),
                    "cycle": self.adaptation_cycles,
                    "timestamp": datetime.now()
                }
                
                for primitive in statement.system_primitives:
                    new_statement_content = primitive.adapt(feedback_score, context)
                    if new_statement_content:
                        new_statement = self.add_statement(
                            new_statement_content,
                            generated_from=statement.content
                        )
                        self.new_statements.append((self.adaptation_cycles, new_statement))
                    
                    cycle_metrics["adaptations"] += 1
                    cycle_metrics["primitive_metrics"][primitive.name] = primitive.metrics.copy()
            
            total_feedback += feedback_score
            cycle_metrics["processed_statements"] += 1
        
        if cycle_metrics["processed_statements"] > 0:
            cycle_metrics["average_feedback"] = total_feedback / cycle_metrics["processed_statements"]
        
        self._update_system_state(cycle_metrics)
        self.adaptation_cycles += 1
        
        return cycle_metrics
    
    def _update_system_state(self, cycle_metrics: dict) -> None:
        if cycle_metrics["processed_statements"] > 0:
            feedback_impact = abs(cycle_metrics["average_feedback"])
            self.system_state["stability"] *= (1 - 0.1 * feedback_impact)
            self.system_state["stability"] = max(0.1, min(1.0, self.system_state["stability"]))
        
        complexity_factor = cycle_metrics["adaptations"] / max(1, len(self.statements))
        self.system_state["complexity"] = (
            self.system_state["complexity"] * 0.9 +
            complexity_factor * 0.1
        )
        
        self.system_state["adaptation_rate"] = (
            cycle_metrics["adaptations"] / max(1, cycle_metrics["processed_statements"])
        )

def main():
    print("\n=== Cybernetic System Simulation ===\n")
    
    # Initialize system
    system = CyberneticSystem()
    
    # Add initial statements
    initial_statements = [
        "Improve system efficiency through resource optimization",
        "Enhance security protocols for data protection",
        "Implement reliability measures for critical components",
        "Enable adaptive responses to system changes",
        "Optimize performance through machine learning",
    ]
    
    print("Initial Statements:")
    print("-" * 50)
    for i, content in enumerate(initial_statements, 1):
        statement = system.add_statement(content)
        print(f"{i}. {content}")
        # Add initial feedback
        statement.add_feedback(
            FeedbackType.POSITIVE if "efficiency" in content.lower() else FeedbackType.NEUTRAL,
            0.8
        )
    
    print("\nRunning Adaptation Cycles:")
    print("-" * 50)
    
    # Run adaptation cycles
    for cycle in range(5):
        print(f"\nCycle {cycle + 1}:")
        print("-" * 20)
        
        # Process feedback cycle
        metrics = system.process_feedback_cycle()
        
        # Add dynamic feedback based on system state
        for statement in system.statements:
            if system.system_state["stability"] < 0.5:
                statement.add_feedback(FeedbackType.NEGATIVE, 0.6)
            else:
                statement.add_feedback(FeedbackType.POSITIVE, 0.7)
        
        # Print cycle results
        print(f"Processed Statements: {metrics['processed_statements']}")
        print(f"Adaptations: {metrics['adaptations']}")
        print(f"Average Feedback: {metrics['average_feedback']:.3f}")
        print("\nSystem State:")
        for key, value in system.system_state.items():
            print(f"  {key.title()}: {value:.3f}")
    
    # Print all new statements generated during the simulation
    print("\nNew Statements Generated During Simulation:")
    print("-" * 50)
    
    if system.new_statements:
        current_cycle = -1
        for cycle, statement in sorted(system.new_statements, key=lambda x: (x[0], x[1].content)):
            if cycle != current_cycle:
                print(f"\nCycle {cycle + 1}:")
                current_cycle = cycle
            print(f"  • {statement.content}")
            if statement.generated_from:
                print(f"    Generated from: \"{statement.generated_from}\"")
    else:
        print("No new statements were generated during the simulation.")

if __name__ == "__main__":
    main()
