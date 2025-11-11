# Priority Guidelines for Savrli AI

This document provides guidance for triaging, prioritizing, and managing features, bugs, and enhancement requests in the Savrli AI platform.

---

## Table of Contents

1. [Priority Levels](#priority-levels)
2. [Triaging Process](#triaging-process)
3. [Priority Assignment Criteria](#priority-assignment-criteria)
4. [Feature Request Evaluation](#feature-request-evaluation)
5. [Bug Severity Classification](#bug-severity-classification)
6. [Examples](#examples)
7. [Decision Framework](#decision-framework)
8. [Escalation Process](#escalation-process)

---

## Priority Levels

### High Priority

**Definition:** Critical functionality, security vulnerabilities, or features that are essential for core platform operations.

**Characteristics:**
- Affects core AI capabilities or platform stability
- Impacts security or data integrity
- Blocks other critical work or user workflows
- Requested by 10+ users or customers
- Required for upcoming release or commitment

**SLA:**
- Response time: Within 24 hours
- Resolution target: 1-2 weeks
- Review frequency: Daily

**Examples:**
- Security vulnerabilities in authentication or API endpoints
- Critical bugs in conversation management or model selection
- Core AI processing failures (multimodal, resource management)
- Platform integration outages affecting production users
- Performance degradation affecting all users

---

### Medium Priority

**Definition:** Important enhancements, new integrations, and non-critical improvements that add significant value.

**Characteristics:**
- Enhances existing functionality
- Adds new platform integrations
- Improves user experience or developer experience
- Requested by 5-10 users
- Nice-to-have for upcoming release

**SLA:**
- Response time: Within 72 hours
- Resolution target: 2-4 weeks
- Review frequency: Weekly

**Examples:**
- New platform integration (e.g., MS Teams, Telegram)
- UI/UX improvements to dashboard
- Documentation updates and enhancements
- Performance optimizations for specific endpoints
- New AI tool additions (beyond core tools)

---

### Low Priority

**Definition:** Nice-to-have features, experimental functionality, and minor enhancements.

**Characteristics:**
- Does not impact core functionality
- Experimental or exploratory feature
- Individual user request (<5 votes)
- Can be deferred without significant impact
- Refinement or polish items

**SLA:**
- Response time: Within 1 week
- Resolution target: 4-8 weeks or backlog
- Review frequency: Monthly

**Examples:**
- Cosmetic UI changes
- Additional export format options
- Experimental AI features
- Minor refactoring tasks
- Documentation formatting improvements

---

## Triaging Process

### Step 1: Initial Assessment

When a new issue, bug report, or feature request is submitted:

1. **Verify completeness**: Ensure sufficient information is provided
   - Description is clear and detailed
   - Reproduction steps (for bugs) or use case (for features) provided
   - Expected vs. actual behavior documented

2. **Categorize the item**:
   - Bug (something is broken)
   - Feature Request (new functionality)
   - Enhancement (improvement to existing functionality)
   - Documentation (docs update or addition)
   - Security (vulnerability or security concern)
   - Performance (speed or efficiency issue)

3. **Add appropriate labels**:
   - Type labels: `bug`, `feature`, `enhancement`, `documentation`, `security`, `performance`
   - Component labels: `multimodal`, `resource-management`, `integrations`, `api`, `dashboard`, `tools`
   - Status labels: `needs-triage`, `triaged`, `in-progress`, `blocked`

### Step 2: Impact Analysis

Assess the impact across multiple dimensions:

**User Impact:**
- How many users are affected?
- Is there a workaround available?
- Does it prevent users from accomplishing their goals?

**System Impact:**
- Does it affect system stability or reliability?
- Could it lead to data loss or corruption?
- Does it create security risks?

**Business Impact:**
- Does it affect key customers or revenue?
- Is it blocking a committed deliverable?
- Does it impact competitive positioning?

### Step 3: Effort Estimation

Estimate the effort required:

- **Small**: < 1 day (1-8 hours)
- **Medium**: 1-3 days (8-24 hours)
- **Large**: 1-2 weeks (40-80 hours)
- **Extra Large**: > 2 weeks (80+ hours)

Consider:
- Code complexity
- Testing requirements
- Documentation needs
- Dependencies on other work
- Risk of introducing new issues

### Step 4: Priority Assignment

Use the [Decision Framework](#decision-framework) to assign priority based on:
- Impact (High/Medium/Low)
- Effort (Small/Medium/Large/XL)
- Strategic alignment
- Dependencies

### Step 5: Assignment and Scheduling

1. Add to appropriate milestone or sprint
2. Assign owner if priority is High or Medium
3. Add to backlog if priority is Low
4. Update stakeholders on decision and timeline

---

## Priority Assignment Criteria

### Security Issues: Always High Priority

**Immediate Actions:**
- Create security advisory if needed
- Assess severity (Critical/High/Medium/Low)
- Develop and test patch
- Notify affected users
- Document fix and prevention measures

**Examples from Savrli AI:**
- API key exposure in logs or responses
- Injection vulnerabilities in conversation inputs
- Unauthorized access to session data
- XSS vulnerabilities in dashboard
- Dependency vulnerabilities in critical packages

---

### Performance Issues: Priority Based on Severity

**High Priority:**
- Response time > 5 seconds for core endpoints
- Memory leaks affecting platform stability
- Database query timeouts
- API rate limit issues affecting all users

**Medium Priority:**
- Response time 2-5 seconds for secondary endpoints
- Inefficient algorithms that could be optimized
- Resource usage higher than expected

**Low Priority:**
- Minor optimizations with minimal user impact
- Code refactoring for future performance
- Caching enhancements for edge cases

---

### Feature Requests: Evaluated by Framework

Use the **RICE Framework** for feature prioritization:

**R - Reach**: How many users will benefit?
- High Reach: 80%+ of users (Score: 10)
- Medium Reach: 30-80% of users (Score: 5)
- Low Reach: <30% of users (Score: 1)

**I - Impact**: How much will it improve the user experience?
- Massive Impact: 3x
- High Impact: 2x
- Medium Impact: 1x
- Low Impact: 0.5x
- Minimal Impact: 0.25x

**C - Confidence**: How certain are we about the estimates?
- High Confidence: 100%
- Medium Confidence: 80%
- Low Confidence: 50%

**E - Effort**: How much time will it take?
- Small: 1 person-week
- Medium: 2-4 person-weeks
- Large: 5-10 person-weeks
- Extra Large: 10+ person-weeks

**RICE Score = (Reach × Impact × Confidence) / Effort**

Higher scores indicate higher priority.

---

## Feature Request Evaluation

### Required Information

Every feature request should include:

1. **Use Case**: What problem does this solve?
2. **User Story**: As a [user type], I want [goal] so that [benefit]
3. **Acceptance Criteria**: How do we know when it's done?
4. **Alternatives Considered**: What other solutions were evaluated?
5. **Dependencies**: What does this depend on or affect?

### Evaluation Questions

**Strategic Alignment:**
- ✓ Does this align with our platform vision?
- ✓ Does this support our key use cases?
- ✓ Does this differentiate us from competitors?

**Technical Feasibility:**
- ✓ Can we implement this with current architecture?
- ✓ Are there technical blockers or dependencies?
- ✓ What is the maintenance burden?

**User Value:**
- ✓ How many users requested this?
- ✓ Is there strong user demand (votes, comments)?
- ✓ Does this solve a real pain point?

**Resource Constraints:**
- ✓ Do we have the expertise to build this?
- ✓ What is the opportunity cost?
- ✓ Can we deliver this in a reasonable timeframe?

### Decision Outcomes

After evaluation, features are:

1. **Approved**: Added to roadmap with priority
2. **Deferred**: Interesting but not now, revisit in 3-6 months
3. **Rejected**: Does not align with platform vision or strategy
4. **Needs More Info**: Requires additional research or clarification

---

## Bug Severity Classification

### Critical (Priority: High)

**Definition:** Complete system failure, data loss, or security breach.

**Characteristics:**
- Platform is completely unusable
- Data is corrupted or lost
- Security vulnerability is actively exploited
- No workaround available

**Examples:**
- Server crashes on startup
- Database corruption
- Authentication bypass vulnerability
- OpenAI API integration completely broken

**Response:**
- Immediate attention (drop everything)
- Fix within 24-48 hours
- Hotfix deployment if in production

---

### Major (Priority: High)

**Definition:** Significant functionality is broken, but workarounds exist.

**Characteristics:**
- Core feature is broken for all users
- Workaround is difficult or time-consuming
- Significant user impact
- Affects key workflows

**Examples:**
- Multimodal model selection returns errors for all vision models
- Session management fails to persist conversations
- Dashboard shows incorrect statistics
- Platform integration fails to send messages

**Response:**
- Address within 1-2 weeks
- Regular status updates
- Include in next sprint

---

### Minor (Priority: Medium)

**Definition:** Functionality works but not as expected; easy workarounds available.

**Characteristics:**
- Feature works with limitations
- Easy workaround exists
- Affects subset of users
- Cosmetic or minor functional issues

**Examples:**
- Sentiment analysis returns slightly inaccurate scores
- Export formatting is inconsistent
- Dashboard theme doesn't persist on all browsers
- Error messages could be more descriptive

**Response:**
- Address within 2-4 weeks
- Include in upcoming sprint
- May be combined with related work

---

### Trivial (Priority: Low)

**Definition:** Cosmetic issues, typos, or very minor problems.

**Characteristics:**
- No functional impact
- Cosmetic or aesthetic issue
- Documentation typo
- Extremely rare edge case

**Examples:**
- Typo in dashboard label
- Inconsistent spacing in UI
- Documentation formatting issue
- Console warning message

**Response:**
- Address when convenient
- May be bundled with other work
- Good candidate for community contributions

---

## Examples

### Example 1: Multimodal Vision Processing Bug

**Scenario:**  
Users report that the `/ai/vision` endpoint returns 500 errors for all image URLs.

**Triaging Process:**

1. **Initial Assessment:**
   - Category: Bug
   - Labels: `bug`, `multimodal`, `vision`, `needs-triage`

2. **Impact Analysis:**
   - User Impact: High - Core feature broken for all users
   - System Impact: Medium - Other features still work
   - Business Impact: High - Key differentiator not working

3. **Effort Estimation:**
   - Small to Medium (1-2 days to debug and fix)

4. **Severity Classification:**
   - **Major Bug** - Core feature broken but platform still usable

5. **Priority Assignment:**
   - **High Priority** - Core multimodal capability broken

6. **Assignment:**
   - Assign to multimodal feature owner
   - Add to current sprint
   - Target: Fix within 1 week

**RICE Score:**
- Reach: 7 (70% of users use vision features)
- Impact: 2x (restores critical functionality)
- Confidence: 100% (bug confirmed)
- Effort: 2 person-days (0.4 weeks)
- **Score: (7 × 2 × 1.0) / 0.4 = 35**

---

### Example 2: New Platform Integration Request (Teams)

**Scenario:**  
Multiple users request Microsoft Teams integration similar to existing Slack/Discord plugins.

**Triaging Process:**

1. **Initial Assessment:**
   - Category: Feature Request
   - Labels: `feature`, `integrations`, `teams`, `needs-triage`
   - Community votes: 8 users

2. **Impact Analysis:**
   - User Impact: Medium - Requested by enterprise users
   - System Impact: Low - Follows existing plugin pattern
   - Business Impact: Medium - Supports enterprise customers

3. **Effort Estimation:**
   - Medium (1-2 weeks including testing and docs)

4. **Feature Evaluation:**
   - Strategic Alignment: ✓ (matches integration strategy)
   - Technical Feasibility: ✓ (plugin pattern exists)
   - User Value: ✓ (8 user votes, enterprise demand)
   - Resource Constraints: ✓ (can allocate resources)

5. **Priority Assignment:**
   - **Medium Priority** - Valuable integration with clear demand

6. **Assignment:**
   - Add to Q1 2026 roadmap
   - Assign to integrations team
   - Target: Deliver in 3-4 weeks

**RICE Score:**
- Reach: 4 (40% of enterprise users)
- Impact: 1.5x (significant value for Teams users)
- Confidence: 80% (proven pattern, slight uncertainty on Teams API)
- Effort: 2 person-weeks
- **Score: (4 × 1.5 × 0.8) / 2 = 2.4**

---

### Example 3: Resource Management Export Enhancement

**Scenario:**  
User requests adding XML export format alongside existing JSON/CSV/Markdown exports.

**Triaging Process:**

1. **Initial Assessment:**
   - Category: Enhancement
   - Labels: `enhancement`, `resource-management`, `export`, `needs-triage`
   - Community votes: 1 user

2. **Impact Analysis:**
   - User Impact: Low - Single user request, existing formats sufficient
   - System Impact: Low - Additive feature, no breaking changes
   - Business Impact: Low - No business driver

3. **Effort Estimation:**
   - Small (< 1 day to implement and test)

4. **Feature Evaluation:**
   - Strategic Alignment: ~ (not core to platform)
   - Technical Feasibility: ✓ (straightforward to implement)
   - User Value: ✗ (minimal demand, existing alternatives)
   - Resource Constraints: ✓ (small effort)

5. **Priority Assignment:**
   - **Low Priority** - Nice-to-have but no strong demand

6. **Assignment:**
   - Add to backlog
   - Mark as "good first issue" for community contributors
   - No target timeline

**RICE Score:**
- Reach: 0.5 (5% of users might use it)
- Impact: 0.25x (minimal impact with existing formats)
- Confidence: 50% (uncertain if anyone would actually use it)
- Effort: 0.2 person-weeks (1 day)
- **Score: (0.5 × 0.25 × 0.5) / 0.2 = 0.31**

---

### Example 4: Session Management Performance Issue

**Scenario:**  
Response time for `/sessions` endpoint exceeds 3 seconds when there are 100+ active sessions.

**Triaging Process:**

1. **Initial Assessment:**
   - Category: Performance
   - Labels: `performance`, `resource-management`, `sessions`, `needs-triage`

2. **Impact Analysis:**
   - User Impact: Medium - Affects users with many sessions
   - System Impact: Medium - Could worsen as usage grows
   - Business Impact: Medium - Affects scalability

3. **Effort Estimation:**
   - Small to Medium (1-3 days to optimize and test)

4. **Severity Classification:**
   - **Medium Performance Issue** - Affects subset of users, has workaround

5. **Priority Assignment:**
   - **Medium Priority** - Important for scalability

6. **Assignment:**
   - Add to current or next sprint
   - Assign to backend/resource management team
   - Target: Optimize within 2 weeks

**RICE Score:**
- Reach: 3 (30% of power users affected)
- Impact: 1.5x (significantly improves UX for affected users)
- Confidence: 90% (clear optimization path)
- Effort: 0.5 person-weeks
- **Score: (3 × 1.5 × 0.9) / 0.5 = 8.1**

---

## Decision Framework

### Priority Decision Tree

```
Is it a security vulnerability?
├─ Yes → HIGH PRIORITY
└─ No → Continue

Is core functionality completely broken?
├─ Yes → HIGH PRIORITY
└─ No → Continue

How many users are affected?
├─ 80%+ → Consider HIGH
├─ 30-80% → Consider MEDIUM
└─ <30% → Consider LOW

What is the user impact?
├─ Blocks critical workflows → Increase priority
├─ Workaround exists → Maintain priority
└─ Minimal impact → Decrease priority

What is the effort required?
├─ Small effort + High impact → Increase priority
├─ Large effort + Low impact → Decrease priority
└─ Otherwise → Maintain priority

Calculate RICE score for features:
├─ Score > 10 → HIGH PRIORITY
├─ Score 2-10 → MEDIUM PRIORITY
└─ Score < 2 → LOW PRIORITY
```

### Priority Matrix

| Impact ↓ / Effort → | Small (<1 week) | Medium (1-3 weeks) | Large (3+ weeks) |
|---------------------|-----------------|-------------------|------------------|
| **High**            | HIGH            | HIGH              | MEDIUM           |
| **Medium**          | MEDIUM          | MEDIUM            | LOW              |
| **Low**             | LOW             | LOW               | LOW              |

---

## Escalation Process

### When to Escalate

Escalate an issue to leadership when:

1. **Priority Conflicts:**
   - Multiple high-priority items competing for resources
   - Disagreement on priority assignment
   - Capacity constraints preventing timely resolution

2. **Dependency Blockers:**
   - Blocked by external team or vendor
   - Technical blocker requires architectural decision
   - Resource allocation needed from other teams

3. **Customer Impact:**
   - Multiple customers affected by same issue
   - Customer threatening to churn
   - SLA breach imminent

4. **Security Concerns:**
   - Critical vulnerability discovered
   - Active security incident
   - Compliance or legal implications

### Escalation Path

1. **Level 1:** Engineering Team Lead
   - Reviews priority assignment
   - Allocates team resources
   - Resolves technical blockers

2. **Level 2:** Engineering Manager
   - Resolves cross-team dependencies
   - Makes architectural decisions
   - Allocates additional resources

3. **Level 3:** Product Leadership
   - Makes strategic trade-off decisions
   - Addresses customer escalations
   - Adjusts roadmap priorities

### Escalation Information

When escalating, provide:

- Issue/feature summary and context
- Current priority and reasoning
- Why escalation is needed
- Proposed resolution or decision needed
- Impact of delay
- Recommendation

---

## Regular Review Cadence

### Daily (High Priority Items)

- Review status of all high-priority bugs and features
- Update stakeholders on progress
- Identify and remove blockers
- Adjust assignments as needed

### Weekly (Medium Priority Items)

- Review medium-priority backlog
- Promote items to high if circumstances change
- Update priority based on new information
- Plan upcoming sprint work

### Monthly (All Items)

- Review entire backlog
- Re-prioritize based on current strategy
- Close or defer stale items
- Update RICE scores for features
- Analyze priority distribution
- Adjust process if needed

### Quarterly (Strategic Review)

- Review priority guidelines effectiveness
- Analyze delivered value by priority
- Adjust criteria based on learnings
- Update stakeholders on roadmap changes

---

## Metrics to Track

### Priority Health Metrics

- **High Priority Age:** Average time high-priority items spend open
  - Target: < 2 weeks
  
- **Backlog Size by Priority:**
  - High: Target < 10 items
  - Medium: Target < 30 items
  - Low: No limit (manage actively)

- **Priority Distribution:**
  - High: 10-20% of total items
  - Medium: 30-40% of total items
  - Low: 40-60% of total items

- **SLA Compliance:**
  - % of high-priority items resolved within 2 weeks
  - % of medium-priority items resolved within 4 weeks
  - Target: > 80% compliance

### Quality Metrics

- **Triage Speed:** Time from creation to triaged
  - Target: < 48 hours for all issues

- **Priority Changes:** How often priorities change after initial assignment
  - Target: < 20% change rate

- **Escalation Rate:** How often issues need escalation
  - Target: < 10% of items

---

## Best Practices

### For Triagers

1. **Be Consistent:** Apply criteria uniformly across all items
2. **Gather Context:** Understand user impact before assigning priority
3. **Communicate Clearly:** Explain priority decisions transparently
4. **Update Regularly:** Re-evaluate priorities as circumstances change
5. **Document Decisions:** Record reasoning for future reference

### For Contributors

1. **Provide Details:** Include all relevant information in requests
2. **Explain Impact:** Help triagers understand user impact
3. **Accept Decisions:** Trust the triage process
4. **Offer Help:** Contribute to high-priority items when possible
5. **Be Patient:** Low priority doesn't mean not valuable

### For Stakeholders

1. **Respect Process:** Allow triage process to work
2. **Provide Input:** Share customer feedback and business context
3. **Trust Expertise:** Engineering team knows technical constraints
4. **Plan Ahead:** Submit requests early for planning
5. **Escalate Appropriately:** Only escalate when truly necessary

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| Nov 10, 2025 | 1.0 | Initial priority guidelines document | _[To be assigned]_ |

---

**Last Updated:** November 10, 2025  
**Next Review:** December 2025

For specific feature priorities and status, see [FEATURE_CATALOG.md](./FEATURE_CATALOG.md).
