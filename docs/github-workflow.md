# GitHub Workflow Guide

Guide for using GitHub and Claude Code agents with PandaForge.

## Repository Setup

**Repository:** https://github.com/lathrodectus/PandaForge
**Base:** BambuStudio v2.5.0.66
**Platform:** macOS (Apple Silicon and Intel)

### Git Remotes

```bash
origin    https://github.com/lathrodectus/PandaForge.git
upstream  https://github.com/bambulab/BambuStudio.git
```

- `origin` - Your fork (push your changes here)
- `upstream` - BambuStudio official repo (pull updates from here)

### Tracking Upstream Updates

```bash
# Fetch latest from BambuStudio
git fetch upstream

# View what's new
git log HEAD..upstream/master --oneline

# Merge updates (or cherry-pick specific commits)
git merge upstream/master
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Work with Claude Code agents (see Agent Strategy below)
# Make changes, test, iterate

# Commit changes
git add <files>
git commit -m "Add feature: description

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# Push to GitHub
git push origin feature/your-feature-name

# Create pull request
gh pr create --title "Add feature: description" \
  --body "## Summary
- What this PR does
- Why it's needed

## Testing
- How to test
- What was verified" \
  --label "klipper-integration"
```

### 2. Using Worktrees for Isolation

For experimental work or parallel development:

```bash
# In Claude Code
"work in a worktree to implement fan control"

# Claude creates isolated worktree
# Work completes

# Exit and keep changes
"exit worktree and keep changes"

# Push the worktree branch
git push origin cc-worktree-<name>

# Create PR from worktree branch
gh pr create --head cc-worktree-<name>
```

### 3. Bug Fixes

```bash
# Create fix branch
git checkout -b fix/issue-description

# Fix the bug
# Test thoroughly

# Commit and push
git commit -m "Fix: description of bug fix"
git push origin fix/issue-description

# Create PR with issue reference
gh pr create --title "Fix: description" \
  --body "Fixes #123" \
  --label "bug"
```

## Claude Code Agent Strategy

### When to Use Which Agent

| Task Type | Agent | Example |
|---|---|---|
| Find files/code | Explore | "Search for all Klipper UI components" |
| Understand architecture | Explore | "How does Moonraker API integration work?" |
| Plan implementation | Plan | "Plan implementation of fan control UI" |
| Complex multi-step | general-purpose | "Implement and test new preset selector" |
| Single file edit | Direct | Just edit the file directly |

### Agent Best Practices

**Explore Agents** - Fast codebase discovery
```
"Find all files related to Moonraker API"
"Search for pressure advance implementation"
"Locate profile conversion logic"
```

**Plan Agents** - Design before implementation
```
"Plan approach for adding Klipper fan control"
"Design profile converter UI integration"
```

**General-Purpose Agents** - Complex tasks
```
"Implement Moonraker temperature monitoring with error handling"
"Refactor BedPlateSelector to support custom bed types"
```

### Parallel Agent Execution

For independent tasks, run agents in parallel:
```
"Use explore agents to find:
1. Moonraker API call sites
2. Fan control UI components
3. Temperature monitoring code"
```

### Agent Delegation Guidelines

- **1 file change:** No agent needed
- **2-3 related files:** 1 Explore agent for context
- **Cross-cutting feature:** 2-3 Explore agents in parallel
- **Large refactor:** Plan agent first, then implement

## GitHub CLI Commands

### Repository Management

```bash
# View repository
gh repo view lathrodectus/PandaForge --web

# Edit repository settings
gh repo edit lathrodectus/PandaForge \
  --description "macOS-native fork of BambuStudio v2.5.0.66 for Klipper 3D printer users" \
  --add-topic "3d-printing,klipper,bambu-studio,macos,slicer"

# Enable features
gh repo edit lathrodectus/PandaForge --enable-issues --enable-wiki
```

### Issue Management

```bash
# Create issue
gh issue create \
  --title "Add Klipper fan control UI" \
  --label "klipper-integration,ui-component" \
  --body "## Description
Feature request details..."

# List issues
gh issue list --label "klipper-integration"

# View issue
gh issue view 123

# Close issue
gh issue close 123
```

### Pull Request Workflow

```bash
# Create PR
gh pr create \
  --title "Add feature X" \
  --body "Description" \
  --label "klipper-integration"

# List PRs
gh pr list

# View PR
gh pr view 123

# Check PR status
gh pr checks 123

# Merge PR
gh pr merge 123 --squash

# Review PR
gh pr review 123 --approve
gh pr review 123 --comment --body "Looks good!"
```

### Labels

Standard labels for issue/PR organization:

| Label | Color | Use For |
|---|---|---|
| `klipper-integration` | Green | Klipper-specific features |
| `moonraker-api` | Blue | Moonraker API integration |
| `profile-converter` | Yellow | Profile conversion system |
| `ui-component` | Orange | UI/UX components |
| `build-system` | Dark Blue | CMake, dependencies, build |
| `documentation` | Light Blue | Documentation improvements |

Create labels:
```bash
gh label create "klipper-integration" --color "0E8A16" --description "Klipper-specific features"
gh label create "moonraker-api" --color "1D76DB" --description "Moonraker API integration"
gh label create "profile-converter" --color "FBCA04" --description "Profile conversion system"
gh label create "ui-component" --color "D93F0B" --description "UI/UX components"
gh label create "build-system" --color "0052CC" --description "CMake, dependencies, build"
gh label create "documentation" --color "0075CA" --description "Documentation improvements"
```

## Branch Strategy

```
main                          # Stable releases
├── feature/klipper-ui        # Klipper UI components
├── feature/moonraker         # Moonraker integration
├── feature/profile-converter # Profile converter UI
├── fix/build-issue           # Bug fixes
└── cc-worktree-*             # Temporary worktree branches
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `cc-worktree-*` - Claude Code worktree branches (temporary)

## Commit Message Format

```
<type>: <short description>

<optional detailed description>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `refactor`, `docs`, `build`, `test`

Examples:
```
feat: Add Klipper fan control UI panel

Implements FanControlPanel with speed controls for part cooling,
auxiliary, and chamber fans. Integrates with Moonraker API.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

```
fix: Resolve pressure advance multi-extruder issue

GCodeWriter now correctly handles pressure advance for multi-extruder
setups by tracking per-extruder state.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

## CI/CD (Future)

Planned GitHub Actions workflows:

- **Build:** Automated macOS builds on push
- **Test:** Run test suite (when available)
- **Release:** Create release artifacts for distribution

## Quick Reference

```bash
# Daily workflow
git checkout -b feature/my-feature
# Work with Claude Code
git commit -m "feat: description"
git push origin feature/my-feature
gh pr create

# Update from upstream
git fetch upstream
git merge upstream/master

# Clean up merged branches
git branch --merged | grep -v main | xargs git branch -d
```

## Resources

- GitHub CLI docs: https://cli.github.com/manual/
- Git workflow: https://guides.github.com/introduction/flow/
- Claude Code docs: Run `/help` in Claude Code
