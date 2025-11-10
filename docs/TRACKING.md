# Project Tracking Guide

This guide helps maintainers and contributors effectively manage project progress using GitHub's built-in tracking features.

## Table of Contents

- [Overview](#overview)
- [Creating Milestones](#creating-milestones)
- [Setting Priorities](#setting-priorities)
- [Linking PRs to Issues](#linking-prs-to-issues)
- [Best Practices](#best-practices)
- [Workflow Examples](#workflow-examples)

---

## Overview

Effective project tracking helps:
- 📊 Visualize progress toward goals
- 🎯 Prioritize work and allocate resources
- 🔗 Connect related work items
- 📈 Measure team velocity
- 🗓️ Plan releases and sprints

### Key Concepts

**Milestones**: Time-bound collections of issues and PRs representing a specific goal or release
**Priorities**: Labels indicating the importance and urgency of work items
**Linking**: Connecting PRs to issues they resolve for automatic tracking

---

## Creating Milestones

### When to Create a Milestone

Create milestones for:
- 🚀 **Product releases** (e.g., "Version 2.1 Release")
- 📅 **Time-bound initiatives** (e.g., "Q4 2025 Documentation Sprint")
- 🎯 **Feature sets** (e.g., "Advanced Analytics Features")
- 🐛 **Bug fix batches** (e.g., "Critical Bug Fixes - November")

### How to Create a Milestone

#### Via GitHub Web Interface

1. Navigate to the repository
2. Click **Issues** or **Pull Requests** tab
3. Click **Milestones** button
4. Click **New Milestone**
5. Fill in the details:
   - **Title**: Clear, descriptive name
   - **Due Date**: Target completion date (optional but recommended)
   - **Description**: Use the [Milestone Template](../.github/MILESTONES_TEMPLATE.md)
6. Click **Create Milestone**

#### Via GitHub CLI

```bash
# Create a milestone
gh milestone create "Version 2.1" \
  --description "Documentation and polish release" \
  --due-date "2026-01-31"

# List all milestones
gh milestone list

# View milestone details
gh milestone view "Version 2.1"
```

### Milestone Naming Conventions

Use clear, consistent naming:

**Release Milestones:**
- Format: `Version X.Y` or `vX.Y.Z`
- Examples: `Version 2.1`, `v2.1.0`, `v2.1.0-beta`

**Sprint/Time-based Milestones:**
- Format: `[Time Period] [Focus Area]`
- Examples: `Q4 2025 Documentation`, `November Bug Fixes`, `2026 Q1 Planning`

**Feature Milestones:**
- Format: `[Feature Name] Implementation`
- Examples: `Analytics Dashboard`, `Mobile App MVP`, `API v2 Migration`

### Milestone Description Template

Use the template in [.github/MILESTONES_TEMPLATE.md](../.github/MILESTONES_TEMPLATE.md) when creating milestones. This ensures consistency and completeness.

**Key sections to include:**
- **Objective**: What are we trying to achieve?
- **Scope**: What's included and excluded?
- **Acceptance Criteria**: How do we know when it's done?
- **Dependencies**: What must be completed first?
- **Key Deliverables**: Main outputs expected

---

## Setting Priorities

### Priority Label System

Use GitHub labels to indicate priority levels:

#### Priority Labels

| Label | Description | Use Case |
|-------|-------------|----------|
| `priority: critical` 🔴 | Immediate attention required | Security vulnerabilities, production outages, data loss bugs |
| `priority: high` 🟠 | Should be addressed soon | Major bugs, important features, blocking issues |
| `priority: medium` 🟡 | Normal priority | Standard features, minor bugs, improvements |
| `priority: low` 🟢 | Nice to have | Small enhancements, documentation, refactoring |

#### Creating Priority Labels

```bash
# Via GitHub CLI
gh label create "priority: critical" --color "d73a4a" --description "Immediate attention required"
gh label create "priority: high" --color "ff9800" --description "Should be addressed soon"
gh label create "priority: medium" --color "ffd700" --description "Normal priority"
gh label create "priority: low" --color "28a745" --description "Nice to have"
```

### How to Set Priorities

#### During Issue Creation

1. Create or open an issue
2. Click **Labels** in the right sidebar
3. Select appropriate priority label
4. Optionally add other labels (type, area, etc.)

#### During Triage

Weekly triage process:
1. Review new issues without priority labels
2. Assess urgency and impact
3. Apply priority labels
4. Add to appropriate milestone if applicable
5. Assign to team member if ready to work

#### Priority Matrix

Use this matrix to determine priority:

```
Impact vs. Urgency Matrix:

High Impact + High Urgency = Priority: Critical 🔴
High Impact + Low Urgency  = Priority: High 🟠
Low Impact  + High Urgency = Priority: Medium 🟡
Low Impact  + Low Urgency  = Priority: Low 🟢
```

### Additional Labels for Context

Combine priority with other labels for better organization:

**Type Labels:**
- `type: bug` - Something isn't working
- `type: feature` - New functionality
- `type: docs` - Documentation improvements
- `type: enhancement` - Improvements to existing features

**Area Labels:**
- `area: api` - API-related work
- `area: integrations` - Platform integrations
- `area: ui` - User interface
- `area: testing` - Testing infrastructure

**Status Labels:**
- `status: blocked` - Waiting on dependencies
- `status: in-progress` - Currently being worked on
- `status: needs-review` - Ready for review
- `status: help-wanted` - Looking for contributors

---

## Linking PRs to Issues

### Why Link PRs to Issues?

Benefits of linking:
- ✅ Automatic issue closure when PR merges
- 📊 Visual progress tracking in milestones
- 🔗 Easy navigation between related work
- 📝 Better documentation of changes
- 🤖 Automated changelog generation

### Linking Methods

#### Method 1: Commit Messages (Recommended)

Use keywords in commit messages:

```bash
# Auto-close issue when merged
git commit -m "fix: resolve session history leak

Fixes #123"

# Reference without closing
git commit -m "feat: add temperature validation

Related to #456"
```

**Closing Keywords:**
- `Fixes #123`
- `Closes #123`
- `Resolves #123`
- `Fix #123`
- `Close #123`
- `Resolve #123`

**Referencing Keywords:**
- `Related to #123`
- `See #123`
- `Ref #123`
- `Part of #123`

#### Method 2: PR Description

Add keywords in the PR description:

```markdown
## Description
Add temperature validation to chat endpoint

## Related Issues
Closes #123
Fixes #456
Related to #789
```

#### Method 3: GitHub Web Interface

1. Open the PR
2. In the right sidebar, find **Development**
3. Click **Link an issue from this repository**
4. Search for and select the issue
5. Choose whether to auto-close on merge

#### Method 4: GitHub CLI

```bash
# Create PR with linked issue
gh pr create --title "fix: resolve memory leak" \
  --body "Closes #123" \
  --milestone "Version 2.1"

# Link issue to existing PR
gh pr edit 456 --body "Closes #123"
```

### Linking Multiple Issues

Link multiple issues when appropriate:

```markdown
## Related Issues
Closes #123 - Main issue
Closes #456 - Related bug
Related to #789 - Future enhancement
```

### Cross-Repository Linking

Link issues from other repositories:

```markdown
Closes Savrli-Inc/Savrli-Backend#123
Related to Savrli-Inc/Savrli-Docs#456
```

---

## Best Practices

### Milestone Management

**Do's:**
- ✅ Create milestones before starting work
- ✅ Add clear descriptions using the template
- ✅ Set realistic due dates
- ✅ Review progress weekly
- ✅ Close milestones when complete
- ✅ Keep milestone scope focused (aim for 10-20 issues)

**Don'ts:**
- ❌ Create too many overlapping milestones
- ❌ Let milestones drift indefinitely
- ❌ Add issues to milestones without review
- ❌ Skip the milestone description
- ❌ Forget to update milestone progress

### Priority Management

**Do's:**
- ✅ Review priorities regularly (weekly)
- ✅ Adjust priorities as situations change
- ✅ Limit critical items (should be <5% of backlog)
- ✅ Explain priority in issue comments
- ✅ Balance quick wins with important work

**Don'ts:**
- ❌ Mark everything as high priority
- ❌ Ignore critical issues
- ❌ Set priorities without context
- ❌ Let priority labels become stale
- ❌ Skip priority on new issues

### Linking Best Practices

**Do's:**
- ✅ Link PRs to issues whenever possible
- ✅ Use clear, descriptive commit messages
- ✅ Reference related work for context
- ✅ Update links if scope changes
- ✅ Verify auto-close behavior

**Don'ts:**
- ❌ Close issues prematurely
- ❌ Link unrelated PRs and issues
- ❌ Forget to link when working on issues
- ❌ Use only issue numbers without context
- ❌ Create PRs without issue discussion first

### Communication

**Keep stakeholders informed:**
- 📊 Share milestone progress in stand-ups
- 📝 Update issue comments with status
- 🔔 Notify when priorities change
- 📅 Communicate due date changes early
- 🎯 Celebrate milestone completions

---

## Workflow Examples

### Example 1: Feature Development

**Scenario:** Implementing a new analytics dashboard

```bash
# 1. Create milestone
gh milestone create "Analytics Dashboard" \
  --description "See .github/MILESTONES_TEMPLATE.md" \
  --due-date "2026-02-28"

# 2. Create issue with priority and milestone
gh issue create --title "Analytics Dashboard - Backend API" \
  --body "Implement analytics data endpoints" \
  --label "type: feature,priority: high,area: api" \
  --milestone "Analytics Dashboard"

# 3. Create feature branch
git checkout -b feature/analytics-api

# 4. Make changes and commit
git commit -m "feat: add analytics endpoints

Implements data collection and aggregation for dashboard.

Closes #234"

# 5. Create PR
gh pr create --title "feat: add analytics endpoints" \
  --body "Closes #234" \
  --milestone "Analytics Dashboard"

# 6. After merge, verify issue is closed and milestone updated
gh milestone view "Analytics Dashboard"
```

### Example 2: Bug Fix Sprint

**Scenario:** Addressing critical bugs before release

```bash
# 1. Create time-bound milestone
gh milestone create "November Critical Bugs" \
  --due-date "2025-11-30"

# 2. Triage and prioritize bugs
gh issue list --label "type: bug" --state open
# Add "priority: critical" to urgent bugs
# Add to "November Critical Bugs" milestone

# 3. Work on highest priority items first
# Each PR should close its linked issue

# 4. Monitor progress
gh milestone view "November Critical Bugs"

# 5. Close milestone when all issues resolved
gh milestone close "November Critical Bugs"
```

### Example 3: Documentation Sprint

**Scenario:** Q4 documentation improvements

```bash
# 1. Create documentation milestone
gh milestone create "Q4 2025 Documentation" \
  --description "Comprehensive documentation update" \
  --due-date "2025-12-31"

# 2. Break down into issues
gh issue create --title "Update API documentation" \
  --label "type: docs,priority: high" \
  --milestone "Q4 2025 Documentation"

gh issue create --title "Add integration examples" \
  --label "type: docs,priority: medium" \
  --milestone "Q4 2025 Documentation"

# 3. Create PRs that reference issues
# Each documentation PR: "Closes #XXX"

# 4. Track completion percentage
gh milestone view "Q4 2025 Documentation"
```

### Example 4: Handling Urgent Issues

**Scenario:** Critical security vulnerability discovered

```bash
# 1. Create issue with critical priority
gh issue create --title "SECURITY: SQL injection in user input" \
  --body "Vulnerability details..." \
  --label "type: bug,priority: critical,security" \
  --assignee @security-team

# 2. Create hotfix branch immediately
git checkout -b hotfix/sql-injection

# 3. Fix and commit
git commit -m "fix: sanitize user input to prevent SQL injection

Critical security fix for input validation.

Fixes #345"

# 4. Create PR for immediate review
gh pr create --title "SECURITY: Fix SQL injection vulnerability" \
  --body "Closes #345

URGENT: Please review immediately" \
  --reviewer @security-team,@tech-lead

# 5. Fast-track review and merge
# 6. Tag release and notify users
```

---

## Tracking Dashboard

### Viewing Project Progress

**GitHub Project Boards:**
Create a project board to visualize work:
1. Go to repository **Projects** tab
2. Create new project (Board or Table view)
3. Add milestones and issues
4. Organize by status columns
5. Track progress visually

**Milestone View:**
```bash
# List all milestones with progress
gh milestone list

# View specific milestone details
gh milestone view "Version 2.1"

# See issues in milestone
gh issue list --milestone "Version 2.1"
```

**Priority View:**
```bash
# List critical issues
gh issue list --label "priority: critical"

# List high-priority issues in specific milestone
gh issue list --label "priority: high" --milestone "Version 2.1"
```

### Metrics to Track

**Milestone Health:**
- Completion percentage
- Days until due date
- Open vs. closed issues
- Blocked items count

**Priority Distribution:**
- Critical issues count (should be low)
- High priority backlog size
- Medium/low priority ratio
- Overdue high-priority items

**Link Coverage:**
- PRs without linked issues
- Issues without PRs
- Average time from issue to PR
- Auto-close success rate

---

## Tools and Automation

### GitHub CLI Scripts

**Daily standup report:**
```bash
#!/bin/bash
echo "=== Today's Priority Items ==="
gh issue list --label "priority: critical,priority: high" \
  --assignee @me --state open

echo -e "\n=== In Progress PRs ==="
gh pr list --author @me --state open
```

**Milestone progress report:**
```bash
#!/bin/bash
MILESTONE="Version 2.1"
echo "=== $MILESTONE Progress ==="
gh milestone view "$MILESTONE"

echo -e "\n=== Blocked Items ==="
gh issue list --milestone "$MILESTONE" --label "status: blocked"

echo -e "\n=== Ready for Review ==="
gh pr list --milestone "$MILESTONE" --label "status: needs-review"
```

### Automation Ideas

**GitHub Actions:**
- Auto-label issues based on content
- Remind about stale milestones
- Post milestone progress to Slack
- Auto-close issues with merged PRs
- Validate PR descriptions have issue links

**Example: Remind about approaching milestone due dates**
```yaml
name: Milestone Due Date Reminder
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM

jobs:
  check-milestones:
    runs-on: ubuntu-latest
    steps:
      - name: Check due dates
        run: |
          # Script to check milestones due in next 7 days
          # Post to Slack/email if found
```

---

## Additional Resources

### GitHub Documentation
- [About Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [Linking PRs to Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
- [Using Labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [GitHub CLI](https://cli.github.com/manual/)

### Related Documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [.github/MILESTONES_TEMPLATE.md](../.github/MILESTONES_TEMPLATE.md) - Milestone template
- [ROADMAP.md](../ROADMAP.md) - Product roadmap

---

## Questions or Feedback?

- 💬 **Discussions**: [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- 🐛 **Issues**: [Report a problem](https://github.com/Savrli-Inc/Savrli-AI/issues)
- 📖 **Docs**: [Full Documentation](../README.md)

---

**Last Updated:** November 10, 2025
