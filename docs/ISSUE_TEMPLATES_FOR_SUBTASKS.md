# Issue Templates for Sub-Tasks

This document provides recommended issue templates for common task types in the Savrli AI project. Use these templates when creating sub-issues from the [ROADMAP.md](./ROADMAP.md) to ensure consistency and completeness.

---

## Table of Contents

- [Feature Request Template](#feature-request-template)
- [Bug Report Template](#bug-report-template)
- [Documentation Task Template](#documentation-task-template)
- [Chore/Maintenance Task Template](#choremaintenance-task-template)
- [Test Task Template](#test-task-template)
- [UI/UX Improvement Template](#uiux-improvement-template)
- [Performance Optimization Template](#performance-optimization-template)
- [Security Enhancement Template](#security-enhancement-template)
- [Labels Reference](#labels-reference)
- [Milestone Guidelines](#milestone-guidelines)

---

## Feature Request Template

Use this template for new feature development or enhancements.

```markdown
## Feature Description

**Feature**: [Brief one-line description]

[Provide a clear and detailed description of the feature. Include the user story or use case.]

**User Story**: As a [type of user], I want [goal] so that [benefit].

## Motivation

[Explain why this feature is needed. What problem does it solve? How does it improve the product?]

## Proposed Solution

[Describe the proposed implementation approach. Include technical details if applicable.]

### Technical Approach

- **Components affected**: [List files/modules that will be modified]
- **New dependencies**: [List any new libraries or tools needed]
- **API changes**: [Describe any new or modified endpoints]
- **Database changes**: [Describe any schema modifications]

## Acceptance Criteria

- [ ] [Specific, testable requirement 1]
- [ ] [Specific, testable requirement 2]
- [ ] [Specific, testable requirement 3]
- [ ] Documentation updated
- [ ] Tests written and passing
- [ ] Code reviewed and approved

## Design/Mockups

[Include or link to any wireframes, mockups, or design documents]

## Implementation Tasks

- [ ] [Specific sub-task 1]
- [ ] [Specific sub-task 2]
- [ ] [Specific sub-task 3]

## Dependencies

**Blocked by**: #[issue number]  
**Blocks**: #[issue number]  
**Related to**: #[issue number]

## Testing Plan

[Describe how this feature will be tested]

- **Unit tests**: [What unit tests are needed?]
- **Integration tests**: [What integration tests are needed?]
- **Manual testing**: [Steps for manual verification]

## Documentation Required

- [ ] API documentation
- [ ] User guide
- [ ] Code comments
- [ ] README updates

## Estimated Effort

**Story Points**: [1, 2, 3, 5, 8, 13]  
**Time Estimate**: [hours/days]

## Additional Context

[Any other relevant information, screenshots, links, or references]

---

**Labels**: `feature`, `[area]`, `[priority]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Bug Report Template

Use this template for reporting and tracking bugs.

```markdown
## Bug Description

**Summary**: [One-line description of the bug]

[Provide a clear and concise description of the bug]

## Environment

- **OS**: [e.g., macOS 13.0, Ubuntu 22.04, Windows 11]
- **Python Version**: [e.g., 3.11.0]
- **Browser** (if applicable): [e.g., Chrome 120, Firefox 121]
- **Deployment**: [local, staging, production]
- **Version/Commit**: [e.g., v2.0.0, commit abc123]

## Steps to Reproduce

1. [First step]
2. [Second step]
3. [Third step]
4. [And so on...]

## Expected Behavior

[Describe what you expected to happen]

## Actual Behavior

[Describe what actually happened]

## Screenshots/Logs

[If applicable, add screenshots or error logs to help explain the problem]

```
[Paste relevant logs here]
```

## Impact

**Severity**: [Critical / High / Medium / Low]

- **Critical**: Production down, data loss, security vulnerability
- **High**: Major functionality broken, affects many users
- **Medium**: Functionality impaired, workaround exists
- **Low**: Minor issue, cosmetic problem

**Affected Users**: [All users / Specific user group / Individual user]

## Possible Solution

[If you have suggestions on how to fix the bug, describe them here]

## Root Cause Analysis

[After investigation, document the root cause]

## Fix Verification

- [ ] Bug reproduced locally
- [ ] Fix implemented
- [ ] Unit tests added
- [ ] Regression tests added
- [ ] Manual testing completed
- [ ] Fix verified in staging
- [ ] Release notes updated

## Related Issues

**Duplicate of**: #[issue number]  
**Related to**: #[issue number]  
**Caused by**: #[issue number]

---

**Labels**: `bug`, `[severity]`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Documentation Task Template

Use this template for documentation improvements and additions.

```markdown
## Documentation Task

**Type**: [New documentation / Update / Fix / Reorganization]

**Document(s)**: [List the document(s) to be created or modified]

## Objective

[Explain what documentation needs to be created or improved and why]

## Target Audience

[Who will use this documentation? E.g., new developers, API users, system administrators]

## Content Outline

[Provide a structured outline of the content to be included]

1. **Section 1**: [Title]
   - Subsection 1.1
   - Subsection 1.2

2. **Section 2**: [Title]
   - Subsection 2.1
   - Subsection 2.2

3. **Section 3**: [Title]
   - Subsection 3.1

## Key Information to Include

- [ ] [Important point 1]
- [ ] [Important point 2]
- [ ] [Important point 3]
- [ ] Code examples
- [ ] Screenshots/diagrams
- [ ] Common pitfalls/troubleshooting

## Examples Required

[List specific examples that should be included]

1. **Example 1**: [Description]
2. **Example 2**: [Description]
3. **Example 3**: [Description]

## Related Documentation

**References**: [Links to related docs]  
**Updates Required**: [Other docs that need to be updated]

## Acceptance Criteria

- [ ] Content is accurate and up-to-date
- [ ] Examples are tested and working
- [ ] Formatting is consistent with existing docs
- [ ] Links are working
- [ ] Spelling and grammar checked
- [ ] Technical review completed
- [ ] Indexed/linked from appropriate places

## Review Process

- [ ] Self-review completed
- [ ] Peer review by [reviewer name]
- [ ] Technical accuracy verified
- [ ] User testing (if applicable)

---

**Labels**: `docs`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Chore/Maintenance Task Template

Use this template for maintenance tasks, refactoring, and technical debt.

```markdown
## Chore/Maintenance Task

**Type**: [Refactoring / Dependency Update / Configuration / Build/CI / Cleanup]

**Summary**: [One-line description of the task]

## Objective

[Explain what needs to be done and why it's important]

## Current State

[Describe the current situation or problem]

## Desired State

[Describe the desired outcome after completion]

## Implementation Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Affected Areas

- **Files/Modules**: [List affected components]
- **Dependencies**: [List any dependency changes]
- **Configuration**: [List any config changes]
- **Build/Deploy**: [Describe any build/deployment impacts]

## Risks & Mitigation

**Potential Risks**:
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]

## Breaking Changes

[Describe any breaking changes and migration path]

- [ ] No breaking changes
- [ ] Breaking changes documented
- [ ] Migration guide provided
- [ ] Deprecation warnings added

## Testing Strategy

- [ ] Existing tests still pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed
- [ ] Regression testing performed

## Acceptance Criteria

- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Verification Steps

1. [How to verify the change]
2. [What to check]
3. [Expected results]

---

**Labels**: `chore`, `[type]`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Test Task Template

Use this template for adding or improving tests.

```markdown
## Test Task

**Type**: [Unit Tests / Integration Tests / E2E Tests / Performance Tests]

**Coverage Target**: [e.g., Increase coverage from 75% to 85%]

## Objective

[Explain what needs to be tested and why]

## Components Under Test

- [Component 1]
- [Component 2]
- [Component 3]

## Test Scenarios

### Happy Path Tests

1. **Scenario**: [Description]
   - **Given**: [Initial state]
   - **When**: [Action]
   - **Then**: [Expected result]

2. **Scenario**: [Description]
   - **Given**: [Initial state]
   - **When**: [Action]
   - **Then**: [Expected result]

### Edge Case Tests

1. **Scenario**: [Description]
   - **Given**: [Initial state]
   - **When**: [Action]
   - **Then**: [Expected result]

### Error Handling Tests

1. **Scenario**: [Description]
   - **Given**: [Initial state]
   - **When**: [Action]
   - **Then**: [Expected result]

## Test Data Requirements

[Describe any test data, fixtures, or mocks needed]

## Implementation Tasks

- [ ] Set up test fixtures/mocks
- [ ] Write test cases
- [ ] Verify tests pass
- [ ] Update test documentation
- [ ] Add tests to CI pipeline

## Coverage Analysis

**Current Coverage**: [percentage]  
**Target Coverage**: [percentage]  
**Files to Cover**: [list files]

## Acceptance Criteria

- [ ] All test scenarios implemented
- [ ] Tests pass consistently
- [ ] Code coverage meets target
- [ ] Tests run in CI/CD
- [ ] No flaky tests
- [ ] Test documentation updated

## Tools & Frameworks

- **Testing Framework**: [e.g., pytest]
- **Mocking**: [e.g., unittest.mock]
- **Coverage Tool**: [e.g., pytest-cov]
- **Other Tools**: [list any other tools]

---

**Labels**: `test`, `[type]`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## UI/UX Improvement Template

Use this template for user interface and user experience enhancements.

```markdown
## UI/UX Improvement

**Type**: [New UI Component / UI Enhancement / UX Flow / Accessibility]

**Summary**: [One-line description of the improvement]

## User Problem

[Describe the user pain point or need this addresses]

**User Story**: As a [type of user], I want [goal] so that [benefit].

## Current Experience

[Describe the current UI/UX and its limitations]

## Proposed Improvement

[Describe the proposed UI/UX change]

## Design

### Visual Design

[Include or link to mockups, wireframes, or design files]

- **Figma/Sketch Link**: [link]
- **Color Palette**: [colors]
- **Typography**: [fonts and sizes]
- **Spacing**: [spacing guidelines]

### Interaction Design

[Describe the user interaction flow]

1. User [action]
2. System [response]
3. User [next action]

### Responsive Behavior

- **Desktop**: [How it appears/behaves on desktop]
- **Tablet**: [How it appears/behaves on tablet]
- **Mobile**: [How it appears/behaves on mobile]

## Accessibility Requirements

- [ ] Keyboard navigation support
- [ ] Screen reader compatible
- [ ] WCAG 2.1 Level AA compliant
- [ ] Proper color contrast
- [ ] ARIA labels where appropriate
- [ ] Focus indicators visible

## Implementation Details

**Components to Modify**: [list components]  
**New Components**: [list new components]  
**CSS/Styling Changes**: [describe styling changes]  
**JavaScript/Logic**: [describe any interactive behavior]

## Browser Compatibility

- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Edge (latest 2 versions)
- [ ] Mobile browsers (iOS Safari, Chrome Android)

## Performance Considerations

- [ ] Images optimized
- [ ] CSS/JS minified
- [ ] Lazy loading implemented (if applicable)
- [ ] Animation performance verified

## Acceptance Criteria

- [ ] Design implementation matches mockups
- [ ] Responsive on all screen sizes
- [ ] Accessible to keyboard users
- [ ] Screen reader compatible
- [ ] Browser compatibility verified
- [ ] Performance benchmarks met
- [ ] User testing completed (if applicable)

## Testing Plan

- **Visual Testing**: [How to verify visual accuracy]
- **Functional Testing**: [How to test interactions]
- **Accessibility Testing**: [Tools and methods]
- **User Testing**: [If applicable, describe user testing plan]

---

**Labels**: `ui`, `ux`, `enhancement`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Performance Optimization Template

Use this template for performance improvement tasks.

```markdown
## Performance Optimization

**Type**: [Backend / Frontend / Database / Network / Memory]

**Summary**: [One-line description of the optimization]

## Performance Issue

[Describe the current performance problem]

### Metrics

**Current Performance**:
- [Metric 1]: [current value]
- [Metric 2]: [current value]
- [Metric 3]: [current value]

**Target Performance**:
- [Metric 1]: [target value]
- [Metric 2]: [target value]
- [Metric 3]: [target value]

## Impact

- **User Impact**: [How does this affect users?]
- **System Impact**: [How does this affect the system?]
- **Severity**: [High / Medium / Low]

## Root Cause

[Describe the root cause of the performance issue]

**Analysis**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Proposed Solution

[Describe the optimization strategy]

### Technical Approach

1. [Optimization technique 1]
2. [Optimization technique 2]
3. [Optimization technique 3]

### Trade-offs

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Costs/Risks**:
- [Cost/Risk 1]
- [Cost/Risk 2]

## Implementation Plan

- [ ] Benchmark current performance
- [ ] Implement optimization
- [ ] Benchmark optimized performance
- [ ] Compare results
- [ ] Document findings

## Benchmarking

**Benchmarking Tools**: [e.g., Apache Bench, pytest-benchmark, Chrome DevTools]

**Test Scenarios**:
1. [Scenario 1 description]
2. [Scenario 2 description]
3. [Scenario 3 description]

## Acceptance Criteria

- [ ] Target performance metrics achieved
- [ ] No functionality regressions
- [ ] Tests pass
- [ ] Benchmarks documented
- [ ] Code reviewed

## Monitoring

[How will performance be monitored after deployment?]

- **Metrics to Track**: [list metrics]
- **Alerting**: [describe alerts]
- **Dashboard**: [link to dashboard]

## Rollback Plan

[Describe how to rollback if the optimization causes issues]

---

**Labels**: `perf`, `optimization`, `[area]`  
**Milestone**: [version number]  
**Assignee**: [username or unassigned]
```

---

## Security Enhancement Template

Use this template for security improvements and fixes.

```markdown
## Security Enhancement

**Type**: [Vulnerability Fix / Security Feature / Security Audit / Compliance]

**Severity**: [Critical / High / Medium / Low]

⚠️ **Note**: Do not include sensitive security details in public issues. Coordinate with maintainers for vulnerability disclosure.

## Security Issue

[Describe the security concern or enhancement - avoid sensitive details in public issues]

## Impact Assessment

**Affected Components**: [List affected components]  
**Attack Vector**: [How could this be exploited?]  
**Affected Users**: [Who is impacted?]  
**Data at Risk**: [What data could be compromised?]

## Risk Score

**Likelihood**: [High / Medium / Low]  
**Impact**: [High / Medium / Low]  
**Overall Risk**: [Critical / High / Medium / Low]

## Proposed Solution

[Describe the security enhancement or fix]

### Security Measures

1. [Security measure 1]
2. [Security measure 2]
3. [Security measure 3]

## Implementation Plan

- [ ] Review security best practices
- [ ] Implement security fix/enhancement
- [ ] Security testing
- [ ] Code review with security focus
- [ ] Document security changes

## Testing Strategy

- [ ] Penetration testing
- [ ] Security scan (e.g., OWASP ZAP, Bandit)
- [ ] Dependency vulnerability scan
- [ ] Manual security review
- [ ] Verify fix effectiveness

## Compliance

[If applicable, list compliance requirements]

- [ ] GDPR compliance
- [ ] SOC 2 compliance
- [ ] HIPAA compliance (if applicable)
- [ ] Other: [specify]

## Acceptance Criteria

- [ ] Security issue resolved
- [ ] No new vulnerabilities introduced
- [ ] Security tests pass
- [ ] Security documentation updated
- [ ] Compliance requirements met

## Disclosure Timeline

[For vulnerabilities - coordinate with maintainers]

- **Reported**: [date]
- **Fix Developed**: [target date]
- **Fix Released**: [target date]
- **Public Disclosure**: [target date, typically 90 days after fix]

## References

- **CVE**: [if applicable]
- **Security Advisories**: [links]
- **Best Practices**: [links to relevant security documentation]

---

**Labels**: `security`, `[severity]`  
**Milestone**: [version number]  
**Assignee**: [username - keep private for vulnerabilities]
```

---

## Labels Reference

### Label Categories

#### Type Labels
- `feature` - New feature or enhancement
- `bug` - Bug or defect
- `docs` - Documentation changes
- `test` - Testing improvements
- `chore` - Maintenance tasks
- `enhancement` - Improvements to existing features
- `refactor` - Code refactoring

#### Area Labels
- `ui` - User interface
- `backend` - Backend/API
- `mobile` - Mobile applications
- `security` - Security-related
- `perf` - Performance-related
- `integration` - Third-party integrations
- `ci/cd` - CI/CD pipeline

#### Priority Labels
- `priority:critical` - Must be done immediately
- `priority:high` - Should be done soon
- `priority:medium` - Normal priority
- `priority:low` - Nice to have

#### Status Labels
- `blocked` - Blocked by another issue
- `in-progress` - Currently being worked on
- `needs-review` - Awaiting review
- `needs-testing` - Awaiting testing
- `ready` - Ready to be picked up

#### Difficulty Labels
- `good-first-issue` - Good for newcomers
- `help-wanted` - Seeking community help
- `expert-needed` - Requires domain expertise

#### Special Labels
- `breaking-change` - Introduces breaking changes
- `wontfix` - Will not be fixed
- `duplicate` - Duplicate of another issue
- `invalid` - Invalid issue

---

## Milestone Guidelines

### Milestone Naming Convention

Use semantic versioning: `v[MAJOR].[MINOR].[PATCH] - [NAME]`

Examples:
- `v2.2 - Enhanced UI`
- `v3.0 - Analytics`
- `v3.1 - Model Operations`

### Milestone Planning

**Short-term Milestones** (1-2 months):
- Clear, achievable goals
- 5-15 issues
- Focused on specific theme

**Long-term Milestones** (3-6 months):
- Larger initiatives
- 15-30 issues
- Multiple related features

### Milestone Fields

- **Title**: Version number and descriptive name
- **Description**: Goals and scope
- **Due Date**: Target release date
- **Issues**: Link all related issues

---

## Tips for Writing Good Issues

### Best Practices

1. **Be Specific**: Provide clear, detailed descriptions
2. **Use Templates**: Start with the appropriate template
3. **Add Context**: Include relevant background information
4. **Include Examples**: Code snippets, screenshots, mockups
5. **Define Success**: Clear acceptance criteria
6. **Link Related Issues**: Reference dependencies and related work
7. **Label Appropriately**: Use relevant labels for filtering
8. **Set Priorities**: Help maintainers prioritize work
9. **Update Regularly**: Keep issue status current

### Common Mistakes to Avoid

- ❌ Vague descriptions
- ❌ Missing acceptance criteria
- ❌ No labels or wrong labels
- ❌ Combining multiple unrelated tasks
- ❌ Missing technical details
- ❌ Not linking to related issues
- ❌ Outdated information

### Issue Lifecycle

1. **New**: Issue created
2. **Triaged**: Reviewed and labeled
3. **Assigned**: Developer assigned
4. **In Progress**: Work started
5. **In Review**: Pull request open
6. **Testing**: Being tested
7. **Done**: Merged and released
8. **Closed**: Completed or won't fix

---

**Last Updated**: November 10, 2025

For questions about issue templates, please refer to [CONTRIBUTING.md](../CONTRIBUTING.md) or open a discussion.
