# Resource Management Tools

This document describes the higher-level resource and content management tools for Savrli AI. These tools complement the core resource management functionality and provide advanced capabilities for organizing, searching, and managing conversational data.

## Overview

The Resource Management Tools API (`/api/resource-tools`) provides scaffolding for advanced resource management features including:

- **Tagging System**: Categorize and organize sessions with custom tags
- **Metadata Management**: Attach arbitrary metadata to sessions for enrichment and filtering
- **Batch Import/Export**: Trigger asynchronous operations for bulk data management
- **Dashboard Integration**: Summary statistics and search capabilities for user interfaces

These tools are designed to work alongside the core session management features (export, import, listing) defined in the base API.

## Related Issue

This functionality is scaffolded as part of [Issue #36](https://github.com/Savrli-Inc/Savrli-AI/issues/36) - Enhanced resource management capabilities.

## Architecture

### Tagging System

The tagging system enables flexible categorization of conversation sessions:

**Key Features:**
- Add/remove tags from sessions
- List all tags with usage statistics
- Filter sessions by tags
- Support for multiple tags per session

**Use Cases:**
- Categorize conversations by topic (e.g., "customer-support", "sales", "technical")
- Mark sessions for review or follow-up (e.g., "needs-review", "escalated")
- Organize by project or team (e.g., "project-alpha", "marketing-team")

**Endpoints:**
- `POST /api/resource-tools/tags/add` - Add tags to a session
- `POST /api/resource-tools/tags/remove` - Remove tags from a session
- `GET /api/resource-tools/tags/{session_id}` - Get tags for a session
- `GET /api/resource-tools/tags` - List all available tags with counts

### Metadata Schema

The metadata system supports arbitrary key-value pairs for custom session enrichment:

**Design Principles:**
- Flexible schema - no predefined structure required
- Support for nested objects and arrays
- Type preservation (strings, numbers, booleans, etc.)
- Versioning support for schema evolution

**Common Metadata Fields:**
```json
{
  "user_id": "string",
  "department": "string",
  "priority": "high|medium|low",
  "sentiment_score": 0.85,
  "language": "en",
  "created_at": "2025-01-01T10:00:00Z",
  "last_updated": "2025-01-01T10:30:00Z",
  "custom_fields": {
    "project_code": "PROJ-123",
    "cost_center": "CC-456"
  }
}
```

**Endpoints:**
- `POST /api/resource-tools/metadata/set` - Set metadata for a session
- `GET /api/resource-tools/metadata/{session_id}` - Get session metadata
- `DELETE /api/resource-tools/metadata/{session_id}` - Delete metadata (all or specific keys)

### Export/Import Flows

The batch export/import system enables asynchronous processing of large datasets:

**Export Flow:**
1. Submit export request with list of session IDs
2. Receive job ID for tracking
3. System processes export in background
4. Poll job status endpoint for completion
5. Download results when ready

**Import Flow:**
1. Submit import request with source data
2. Receive job ID for tracking
3. System validates and processes import in background
4. Poll job status endpoint for completion
5. Review import results and any errors

**Features:**
- Asynchronous processing for large operations
- Progress tracking via job IDs
- Support for multiple formats (JSON, CSV, Markdown)
- Include/exclude tags and metadata
- Merge strategies (append, overwrite, merge)
- Error handling and validation

**Endpoints:**
- `POST /api/resource-tools/export/trigger` - Trigger batch export
- `POST /api/resource-tools/import/trigger` - Trigger batch import
- `GET /api/resource-tools/jobs/{job_id}` - Check job status

### Dashboard Integration

Dashboard endpoints provide aggregated data for user interfaces:

**Summary Statistics:**
- Total sessions count
- Tag distribution (tag cloud data)
- Metadata field usage
- Recent activity timeline
- Storage usage metrics
- Popular sessions/conversations

**Search Capabilities:**
- Full-text search across conversation content
- Filter by tags (AND/OR logic)
- Filter by metadata values
- Date range filtering
- Sort by relevance, date, or custom fields
- Pagination support

**Endpoints:**
- `GET /api/resource-tools/dashboard/summary` - Get dashboard statistics
- `GET /api/resource-tools/search` - Advanced search and filtering

## Implementation Notes

### Current Status

⚠️ **All endpoints are currently stubs returning HTTP 501 (Not Implemented).**

This is intentional scaffolding to define the API surface and integration points. Implementation of actual functionality should be done as part of issue #36.

### Storage Considerations

The resource tools should **not** duplicate storage implementation from the core `resource_manager.py` module. Instead, they should:

1. Use existing `SessionManager` for session access
2. Extend storage with additional collections/tables for:
   - Tags (session_id → tag mappings)
   - Metadata (session_id → key-value store)
   - Jobs (async operation tracking)
3. Consider using a database (SQLite, PostgreSQL) for production deployments
4. Implement caching for frequently accessed data

### Integration with Existing Features

The resource tools complement existing functionality:

| Feature | Existing API | Resource Tools Enhancement |
|---------|--------------|----------------------------|
| Export | `/ai/sessions/export` - single session | `/api/resource-tools/export/trigger` - batch async |
| Import | `/ai/sessions/import` - single session | `/api/resource-tools/import/trigger` - batch async |
| Session List | `/ai/sessions` - basic listing | `/api/resource-tools/search` - advanced filtering |
| Session Data | Session content only | Add tags and metadata |

### Future Enhancements

Potential features to consider in future iterations:

- **Access Control**: Role-based permissions for sessions
- **Sharing**: Share sessions with other users
- **Versioning**: Track changes to sessions over time
- **Analytics**: Advanced analytics and insights
- **Webhooks**: Notify external systems of events
- **Scheduling**: Scheduled exports/reports
- **Templates**: Predefined tag sets and metadata schemas
- **Validation**: Schema validation for metadata

## Usage Examples

### Adding Tags to a Session

```bash
curl -X POST http://localhost:8000/api/resource-tools/tags/add \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "tags": ["customer-support", "billing-inquiry"]
  }'
```

**Expected Response (when implemented):**
```json
{
  "success": true,
  "message": "Tags added successfully",
  "session_id": "session_123",
  "tags": ["customer-support", "billing-inquiry"]
}
```

### Setting Session Metadata

```bash
curl -X POST http://localhost:8000/api/resource-tools/metadata/set \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "metadata": {
      "user_id": "user_456",
      "department": "Sales",
      "priority": "high",
      "sentiment_score": 0.85
    }
  }'
```

### Triggering Batch Export

```bash
curl -X POST http://localhost:8000/api/resource-tools/export/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "session_ids": ["session_123", "session_456", "session_789"],
    "format": "json",
    "include_metadata": true,
    "include_tags": true
  }'
```

**Expected Response (when implemented):**
```json
{
  "success": true,
  "message": "Export job created",
  "job_id": "job_abc123",
  "estimated_completion": "2025-01-01T10:05:00Z"
}
```

### Checking Job Status

```bash
curl http://localhost:8000/api/resource-tools/jobs/job_abc123
```

**Expected Response (when implemented):**
```json
{
  "job_id": "job_abc123",
  "status": "completed",
  "progress": 100,
  "created_at": "2025-01-01T10:00:00Z",
  "completed_at": "2025-01-01T10:04:32Z",
  "result": {
    "download_url": "/downloads/export_abc123.json",
    "session_count": 3,
    "file_size_bytes": 45678
  }
}
```

### Searching Resources

```bash
curl "http://localhost:8000/api/resource-tools/search?tags=customer-support&tags=billing-inquiry"
```

## Testing

Test stubs are provided in `tests/test_resource_tools.py`. These tests verify that:

1. All endpoints are accessible and return 501 status
2. Request models validate correctly
3. Response models match specifications
4. Error messages reference issue #36

Run tests:
```bash
pytest tests/test_resource_tools.py -v
```

## Next Steps

To implement these features (issue #36):

1. **Choose Storage Backend**: Decide on database/storage for tags and metadata
2. **Implement Data Models**: Create ORM models or data structures
3. **Add Business Logic**: Implement each endpoint with actual functionality
4. **Job Queue**: Set up async job processing (e.g., Celery, RQ)
5. **Update Tests**: Replace stubs with comprehensive tests
6. **Add Documentation**: Document implemented features with examples
7. **Security**: Add authentication and authorization
8. **Performance**: Add caching, indexing, and optimization

## API Reference

See the OpenAPI documentation at `/docs` when the server is running for full API reference including:

- Request/response schemas
- Validation rules
- Error codes
- Example payloads

## Contributing

When implementing these features:

- Follow existing code style and patterns
- Add comprehensive tests
- Update this documentation
- Consider backward compatibility
- Add appropriate logging
- Handle edge cases gracefully

## Support

For questions or issues:
- Open an issue on GitHub
- Reference issue #36 for implementation tracking
- Check existing tests for expected behavior
