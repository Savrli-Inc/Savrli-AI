# Issue Templates for Sub-tasks

This document provides recommended GitHub issue templates for creating sub-tasks from the roadmap. Use these templates to ensure consistent, well-documented issues that are easy to understand and implement.

---

## Table of Contents

1. [Feature Sub-task Template](#feature-sub-task-template)
2. [Bug Fix Template](#bug-fix-template)
3. [Documentation Task Template](#documentation-task-template)
4. [Testing Task Template](#testing-task-template)
5. [Chore/Maintenance Template](#choremaintenance-template)
6. [Integration Task Template](#integration-task-template)
7. [UI/UX Task Template](#uiux-task-template)
8. [Performance Optimization Template](#performance-optimization-template)

---

## Feature Sub-task Template

Use this template for implementing new features or enhancements.

```markdown
## Feature Sub-task: [Short descriptive title]

**Related to Roadmap Feature**: [Link to parent feature in ROADMAP.md]  
**Milestone**: `[milestone-name]` (e.g., v2.1-playground)  
**Labels**: `feature`, `area:[frontend/backend/etc]`, `priority:[high/medium/low]`

---

### Description

[Clear, concise description of what needs to be implemented]

**Example**: Implement real-time streaming UI component that displays AI responses token-by-token as they arrive from the backend.

---

### Expected Outcome

[What should exist when this task is complete?]

**Example**:
- Users see AI responses appear progressively in real-time
- Streaming can be stopped mid-response with a cancel button
- Loading indicators show when waiting for first token

---

### Technical Details

**Files to Create/Modify**:
- [ ] `[path/to/file1.py]` - [What changes are needed]
- [ ] `[path/to/file2.js]` - [What changes are needed]

**Dependencies**:
- [ ] [List any dependencies or prerequisite tasks]
- [ ] [Link to related issues if applicable]

**API Changes** (if applicable):
- New endpoints: [List any new endpoints]
- Modified endpoints: [List modifications to existing endpoints]
- Breaking changes: [Yes/No - describe if yes]

---

### Implementation Approach

[Brief overview of how to implement this feature]

**Example**:
1. Create StreamingDisplay component in `components/`
2. Add Server-Sent Events (SSE) handler
3. Implement token buffering and display logic
4. Add cancel/stop functionality
5. Wire up to existing chat endpoint

---

### Acceptance Criteria

- [ ] [Specific, testable requirement 1]
- [ ] [Specific, testable requirement 2]
- [ ] [Specific, testable requirement 3]
- [ ] Code follows project style guidelines
- [ ] Tests added/updated with >80% coverage
- [ ] Documentation updated
- [ ] Manually tested and verified

**Example**:
- [ ] Streaming displays tokens as they arrive (not batched)
- [ ] Cancel button stops streaming immediately
- [ ] Error handling shows appropriate messages
- [ ] Works with all supported models
- [ ] No memory leaks during long responses

---

### Testing Checklist

- [ ] Unit tests added for new functions/components
- [ ] Integration tests cover main workflows
- [ ] Edge cases tested (empty responses, errors, timeouts)
- [ ] Performance tested with large responses
- [ ] Browser compatibility verified (Chrome, Firefox, Safari)

---

### Documentation Requirements

- [ ] Inline code comments for complex logic
- [ ] API documentation updated (if applicable)
- [ ] User-facing documentation in `docs/`
- [ ] README updated (if user-visible feature)
- [ ] CHANGELOG entry added

---

### Additional Context

[Any additional information, screenshots, mockups, or references]

**Example**:
- Mockup: [Link to design mockup]
- Similar implementation: [Link to reference]
- Discussion: [Link to discussion or RFC]

---

### Related Issues/PRs

- Related to #[issue-number]
- Depends on #[issue-number]
- Blocks #[issue-number]
```

---

## Bug Fix Template

Use this template for fixing bugs discovered in existing features.

```markdown
## Bug Fix: [Short description of the bug]

**Milestone**: `[milestone-name]`  
**Labels**: `bug`, `area:[area]`, `priority:[high/medium/low]`

---

### Bug Description

[Clear description of the bug and its impact]

**Example**: Streaming responses fail with a TypeError when the model returns an empty delta, causing the UI to freeze.

---

### Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Example**:
1. Open playground at `/playground`
2. Select GPT-4 model
3. Send prompt: "Hello"
4. Observe error in browser console

---

### Expected Behavior

[What should happen?]

**Example**: Streaming should handle empty deltas gracefully and continue processing subsequent tokens.

---

### Actual Behavior

[What actually happens?]

**Example**: TypeError: Cannot read property 'content' of undefined, streaming stops, UI freezes.

---

### Environment

- **Browser/Platform**: [e.g., Chrome 120 on macOS]
- **API Version**: [e.g., v2.1.0]
- **Model**: [e.g., gpt-4-turbo]
- **Reproducibility**: [Always/Sometimes/Rarely]

---

### Root Cause Analysis

[If known, describe the root cause]

**Example**: The code assumes every chunk has `choices[0].delta.content`, but OpenAI can send chunks with empty deltas during streaming.

---

### Proposed Solution

[How should this be fixed?]

**Example**:
1. Add null check for `delta.content`
2. Skip chunks with empty deltas
3. Add unit test for empty delta handling

---

### Files to Modify

- [ ] `[path/to/file.py]` - [What to fix]

---

### Testing

- [ ] Add regression test to prevent recurrence
- [ ] Verify fix in development environment
- [ ] Test with multiple models
- [ ] Verify no new bugs introduced

---

### Acceptance Criteria

- [ ] Bug no longer reproducible
- [ ] Regression test added
- [ ] No breaking changes
- [ ] Related bugs checked and fixed

---

### Additional Context

- Error logs: [Paste relevant logs]
- Screenshots: [If applicable]
- Related bugs: #[issue-number]
```

---

## Documentation Task Template

Use this template for documentation improvements.

```markdown
## Documentation: [What documentation is being added/updated]

**Milestone**: `[milestone-name]`  
**Labels**: `docs`, `priority:[high/medium/low]`

---

### Documentation Need

[What documentation is missing or needs improvement?]

**Example**: The Slack integration guide lacks OAuth setup instructions, making it difficult for users to configure the bot.

---

### Target Audience

[Who is this documentation for?]

**Example**:
- Primary: Developers integrating Savrli AI with Slack
- Secondary: DevOps engineers setting up production deployments

---

### Content Outline

[High-level outline of what should be documented]

**Example**:
1. **Prerequisites**
   - Slack workspace admin access
   - Savrli AI deployment URL
   
2. **Creating a Slack App**
   - Step-by-step with screenshots
   - Required scopes and permissions
   
3. **OAuth Configuration**
   - Redirect URLs
   - Token installation
   
4. **Environment Variables**
   - Complete list with examples
   
5. **Testing the Integration**
   - Verification steps
   - Common issues and solutions

---

### Files to Create/Update

- [ ] `docs/[filename].md` - [New file or update existing]
- [ ] `README.md` - [Update with new doc link]
- [ ] `docs/INTEGRATION_API.md` - [Add cross-references]

---

### Required Elements

- [ ] Clear, step-by-step instructions
- [ ] Code examples that work copy-paste
- [ ] Screenshots or diagrams (if UI-related)
- [ ] Common issues / troubleshooting section
- [ ] Links to relevant external documentation
- [ ] Last updated date

---

### Examples to Include

**Example**:
- [ ] Complete OAuth flow example
- [ ] Sample environment configuration
- [ ] Example bot interaction
- [ ] Webhook payload examples
- [ ] Error handling examples

---

### Acceptance Criteria

- [ ] Documentation is clear and complete
- [ ] All code examples tested and working
- [ ] Screenshots/diagrams included where needed
- [ ] Follows project documentation style
- [ ] Reviewed by at least one other person
- [ ] Links verified and working

---

### Additional Context

- Reference documentation: [Links]
- Similar examples: [Links]
- User feedback/requests: [Links to issues]
```

---

## Testing Task Template

Use this template for adding or improving tests.

```markdown
## Testing: [What is being tested]

**Milestone**: `[milestone-name]`  
**Labels**: `test`, `area:[area]`, `priority:[high/medium/low]`

---

### Testing Objective

[What needs to be tested and why?]

**Example**: Add comprehensive tests for the streaming chat endpoint to ensure reliability under various conditions.

---

### Current Test Coverage

[What tests currently exist, if any?]

**Example**: 
- Existing: Basic chat endpoint test
- Missing: Streaming tests, error handling, edge cases

---

### Test Cases to Add

**Unit Tests**:
- [ ] [Test case 1]
- [ ] [Test case 2]

**Integration Tests**:
- [ ] [Test case 1]
- [ ] [Test case 2]

**End-to-End Tests** (if applicable):
- [ ] [Test case 1]

**Example**:

**Unit Tests**:
- [ ] Test token-by-token streaming
- [ ] Test empty delta handling
- [ ] Test error mid-stream
- [ ] Test stream cancellation

**Integration Tests**:
- [ ] Test complete streaming flow
- [ ] Test streaming with session history
- [ ] Test streaming with different models
- [ ] Test concurrent streams

---

### Files to Create/Update

- [ ] `tests/test_[feature].py` - [New test file or update existing]

---

### Test Data Requirements

[Any specific test data or fixtures needed?]

**Example**:
- Mock OpenAI responses with various stream patterns
- Sample prompts of different lengths
- Error scenarios (timeout, invalid token, etc.)

---

### Expected Coverage Improvement

- Current coverage: [X%]
- Target coverage: [Y%]

**Example**:
- Current coverage: 65%
- Target coverage: 85%

---

### Acceptance Criteria

- [ ] All specified test cases implemented
- [ ] All tests pass consistently
- [ ] Coverage target achieved
- [ ] Tests follow project testing conventions
- [ ] Tests are maintainable and well-documented
- [ ] CI/CD pipeline updated if needed

---

### Additional Context

- Related feature: #[issue-number]
- Testing framework: [pytest, jest, etc.]
- Special requirements: [mocking, fixtures, etc.]
```

---

## Chore/Maintenance Template

Use this template for maintenance tasks and infrastructure improvements.

```markdown
## Chore: [Short description of maintenance task]

**Milestone**: `[milestone-name]`  
**Labels**: `chore`, `priority:[high/medium/low]`

---

### Task Description

[What maintenance work needs to be done?]

**Example**: Update all dependencies to their latest stable versions to address security vulnerabilities and improve performance.

---

### Motivation

[Why is this task important?]

**Example**: 
- 3 dependencies have known security vulnerabilities
- Performance improvements in FastAPI 0.110+
- Improved Python 3.12 compatibility

---

### Scope of Work

**Dependencies to Update**:
- [ ] `[package-name]`: [current-version] → [target-version]
- [ ] `[package-name]`: [current-version] → [target-version]

**Configuration Changes**:
- [ ] [Config file 1] - [What needs updating]
- [ ] [Config file 2] - [What needs updating]

**Example**:
- [ ] `fastapi`: 0.104.1 → 0.110.0
- [ ] `openai`: 1.3.0 → 1.12.0
- [ ] `pytest`: 7.4.0 → 8.0.0

---

### Potential Breaking Changes

[Any known breaking changes to be aware of?]

**Example**:
- FastAPI 0.110 changed response model validation
- OpenAI client API signature updated
- Need to update import statements

---

### Testing Strategy

- [ ] Run full test suite
- [ ] Test all integrations manually
- [ ] Verify playground functionality
- [ ] Check for deprecation warnings
- [ ] Performance benchmark comparison

---

### Rollback Plan

[How to rollback if issues occur?]

**Example**: If issues arise, revert `requirements.txt` to previous versions and redeploy.

---

### Acceptance Criteria

- [ ] All dependencies updated successfully
- [ ] All tests pass
- [ ] No new security vulnerabilities
- [ ] Application functions as expected
- [ ] Documentation updated (if needed)
- [ ] `requirements.txt` and lock files updated

---

### Additional Context

- Security advisories: [Links]
- Release notes: [Links]
- Related issues: #[issue-number]
```

---

## Integration Task Template

Use this template for tasks related to third-party integrations.

```markdown
## Integration: [Platform name] - [Specific feature]

**Milestone**: `[milestone-name]`  
**Labels**: `feature`, `area:integrations`, `priority:[high/medium/low]`

---

### Integration Overview

[Brief description of the integration]

**Example**: Implement webhook handling for Notion database updates to trigger AI processing when new entries are added.

---

### Platform Details

- **Platform**: [e.g., Notion, Slack, Discord]
- **API Version**: [e.g., v2, v9]
- **Authentication**: [OAuth 2.0, API Key, etc.]
- **Rate Limits**: [e.g., 3 requests/second]

---

### Features to Implement

- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Feature 3]

**Example**:
- [ ] Receive webhook notifications
- [ ] Verify webhook signatures
- [ ] Process database update events
- [ ] Trigger AI analysis
- [ ] Send results back to Notion

---

### Technical Implementation

**Plugin File**: `integrations/[platform]_plugin.py`

**Methods to Implement**:
- [ ] `__init__()` - Configuration and setup
- [ ] `send_message()` - Send data to platform
- [ ] `process_webhook()` - Handle incoming webhooks
- [ ] `verify_signature()` - Webhook security

**New Endpoints**:
- [ ] `POST /integrations/[platform]/webhook` - Receive webhooks
- [ ] `POST /integrations/[platform]/send` - Send to platform

---

### Configuration

**Environment Variables**:
```bash
[PLATFORM]_API_KEY=your-api-key
[PLATFORM]_WEBHOOK_SECRET=your-secret
[PLATFORM]_ENABLED=true
```

**Example**:
```bash
NOTION_API_KEY=secret_abc123
NOTION_WEBHOOK_SECRET=whsec_xyz789
NOTION_ENABLED=true
```

---

### Testing Requirements

- [ ] Unit tests for all plugin methods
- [ ] Mock external API calls
- [ ] Test webhook verification
- [ ] Test error handling and retries
- [ ] Integration test with sandbox account

---

### Documentation Requirements

- [ ] Update `docs/INTEGRATION_API.md`
- [ ] Add to `docs/PLUGIN_EXAMPLES.md` with examples
- [ ] Create setup guide in `docs/integrations/[PLATFORM].md`
- [ ] Add to README integrations list

---

### Security Considerations

- [ ] Webhook signature verification implemented
- [ ] API credentials stored securely (env vars)
- [ ] Rate limiting implemented
- [ ] Input validation on all webhook data
- [ ] HTTPS enforced for webhooks

---

### Acceptance Criteria

- [ ] Integration works end-to-end
- [ ] Webhook verification passes
- [ ] Error handling graceful
- [ ] Tests pass with >80% coverage
- [ ] Documentation complete
- [ ] Security review passed

---

### Additional Context

- Platform API docs: [Link]
- Example integrations: [Links]
- Related issues: #[issue-number]
```

---

## UI/UX Task Template

Use this template for frontend and user experience improvements.

```markdown
## UI/UX: [Feature/Improvement name]

**Milestone**: `[milestone-name]`  
**Labels**: `feature`, `area:frontend`, `priority:[high/medium/low]`

---

### User Story

**As a** [type of user]  
**I want** [goal]  
**So that** [benefit]

**Example**:
**As a** developer using the playground  
**I want** to see AI responses appear in real-time  
**So that** I can get immediate feedback and stop long responses early

---

### Current Experience

[What is the current user experience?]

**Example**: Currently, users must wait for the entire response to complete before seeing any output, which can take 10-30 seconds for long responses.

---

### Desired Experience

[What should the new experience be?]

**Example**: Users should see each word appear as the AI generates it, with a clear indicator when streaming is in progress and ability to stop at any time.

---

### Design Specifications

**Visual Design**:
- Mockups: [Link to Figma/design file]
- Color scheme: [Colors from design system]
- Typography: [Fonts and sizes]
- Spacing: [Padding/margins]

**Interactions**:
- [ ] [Interaction 1] - [How it should work]
- [ ] [Interaction 2] - [How it should work]

**Example**:
- [ ] Streaming indicator - Pulsing dot next to response
- [ ] Stop button - Red button appears during streaming
- [ ] Word appears - Fade-in animation for new tokens

---

### Components to Create/Modify

- [ ] `components/[ComponentName].jsx` - [Description]
- [ ] `styles/[stylesheet].css` - [Description]

---

### Responsive Design

- [ ] Mobile (320px - 767px)
- [ ] Tablet (768px - 1023px)
- [ ] Desktop (1024px+)

**Behavior per breakpoint**: [Describe responsive behavior]

---

### Accessibility Requirements

- [ ] Keyboard navigation support
- [ ] Screen reader compatibility
- [ ] ARIA labels and roles
- [ ] Color contrast meets WCAG AA
- [ ] Focus indicators visible
- [ ] Error messages announced

---

### Browser Support

- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Edge (latest 2 versions)

---

### Performance Requirements

- [ ] Initial render < 100ms
- [ ] Smooth animations (60fps)
- [ ] No layout shifts (CLS < 0.1)
- [ ] Lazy load non-critical resources

---

### Acceptance Criteria

- [ ] Matches design specifications
- [ ] Responsive on all screen sizes
- [ ] Accessible (WCAG AA compliant)
- [ ] Works in all supported browsers
- [ ] No performance regressions
- [ ] User feedback positive (if testing with users)

---

### Testing Checklist

- [ ] Visual regression tests
- [ ] Interaction tests
- [ ] Accessibility audit passed
- [ ] Cross-browser testing completed
- [ ] Performance benchmarks met

---

### Additional Context

- Design files: [Link]
- User research: [Link]
- Inspiration: [Links to similar UIs]
```

---

## Performance Optimization Template

Use this template for performance improvement tasks.

```markdown
## Performance: [What is being optimized]

**Milestone**: `[milestone-name]`  
**Labels**: `feature`, `performance`, `priority:[high/medium/low]`

---

### Performance Issue

[What performance problem needs to be addressed?]

**Example**: Chat endpoint response time is 3-5 seconds for simple queries due to inefficient session history retrieval.

---

### Current Metrics

- **Metric**: [Current value]
- **Target**: [Target value]

**Example**:
- **Response Time (p95)**: 4.2 seconds
- **Response Time (p50)**: 2.8 seconds
- **Target Response Time**: <500ms

---

### Root Cause

[What is causing the performance issue?]

**Example**: 
- Loading entire conversation history from database
- No caching layer
- Inefficient query without indexes
- Processing all messages even when not needed

---

### Proposed Optimization

[How will performance be improved?]

**Example**:
1. Add Redis caching layer for recent conversations
2. Implement database indexing on session_id
3. Limit history retrieval to last 50 messages
4. Add query result pagination

---

### Implementation Plan

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

**Example**:
- [ ] Set up Redis cache
- [ ] Add cache middleware
- [ ] Implement cache invalidation logic
- [ ] Add database indexes
- [ ] Update query to use indexes
- [ ] Add pagination support

---

### Files to Modify

- [ ] `[path/to/file]` - [Changes]

---

### Benchmarking

**Before Optimization**:
```
[Benchmark results before changes]
```

**After Optimization** (Target):
```
[Expected benchmark results]
```

**Example**:

**Before**:
- p50: 2.8s
- p95: 4.2s
- p99: 6.1s
- Throughput: 50 req/min

**After** (Target):
- p50: <300ms
- p95: <500ms
- p99: <1s
- Throughput: >500 req/min

---

### Testing Strategy

- [ ] Load testing with realistic scenarios
- [ ] Stress testing at peak load
- [ ] Memory profiling
- [ ] CPU profiling
- [ ] Database query analysis

**Tools**:
- Load testing: [e.g., k6, locust]
- Profiling: [e.g., py-spy, cProfile]
- Monitoring: [e.g., Datadog, New Relic]

---

### Acceptance Criteria

- [ ] Target metrics achieved
- [ ] No functionality regressions
- [ ] Memory usage acceptable
- [ ] Code remains maintainable
- [ ] Monitoring/alerts configured

---

### Monitoring

[What metrics should be monitored post-deployment?]

**Example**:
- Response time percentiles (p50, p95, p99)
- Cache hit rate
- Database query time
- Error rate
- Resource utilization

---

### Rollback Plan

[How to rollback if optimization causes issues?]

**Example**: Feature flag controls cache usage. Can disable caching via environment variable without code deployment.

---

### Additional Context

- Profiling results: [Link/paste results]
- Related performance issues: #[issue-number]
- Monitoring dashboard: [Link]
```

---

## Tips for Using These Templates

### General Guidelines

1. **Be Specific**: Clear, specific tasks are easier to estimate and implement
2. **One Task, One Issue**: Don't combine multiple unrelated tasks
3. **Reference the Roadmap**: Always link back to the parent feature
4. **Use Checklists**: Makes it easy to track progress
5. **Add Context**: Include links, screenshots, and examples
6. **Set Clear Criteria**: Define "done" explicitly

### Label Combinations

Use multiple labels to categorize issues effectively:

```
feature + area:frontend + priority:high
bug + area:backend + priority:medium
docs + priority:low
test + area:integrations + priority:high
chore + priority:medium
```

### Milestone Assignment

- Assign issues to the appropriate milestone from [ROADMAP.md](./ROADMAP.md)
- Milestones should have target dates
- Group related issues in the same milestone

### Issue Relationships

Use keywords to link issues:
- `Closes #123` - This PR will close the issue
- `Fixes #123` - Alias for Closes
- `Resolves #123` - Alias for Closes
- `Relates to #123` - Related but doesn't close
- `Depends on #123` - Can't start until dependency is done
- `Blocks #123` - Other issue waiting for this

---

## Creating Issues from Roadmap

### Step-by-Step Process

1. **Choose a Feature** from [docs/ROADMAP.md](./ROADMAP.md)
2. **Select a Sub-task** (there are 3-6 for each feature)
3. **Pick the Right Template** from this document
4. **Fill in All Sections** with specific details
5. **Add Appropriate Labels** (type, area, priority)
6. **Assign to Milestone** as specified in roadmap
7. **Link Related Issues** using keywords
8. **Submit for Review** (or assign if self-implementing)

### Example: Creating an Issue for Playground Streaming

From ROADMAP.md, Feature 1, Sub-task 1:
> "Design and implement streaming UI components"

1. Use **UI/UX Task Template**
2. Title: "UI/UX: Implement real-time streaming display component"
3. Labels: `feature`, `area:frontend`, `priority:high`
4. Milestone: `v2.1-playground`
5. Fill template with streaming-specific details
6. Submit issue

---

## Issue Template Best Practices

### For Issue Creators

- **Use the checklist format** - Easy to track progress
- **Be explicit about "done"** - Clear acceptance criteria
- **Provide examples** - Show what you mean
- **Link to resources** - Design files, docs, references
- **Estimate complexity** - Helps with planning (S/M/L or hours)

### For Issue Assignees

- **Ask questions early** - Don't assume, clarify
- **Update progress** - Check off completed items
- **Document decisions** - Add comments explaining choices
- **Link your PR** - Connect the issue to the implementation
- **Update tests/docs** - Don't forget non-code deliverables

### For Reviewers

- **Check all criteria** - Ensure all checkboxes are addressed
- **Test thoroughly** - Verify the acceptance criteria
- **Review documentation** - Ensure docs were updated
- **Provide constructive feedback** - Help improve the work
- **Celebrate completion** - Acknowledge good work! 🎉

---

## Customizing Templates

Feel free to adapt these templates for your specific needs:

- Add project-specific sections
- Remove sections that don't apply
- Combine templates for complex tasks
- Create new templates for recurring task types

---

**Last Updated**: November 10, 2025  
**Maintained by**: Savrli AI Team  
**Feedback**: Open an issue or PR to improve these templates!
