# GitHub Repository Setup

## Variables (Settings → Secrets and variables → Actions)

### Repository Variables
| Name | Value | Purpose |
|------|-------|---------|
| `ZENODO_TOKEN` | `znzl0KL0jzAG...` | Zenodo API uploads |
| `PYTHON_VERSION` | `3.11` | CI/CD Python version |

### Repository Secrets (Set in GitHub UI)
- `ZENODO_TOKEN` - Your Zenodo API token
- `GH_TOKEN` - GitHub token for releases

## Environment Protection Rules
Set these in Settings → Environments:
- `production` → require review for tags
- `testing` → automatic on PRs

## Badges for README
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20072372.svg)](https://doi.org/10.5281/zenodo.20072372)
[![GitHub release](https://img.shields.io/github/v/release/esqet-architect/ESQET-Core)](https://github.com/esqet-architect/ESQET-Core/releases)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/esqet-architect/ESQET-Core/validate.yml)](https://github.com/esqet-architect/ESQET-Core/actions)
