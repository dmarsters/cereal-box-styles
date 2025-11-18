"""
Olog compiler: converts YAML categorical specifications into diagrams and MCP servers.

This tool:
1. Parses YAML olog specifications
2. Validates commutative diagrams
3. Generates visual diagrams (Mermaid/Graphviz)
4. Compiles to executable MCP server code
"""

import yaml
import json
from typing import Dict, List, Set
from pathlib import Path


class OlogParser:
    """Parse and validate YAML olog specifications."""
    
    def __init__(self, yaml_path: str):
        with open(yaml_path, 'r') as f:
            self.spec = yaml.safe_load(f)
        
        self.metadata = self.spec['olog']['metadata']
        self.types = self.spec['olog']['types']
        self.morphisms = self.spec['olog']['morphisms']
        self.diagrams = self.spec['olog']['commutative_diagrams']
        self.natural_transforms = self.spec['olog'].get('natural_transformations', {})
    
    def validate(self) -> Dict[str, List[str]]:
        """Validate the olog structure."""
        errors = []
        warnings = []
        
        # Check that all morphisms reference existing types
        type_names = set(self.types.keys())
        
        for morphism in self.morphisms:
            source = morphism['source'].split(' + ')[0]  # Handle composite types
            target = morphism['target']
            
            if source not in type_names:
                errors.append(f"Morphism '{morphism['name']}' references unknown source type '{source}'")
            if target not in type_names:
                errors.append(f"Morphism '{morphism['name']}' references unknown target type '{target}'")
        
        # Check that all commutative diagram paths reference existing morphisms
        morphism_names = {m['name'] for m in self.morphisms}
        
        for diagram_name, diagram in self.diagrams.items():
            # Some diagrams have 'paths', others have different structures
            if 'paths' in diagram:
                for path in diagram['paths']:
                    # Paths are described in natural language; we just check they're non-empty
                    if not path.get('steps'):
                        warnings.append(f"Commutative diagram '{diagram_name}' has path without steps")
            elif 'constraint_type' not in diagram:
                warnings.append(f"Commutative diagram '{diagram_name}' has unknown structure")
        
        return {
            'errors': errors,
            'warnings': warnings,
            'valid': len(errors) == 0
        }


class OlogDiagramGenerator:
    """Generate visual representations of ologs."""
    
    def __init__(self, parser: OlogParser):
        self.parser = parser
    
    def generate_mermaid(self) -> str:
        """Generate Mermaid diagram syntax."""
        
        lines = [
            "graph TD",
            f"    title[{self.parser.metadata['name']}]",
        ]
        
        # Add types as nodes
        for type_name in self.parser.types.keys():
            lines.append(f"    {type_name}[{type_name}]")
        
        # Add morphisms as edges
        for morphism in self.parser.morphisms:
            source = morphism['source'].replace(' + ', '<br/>+<br/>')
            target = morphism['target']
            name = morphism['name']
            description = morphism.get('description', '')
            
            # Mermaid syntax for edge labels
            lines.append(f"    {source} -->|{name}| {target}")
        
        # Add commutative diagram annotations
        for diagram_name, diagram in self.parser.diagrams.items():
            lines.append(f"    note_{diagram_name}[\"{diagram_name}<br/>{diagram['description']}\" ]")
        
        return "\n".join(lines)
    
    def generate_graphviz(self) -> str:
        """Generate Graphviz DOT format for more sophisticated layouts."""
        
        lines = [
            "digraph G {",
            f'    label = "{self.parser.metadata["name"]}";',
            "    rankdir = TB;",
            "    node [shape=box, style=rounded];",
            ""
        ]
        
        # Types as nodes
        for type_name, type_spec in self.parser.types.items():
            instances_str = ", ".join(type_spec['instances'][:3])
            if len(type_spec['instances']) > 3:
                instances_str += f", ... ({len(type_spec['instances'])} total)"
            
            label = f"{type_name}\\n{type_spec['description']}"
            lines.append(f'    "{type_name}" [label="{label}"];')
        
        lines.append("")
        
        # Morphisms as edges
        for morphism in self.parser.morphisms:
            source = morphism['source'].split(' + ')[0]
            target = morphism['target']
            name = morphism['name']
            
            lines.append(f'    "{source}" -> "{target}" [label="{name}"];')
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def save_diagram(self, format: str = 'mermaid', output_path: str = None):
        """Save diagram to file."""
        if format == 'mermaid':
            diagram = self.generate_mermaid()
            if not output_path:
                output_path = f"{self.parser.metadata['name']}.mmd"
        elif format == 'graphviz':
            diagram = self.generate_graphviz()
            if not output_path:
                output_path = f"{self.parser.metadata['name']}.dot"
        else:
            raise ValueError(f"Unknown format: {format}")
        
        with open(output_path, 'w') as f:
            f.write(diagram)
        
        print(f"Diagram saved to {output_path}")
        return output_path


