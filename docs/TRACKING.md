# Project Tracking and Progress Management

This guide helps maintainers and project managers effectively track progress, manage milestones, and organize the project backlog.

## Table of Contents

- [Overview](#overview)
- [Creating Milestones](#creating-milestones)
- [Setting Priorities](#setting-priorities)
- [Linking PRs to Issues](#linking-prs-to-issues)
- [Project Boards](#project-boards)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## Overview

Effective project tracking ensures that:
- Team members understand priorities and deadlines
- Progress is visible and measurable
- Issues and PRs are properly organized
- Stakeholders can track project health
- Resources are allocated efficiently

---

## Creating Milestones

### What are Milestones?

Milestones represent significant project goals or releases. They group related issues and PRs together to track progress toward a specific objective.

### When to Create a Milestone

Create a milestone when:
- Planning a new version release (e.g., v2.1, v3.0)
- Starting a major feature development cycle
- Organizing a sprint or development phase
- Tracking a specific initiative or project goal

### How to Create a Milestone

**Via GitHub UI:**
1. Navigate to the repository
2. Click **Issues** → **Milestones** → **New Milestone**
3. Fill in the required information (see template below)
4. Click **Create Milestone**

**Via GitHub CLI:**
```bash
gh milestone create "v2.1 - Documentation & Examples" \
  --description "Complete comprehensive documentation for all features" \
  --due-date 2026-01-31
```

### Milestone Template

Use the [MILESTONES_TEMPLATE.md](../.github/MILESTONES_TEMPLATE.md) when creating new milestones. At minimum, include:

- **Title**: Clear, version-numbered or descriptive name
- **Description**: Overview of goals and scope
- **Due Date**: Target completion date
- **Acceptance Criteria**: What defines completion
- **Key Deliverables**: Main items to be completed

### Milestone Naming Conventions

Follow these patterns:

- **Version Releases**: `v2.1 - Documentation & Examples`
- **Feature Initiatives**: `Multi-Modal AI Support`
- **Sprint/Cycle**: `Q1 2026 Sprint 1`
- **Bug Fix Batch**: `Bug Fix Round - January 2026`

### Managing Milestones

**Updating Progress:**
- Regularly review and update milestone descriptions
- Close completed milestones promptly
- Adjust due dates when necessary (with justification)

**Closing Milestones:**
- Ensure all critical issues are resolved
- Document any deferred items
- Create follow-up milestones if needed
- Write a release summary or retrospective

---

## Setting Priorities

### Priority Labels

Use these standard priority labels on issues:

| Label | Description | Expected Response Time |
|-------|-------------|------------------------|
| `priority: critical` | Security issues, production bugs, system down | Immediate (< 24 hours) |
| `priority: high` | Important features, major bugs affecting users | 1-3 days |
| `priority: medium` | Standard features, moderate bugs | 1-2 weeks |
| `priority: low` | Nice-to-have features, minor improvements | As time permits |

### How to Prioritize Issues

**Criteria for Prioritization:**

1. **Impact**: How many users are affected?
2. **Urgency**: Is there a deadline or blocker?
3. **Effort**: How much work is required?
4. **Dependencies**: Are other issues blocked by this?
5. **Strategic Value**: Does it align with roadmap goals?

**Priority Matrix:**

```
High Impact + High Urgency = CRITICAL
High Impact + Low Urgency = HIGH
Low Impact + High Urgency = HIGH
Low Impact + Low Urgency = LOW/MEDIUM
```

### Assigning Priorities

**Via GitHub UI:**
1. Open the issue
2. Click **Labels** → Select appropriate `priority:` label
3. Add context in comments if priority changes

**Via GitHub CLI:**
```bash
gh issue edit 42 --add-label "priority: high"
```

### Priority Guidelines by Type

**Security Issues:**
- Always `priority: critical`
- Must be addressed immediately
- Consider private security advisory if needed

**Bug Fixes:**
- Critical bugs affecting production: `priority: critical`
- Bugs affecting core features: `priority: high`
- UI/UX issues: `priority: medium`
- Minor bugs: `priority: low`

**Features:**
- Roadmap features with deadlines: `priority: high`
- Community requested (10+ votes): `priority: medium`
- Nice-to-have enhancements: `priority: low`

**Documentation:**
- Missing critical docs: `priority: high`
- Unclear documentation: `priority: medium`
- Enhancement/examples: `priority: low`

---

## Linking PRs to Issues

### Why Link PRs to Issues?

- Provides context for code changes
- Automatically updates issue status
- Creates audit trail
- Enables better release notes
- Improves project tracking

### How to Link PRs to Issues

**Method 1: Using Keywords in PR Description**

Use closing keywords in the PR description or commit messages:

```markdown
Closes #123
Fixes #456
Resolves #789
```

**Other linking keywords:**
- `closes`, `closed`, `close`
- `fixes`, `fixed`, `fix`
- `resolves`, `resolved`, `resolve`

**Example PR Description:**
```markdown
## Description
Add email drafting tool with tone and length controls.

## Changes
- Implemented email drafter in `tools/email_drafter.py`
- Added endpoint `/ai/tools/email/draft`
- Created comprehensive tests

Closes #45
```

**Method 2: Using GitHub's UI**

1. Open the PR
2. In the right sidebar, click **Development**
3. Search for and select related issues
4. Click to link

**Method 3: Using GitHub CLI**

```bash
# Create PR with linked issue
gh pr create --title "Add email drafting tool" \
  --body "Closes #45" \
  --base main
```

### Best Practices for Linking

**Do:**
- ✅ Link PRs to issues before merging
- ✅ Use closing keywords for issues that will be fully resolved
- ✅ Link multiple issues if PR addresses multiple problems
- ✅ Reference related issues even if not fully resolving them

**Don't:**
- ❌ Use closing keywords for partial fixes (use "Related to #123" instead)
- ❌ Link unrelated issues just to close them
- ❌ Forget to link when the PR directly addresses an issue

**Example Scenarios:**

```markdown
# Full resolution
Closes #123

# Partial work
Related to #123 (implements phase 1)

# Multiple issues
Closes #45
Fixes #67
Related to #89
```

---

## Project Boards

### When to Use Project Boards

Use GitHub Project Boards for:
- Sprint planning and tracking
- Feature development workflows
- Roadmap visualization
- Bug triage processes
- Release planning

### Recommended Board Columns

**Basic Kanban:**
- 📋 Backlog
- 🔄 In Progress
- 👀 In Review
- ✅ Done

**Extended Workflow:**
- 📋 Backlog
- 🎯 Prioritized
- 🔄 In Progress
- 🧪 Testing
- 👀 In Review
- ✅ Done
- 🚫 Won't Fix

### Automation Rules

Set up automation to move cards:
- **To In Progress**: When PR is opened or issue is assigned
- **To In Review**: When PR is marked ready for review
- **To Done**: When issue is closed or PR is merged

### Project Board Best Practices

1. **Keep it Updated**: Move cards regularly (daily or on status change)
2. **Clear Card Titles**: Use descriptive issue/PR titles
3. **Add Context**: Use labels, assignees, and milestones
4. **Archive Completed**: Clean up Done column periodically
5. **Review Regularly**: Weekly review of Backlog and In Progress

---

## Best Practices

### Issue Management

**Creating Issues:**
- Use descriptive, searchable titles
- Provide clear problem description
- Include reproduction steps for bugs
- Add relevant labels (type, priority, area)
- Assign to milestone if applicable
- Add acceptance criteria for features

**Triaging Issues:**
- Review new issues daily
- Assign appropriate labels
- Set priority level
- Link related issues
- Assign to team member or milestone
- Close duplicates and invalid issues

**Closing Issues:**
- Verify the issue is fully resolved
- Link to resolving PR or commit
- Add closing comment explaining resolution
- Update documentation if needed

### Pull Request Management

**Creating PRs:**
- Write clear, descriptive titles
- Fill out PR template completely
- Link related issues
- Add appropriate labels
- Request reviews from relevant team members
- Keep PRs focused on single concern

**Reviewing PRs:**
- Review within 1-2 business days
- Provide constructive feedback
- Test changes when possible
- Approve when ready or request changes
- Re-review after changes

**Merging PRs:**
- Ensure all checks pass
- Confirm all review comments addressed
- Verify linked issues will close correctly
- Use squash merge for feature branches
- Delete branch after merge

### Milestone Management

**Planning Milestones:**
- Set realistic due dates
- Scope appropriately (not too large)
- Align with roadmap and releases
- Define clear acceptance criteria
- Communicate to team

**Tracking Milestones:**
- Monitor progress weekly
- Update descriptions as needed
- Communicate delays early
- Move non-critical items if falling behind
- Celebrate completion!

### Communication

**Status Updates:**
- Weekly milestone progress reports
- Blockers and dependencies highlighted
- Changes to priorities communicated
- Stakeholder updates for major milestones

**Documentation:**
- Keep ROADMAP.md updated
- Document decisions in issues
- Maintain CHANGELOG.md
- Update docs alongside code changes

---

## Examples

### Example 1: Feature Development Workflow

**Issue Creation:**
```markdown
Title: Add sentiment analysis tool
Labels: enhancement, priority: medium
Milestone: v2.1 - Documentation & Examples

## Description
Implement sentiment analysis tool to analyze text sentiment.

## Acceptance Criteria
- [ ] Sentiment endpoint implemented
- [ ] Returns sentiment score and emotions
- [ ] Tests with >80% coverage
- [ ] Documentation updated
```

**PR Creation:**
```markdown
Title: feat: add sentiment analysis tool

## Description
Implements sentiment analysis tool with emotion detection.

## Changes
- Added `tools/sentiment_analysis.py`
- Created endpoint `/ai/tools/sentiment`
- Added comprehensive test suite
- Updated API documentation

## Testing
- [x] All tests pass
- [x] Manual testing completed
- [x] API tested with curl and Postman

Closes #67
```

### Example 2: Bug Fix Workflow

**Issue:**
```markdown
Title: Session history memory leak in stateful conversations
Labels: bug, priority: high
Milestone: v2.0.1 - Bug Fixes

## Description
Memory usage increases over time due to session history not being cleaned up.

## Steps to Reproduce
1. Create multiple sessions
2. Send 100+ messages per session
3. Observe memory usage growth

## Expected Behavior
Old session data should be cleaned up after timeout.

## Current Behavior
Session data persists indefinitely.
```

**PR:**
```markdown
Title: fix: resolve session history memory leak

## Description
Implements automatic cleanup of expired session data.

## Changes
- Added session expiration logic (30 min timeout)
- Background cleanup task runs every 5 minutes
- Added session last_activity timestamp

## Testing
- Added memory leak regression test
- Verified cleanup runs correctly
- Tested with 1000+ sessions

Fixes #89
```

### Example 3: Milestone Example

**Milestone: v2.1 - Documentation & Examples**

**Description:**
Complete comprehensive documentation for all features and provide real-world examples.

**Due Date:** January 31, 2026

**Acceptance Criteria:**
- [ ] All API endpoints documented
- [ ] Platform integration guides completed
- [ ] 10+ code examples added
- [ ] Video tutorials created
- [ ] Quickstart guide updated

**Progress:** 12/20 issues closed (60%)

**Linked Issues:**
- #45: Add platform integration examples
- #67: Document sentiment analysis API
- #89: Create email drafting tutorial
- #102: Add video walkthrough
- #115: Update quickstart guide

---

## Resources

### GitHub Documentation
- [About Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [Linking PRs to Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
- [Managing Project Boards](https://docs.github.com/en/issues/organizing-your-work-with-project-boards)
- [Using Labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)

### Internal Documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [ROADMAP.md](../ROADMAP.md) - Feature roadmap
- [.github/MILESTONES_TEMPLATE.md](../.github/MILESTONES_TEMPLATE.md) - Milestone template

---

**Last Updated:** November 10, 2025  
**Maintainers:** Savrli AI Team
