#!/usr/bin/env python3
"""
Curriculum Graph Generator — builds a traversable graph from module prerequisites.

Outputs:
- curriculum_graph.yaml: Full graph with nodes and edges
- curriculum_graph.dot: Graphviz DOT format for visualization
- Journey paths: Named sequences through the graph for each certification track
"""

import yaml
import sys
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum/workstreams"
OUTPUT_DIR = ENABLEMENT_ROOT / "curriculum"


def find_modules(curriculum_root):
    """Find all module.yaml files."""
    modules = {}
    for module_path in Path(curriculum_root).rglob("module.yaml"):
        with open(module_path, 'r') as f:
            module = yaml.safe_load(f)
        module['_path'] = str(module_path.relative_to(ENABLEMENT_ROOT))
        modules[module['riu_id']] = module
    return modules


def build_graph(modules):
    """Build graph structure for YAML output."""
    nodes = []
    edges = []

    for riu_id, module in sorted(modules.items()):
        node = {
            'id': riu_id,
            'name': module['name'],
            'workstream': module.get('workstream', ''),
            'journey_stage': module.get('journey_stage', ''),
            'classification': module.get('classification', ''),
            'difficulty': module.get('difficulty', ''),
            'path': module.get('_path', ''),
        }
        nodes.append(node)

        prereqs = module.get('prerequisites', {})
        for req in prereqs.get('required', []) or []:
            edges.append({
                'from': req,
                'to': riu_id,
                'type': 'required',
            })
        for req in prereqs.get('recommended', []) or []:
            edges.append({
                'from': req,
                'to': riu_id,
                'type': 'recommended',
            })

    return {'nodes': nodes, 'edges': edges}


def generate_dot(graph, modules):
    """Generate Graphviz DOT format."""
    lines = ['digraph curriculum {']
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=box, style=rounded, fontname="Arial"];')
    lines.append('')

    # Color by journey stage
    stage_colors = {
        'foundation': '#4CAF50',
        'retrieval': '#2196F3',
        'orchestration': '#FF9800',
        'specialization': '#9C27B0',
        'evaluation': '#F44336',
        'all': '#607D8B',
    }

    # Add nodes grouped by workstream
    workstreams = defaultdict(list)
    for node in graph['nodes']:
        workstreams[node['workstream']].append(node)

    for ws, ws_nodes in workstreams.items():
        ws_safe = ws.replace(' ', '_').replace('&', 'and')
        lines.append(f'  subgraph cluster_{ws_safe} {{')
        lines.append(f'    label="{ws}";')
        lines.append(f'    style=dashed;')
        for node in ws_nodes:
            color = stage_colors.get(node['journey_stage'], '#999999')
            label = f"{node['id']}\\n{node['name'][:30]}"
            lines.append(f'    "{node["id"]}" [label="{label}", fillcolor="{color}", style="rounded,filled", fontcolor="white"];')
        lines.append('  }')
        lines.append('')

    # Add edges
    for edge in graph['edges']:
        style = 'solid' if edge['type'] == 'required' else 'dashed'
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}" [style={style}];')

    lines.append('}')
    return '\n'.join(lines)


def identify_entry_points(modules):
    """Find modules with no required prerequisites (entry points)."""
    entry_points = []
    for riu_id, module in modules.items():
        prereqs = module.get('prerequisites', {})
        required = prereqs.get('required', []) or []
        if not required:
            entry_points.append(riu_id)
    return sorted(entry_points)


def generate_graph():
    print("Generating curriculum graph...")

    modules = find_modules(CURRICULUM_ROOT)
    if not modules:
        print("[WARN] No modules found. Nothing to generate.")
        return

    graph = build_graph(modules)

    # Write YAML graph
    graph_output = {
        'generated_from': 'enablement/curriculum/workstreams/**/module.yaml',
        'total_nodes': len(graph['nodes']),
        'total_edges': len(graph['edges']),
        'entry_points': identify_entry_points(modules),
        'graph': graph,
    }

    yaml_path = OUTPUT_DIR / "curriculum_graph.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(graph_output, f, default_flow_style=False, sort_keys=False)
    print(f"  Written: {yaml_path}")

    # Write DOT graph
    dot_content = generate_dot(graph, modules)
    dot_path = OUTPUT_DIR / "curriculum_graph.dot"
    with open(dot_path, 'w') as f:
        f.write(dot_content)
    print(f"  Written: {dot_path}")

    # Summary
    print(f"\n  Nodes: {len(graph['nodes'])}")
    print(f"  Edges: {len(graph['edges'])}")
    print(f"  Entry points: {', '.join(identify_entry_points(modules))}")


if __name__ == "__main__":
    generate_graph()
