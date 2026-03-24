#!/usr/bin/env python3
"""
Layer 1 — Automated Checks Evaluator

Pre-screens submissions before AI rubric evaluation.
Checks: artifacts present, code runs, sources cited, format valid.

Returns PASS/FAIL per check with specific failure reasons.
"""

import yaml
import os
import subprocess
import sys
from pathlib import Path


def check_artifacts_present(submission_dir, required_artifacts):
    """Check that all required artifacts exist in the submission."""
    results = []
    for artifact_spec in required_artifacts:
        # Extract filename from artifact spec (before the " — " description)
        filename = artifact_spec.split(" — ")[0].strip()
        # Handle directory artifacts (ending with /)
        if filename.endswith('/'):
            path = Path(submission_dir) / filename
            exists = path.is_dir() and any(path.iterdir())
            results.append({
                'artifact': filename,
                'check': 'directory_exists_and_nonempty',
                'passed': exists,
                'reason': None if exists else f"Directory '{filename}' missing or empty",
            })
        else:
            path = Path(submission_dir) / filename
            exists = path.is_file() and path.stat().st_size > 0
            results.append({
                'artifact': filename,
                'check': 'file_exists_and_nonempty',
                'passed': exists,
                'reason': None if exists else f"File '{filename}' missing or empty",
            })
    return results


def check_code_runs(submission_dir):
    """Check that any Python/JS files in the submission can at least be parsed."""
    results = []
    for ext, cmd_template in [('.py', 'python3 -m py_compile {}'), ('.js', 'node --check {}')]:
        for code_file in Path(submission_dir).rglob(f'*{ext}'):
            cmd = cmd_template.format(str(code_file))
            try:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, timeout=10
                )
                passed = result.returncode == 0
                results.append({
                    'artifact': str(code_file.relative_to(submission_dir)),
                    'check': 'syntax_valid',
                    'passed': passed,
                    'reason': None if passed else result.stderr[:200],
                })
            except subprocess.TimeoutExpired:
                results.append({
                    'artifact': str(code_file.relative_to(submission_dir)),
                    'check': 'syntax_valid',
                    'passed': False,
                    'reason': 'Syntax check timed out',
                })
    return results


def check_sources_cited(submission_dir):
    """Check that markdown files contain source citations."""
    results = []
    for md_file in Path(submission_dir).rglob('*.md'):
        content = md_file.read_text()
        # Look for common citation patterns: URLs, reference sections, footnotes
        has_urls = 'http://' in content or 'https://' in content
        has_references = any(
            heading in content.lower()
            for heading in ['## references', '## sources', '## citations', '## bibliography']
        )
        has_footnotes = '[^' in content or '(source:' in content.lower()

        has_citations = has_urls or has_references or has_footnotes
        results.append({
            'artifact': str(md_file.relative_to(submission_dir)),
            'check': 'sources_cited',
            'passed': has_citations,
            'reason': None if has_citations else 'No sources, URLs, or references found',
        })
    return results


def check_yaml_valid(submission_dir):
    """Check that any YAML files are valid."""
    results = []
    for yaml_file in Path(submission_dir).rglob('*.yaml'):
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            results.append({
                'artifact': str(yaml_file.relative_to(submission_dir)),
                'check': 'yaml_valid',
                'passed': True,
                'reason': None,
            })
        except yaml.YAMLError as e:
            results.append({
                'artifact': str(yaml_file.relative_to(submission_dir)),
                'check': 'yaml_valid',
                'passed': False,
                'reason': str(e)[:200],
            })
    return results


def run_automated_checks(submission_dir, module_path):
    """Run all Layer 1 checks on a submission."""
    # Load module to get required artifacts
    with open(module_path, 'r') as f:
        module = yaml.safe_load(f)

    required_artifacts = module.get('required_artifacts', [])
    riu_id = module.get('riu_id', 'UNKNOWN')

    print(f"Layer 1 Automated Checks — {riu_id}")
    print("=" * 50)

    all_results = []

    # Run checks
    print("\n1. Artifacts Present")
    artifact_results = check_artifacts_present(submission_dir, required_artifacts)
    all_results.extend(artifact_results)
    for r in artifact_results:
        status = "PASS" if r['passed'] else "FAIL"
        print(f"   [{status}] {r['artifact']}")
        if r['reason']:
            print(f"         {r['reason']}")

    print("\n2. Code Syntax Valid")
    code_results = check_code_runs(submission_dir)
    all_results.extend(code_results)
    if code_results:
        for r in code_results:
            status = "PASS" if r['passed'] else "FAIL"
            print(f"   [{status}] {r['artifact']}")
    else:
        print("   [SKIP] No code files found")

    print("\n3. Sources Cited")
    source_results = check_sources_cited(submission_dir)
    all_results.extend(source_results)
    if source_results:
        for r in source_results:
            status = "PASS" if r['passed'] else "FAIL"
            print(f"   [{status}] {r['artifact']}")
    else:
        print("   [SKIP] No markdown files found")

    print("\n4. YAML Valid")
    yaml_results = check_yaml_valid(submission_dir)
    all_results.extend(yaml_results)
    if yaml_results:
        for r in yaml_results:
            status = "PASS" if r['passed'] else "FAIL"
            print(f"   [{status}] {r['artifact']}")
    else:
        print("   [SKIP] No YAML files found")

    # Summary
    total = len(all_results)
    passed = sum(1 for r in all_results if r['passed'])
    failed = total - passed

    print(f"\n{'=' * 50}")
    overall = "PASS" if failed == 0 else "FAIL"
    print(f"LAYER 1 RESULT: {overall} ({passed}/{total} checks passed)")

    if overall == "FAIL":
        print("\nBlocking issues (must fix before Layer 2 evaluation):")
        for r in all_results:
            if not r['passed']:
                print(f"  - {r['artifact']}: {r['reason']}")

    return failed == 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: automated_checks.py <submission_dir> <module.yaml>")
        sys.exit(1)

    success = run_automated_checks(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
