---
name: validation-suite
description: Validate implementation against spec requirements. Use when checking spec compliance, constitution adherence, token efficiency, cross-agent compatibility, performance targets, security best practices, and documentation completeness.
---

# Validation Suite

Validate implementation against spec requirements.

## Overview

Runs comprehensive validation checks on implemented features against specifications, constitution principles, and quality standards.

## Quick Start

```
/validation-suite --spec 1-agents-md-gen
/validation-suite --all
/validation-suite --category token-efficiency
```

## Validation Categories

```
✅ Spec Compliance      - All FRs implemented
✅ Constitution         - All principles followed
✅ Token Efficiency     - >80% savings achieved
✅ Cross-Agent          - Works on Claude Code + Goose
✅ Performance          - Meets SLA targets
✅ Security             - No hardcoded secrets
✅ Documentation        - All docs present
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations pass |
| 1 | Warnings (non-blocking) |
| 2 | Errors (blocking) |

## Validation Rules

### Spec Compliance
Check each FR in spec.md is implemented with working acceptance scenarios.

### Constitution
- MCP Code Execution: Data operations use scripts
- Progressive Disclosure: SKILL.md under 500 tokens
- Kubernetes-Native: Services have K8s manifests
- Security: No hardcoded secrets

### Token Efficiency
Skills using scripts must show >80% reduction vs direct MCP calls.

## Report Format

```
Validation Report: agents-md-gen
=====================================

✅ Spec Compliance         10/10 FRs implemented
✅ Constitution            8/8 principles followed
✅ Token Efficiency        95% savings (target: >80%)
⚠️  Performance            35s scan (target: <30s)

Result: PASS (1 warning)
```

## Scripts

Run `scripts/validate.py --spec <name>` or `scripts/validate.py --all`.