class OlogToMCPCompiler:
    """Compile YAML olog to executable MCP server code."""
    
    def __init__(self, parser: OlogParser):
        self.parser = parser
    
    def compile(self, output_path: str = None) -> str:
        """Compile olog to MCP server Python code."""
        
        if not output_path:
            output_path = f"{self.parser.metadata['name']}_mcp.py"
        
        code = self._generate_mcp_stub()
        
        with open(output_path, 'w') as f:
            f.write(code)
        
        print(f"MCP server code generated at {output_path}")
        return output_path
    
    def _generate_mcp_stub(self) -> str:
        """Generate stub MCP server code from olog."""
        
        type_imports = ", ".join(self.parser.types.keys())
        
        code = f'''"""
MCP Server auto-generated from {self.parser.metadata['name']} olog specification.
Generated by OlogToMCPCompiler.

This server implements the categorical structure defined in the olog:
{self.parser.metadata['description']}
"""

from fastmcp import FastMCP
from typing import Literal
import json

mcp = FastMCP("{self.parser.metadata['name']}")

# ============================================================================
# TYPE DEFINITIONS (from olog)
# ============================================================================

TYPES = {{'''
        
        for type_name, type_spec in self.parser.types.items():
            instances = json.dumps(type_spec['instances'])
            code += f'''
    "{type_name}": {{
        "description": "{type_spec['description']}",
        "instances": {instances},
        "properties": {json.dumps(type_spec.get('properties', []))}
    }},'''
        
        code += '''
}

# ============================================================================
# MORPHISM IMPLEMENTATIONS (from olog)
# ============================================================================

'''
        
        # Generate tool stubs for key morphisms
        for morphism in self.parser.morphisms:
            if morphism.get('deterministic'):
                code += self._generate_morphism_tool(morphism)
        
        code += '''
# ============================================================================
# COMMUTATIVE DIAGRAM VALIDATORS
# ============================================================================

'''
        
        for diagram_name, diagram in self.parser.diagrams.items():
            code += self._generate_diagram_validator(diagram_name, diagram)
        
        code += f'''
# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
def list_types() -> dict:
    """List all types in the {self.parser.metadata['name']} olog."""
    return TYPES

@mcp.tool()
def get_type_instances(type_name: str) -> dict:
    """Get instances of a specific type."""
    if type_name not in TYPES:
        return {{"error": f"Unknown type: {{type_name}}"}}
    
    return {{
        "type": type_name,
        "description": TYPES[type_name]["description"],
        "instances": TYPES[type_name]["instances"]
    }}

@mcp.tool()
def validate_composition(component_choices: dict) -> dict:
    """
    Validate that chosen components satisfy commutative diagram constraints.
    
    Args:
        component_choices: dict with keys like 'palette', 'material', 'lighting', 'camera'
    
    Returns:
        dict with validation results and any constraint violations
    """
    violations = []
    
    # TODO: Implement actual constraint checking based on commutative diagrams
    
    return {{
        "valid": len(violations) == 0,
        "violations": violations,
        "message": "All commutative diagram constraints satisfied" if len(violations) == 0 else "Constraint violations detected"
    }}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
'''
        
        return code
    
    def _generate_morphism_tool(self, morphism: Dict) -> str:
        """Generate a tool for a deterministic morphism."""
        
        tool_name = morphism['name']
        source = morphism['source']
        target = morphism['target']
        description = morphism.get('description', '')
        
        return f'''
@mcp.tool()
def {tool_name}(source_instance: str) -> dict:
    """
    Morphism: {source} → {target}
    {description}
    
    Args:
        source_instance: Instance of {source}
    
    Returns:
        Instance of {target}
    """
    # TODO: Implement actual morphism logic
    return {{"source": source_instance, "target": "TODO", "morphism": "{tool_name}"}}

'''
    
    def _generate_diagram_validator(self, diagram_name: str, diagram: Dict) -> str:
        """Generate a validator for a commutative diagram."""
        
        description = diagram.get('description', '')
        constraint_type = diagram.get('constraint_type', 'unknown')
        
        return f'''
def validate_{diagram_name}(components: dict) -> dict:
    """
    Validate commutative diagram: {diagram_name}
    {description}
    Constraint type: {constraint_type}
    """
    # TODO: Implement actual diagram validation
    return {{"diagram": "{diagram_name}", "valid": True}}

'''


def main():
    """CLI for olog compilation."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python olog_compiler.py <olog.yaml> [--diagram] [--mcp]")
        print("  --diagram: Generate visual diagram (Mermaid)")
        print("  --mcp: Generate MCP server code")
        sys.exit(1)
    
    yaml_path = sys.argv[1]
    
    # Parse olog
    parser = OlogParser(yaml_path)
    
    # Validate
    validation = parser.validate()
    if not validation['valid']:
        print("Validation errors:")
        for error in validation['errors']:
            print(f"  ERROR: {error}")
        sys.exit(1)
    
    if validation['warnings']:
        print("Validation warnings:")
        for warning in validation['warnings']:
            print(f"  WARNING: {warning}")
    
    # Generate outputs
    if '--diagram' in sys.argv or '--all' in sys.argv:
        diagram_gen = OlogDiagramGenerator(parser)
        diagram_gen.save_diagram(format='graphviz')
    
    if '--mcp' in sys.argv or '--all' in sys.argv:
        compiler = OlogToMCPCompiler(parser)
        compiler.compile()
    
    print("Compilation complete.")


if __name__ == "__main__":
    main()
