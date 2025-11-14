# Resource Tools - Higher-Level Resource & Content Management

This document describes the higher-level resource and content management tools that complement the core resource management functionality (see issue #36).

## Overview

The Resource Tools API provides lightweight helper endpoints for:
- **Tagging**: Organize conversations with tags for better categorization
- **Metadata Management**: Store and query custom metadata for sessions
- **Import/Export Triggers**: Schedule and trigger background import/export operations

These tools work alongside the core resource management in `resource_manager.py` and will integrate with the persistent storage backend being developed in issue #36.

## Architecture

```
┌─────────────────────────────────────────────┐
│         API Layer (FastAPI)                 │
│    /api/resource-tools/* endpoints          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│      Resource Tools (resource_tools.py)     │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ │
│  │   Tag    │ │ Metadata │ │ Import/     │ │
│  │ Manager  │ │ Manager  │ │ Export      │ │
│  │          │ │          │ │ Triggers    │ │
│  └──────────┘ └──────────┘ └─────────────┘ │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  Core Resource Manager (resource_manager.py)│
│  ConversationExporter / Importer            │
│  SessionManager                             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│    Storage Backend (TODO: issue #36)        │
│    Persistent storage for conversations,    │
│    tags, metadata, and job queue            │
└─────────────────────────────────────────────┘
```

## API Endpoints

### Tagging Endpoints

#### Add Tag to Session
```http
POST /api/resource-tools/tags
Content-Type: application/json

{
  "session_id": "session_123",
  "tag": "important",
  "metadata": {
    "added_by": "user@example.com",
    "reason": "high priority conversation"
  }
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_123",
  "tag": "important",
  "message": "Tag added successfully"
}
```

#### Remove Tag from Session
```http
DELETE /api/resource-tools/tags
Content-Type: application/json

{
  "session_id": "session_123",
  "tag": "important"
}
```

#### Get Tags for Session
```http
GET /api/resource-tools/tags/{session_id}
```

**Response:**
```json
{
  "session_id": "session_123",
  "tags": ["important", "customer-support", "resolved"],
  "count": 3
}
```

#### Find Sessions by Tag
```http
GET /api/resource-tools/tags/search?tag=important
```

**Response:**
```json
{
  "tag": "important",
  "sessions": ["session_123", "session_456", "session_789"],
  "count": 3
}
```

### Metadata Management Endpoints

#### Set Session Metadata
```http
POST /api/resource-tools/metadata
Content-Type: application/json

{
  "session_id": "session_123",
  "metadata": {
    "customer_id": "cust_456",
    "priority": "high",
    "department": "sales",
    "custom_field": "value"
  }
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_123",
  "message": "Metadata updated successfully"
}
```

#### Get Session Metadata
```http
GET /api/resource-tools/metadata/{session_id}
```

**Response:**
```json
{
  "session_id": "session_123",
  "metadata": {
    "customer_id": "cust_456",
    "priority": "high",
    "department": "sales",
    "custom_field": "value",
    "last_updated": "2025-01-10T12:00:00Z"
  }
}
```

#### Delete Session Metadata
```http
DELETE /api/resource-tools/metadata/{session_id}
```

Optional query parameters:
- `keys`: Comma-separated list of specific metadata keys to delete

#### Search Sessions by Metadata
```http
POST /api/resource-tools/metadata/search
Content-Type: application/json

{
  "filters": {
    "priority": "high",
    "department": "sales"
  }
}
```

**Response:**
```json
{
  "filters": {
    "priority": "high",
    "department": "sales"
  },
  "sessions": ["session_123", "session_456"],
  "count": 2
}
```

### Import/Export Trigger Endpoints

#### Schedule Export
```http
POST /api/resource-tools/export/schedule
Content-Type: application/json

{
  "session_id": "session_123",
  "format": "json",
  "destination": "s3://bucket/exports/session_123.json",
  "schedule": "0 0 * * *"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "export_session_123_1234567890.123",
  "status": "pending",
  "message": "Export scheduled successfully"
}
```

#### Trigger Import
```http
POST /api/resource-tools/import/trigger
Content-Type: application/json

{
  "source": "s3://bucket/imports/conversation.json",
  "format": "json",
  "target_session_id": "new_session_456"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "import_1234567890.123",
  "status": "pending",
  "message": "Import triggered successfully"
}
```

#### Get Job Status
```http
GET /api/resource-tools/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "export_session_123_1234567890.123",
  "status": "completed",
  "session_id": "session_123",
  "format": "json",
  "destination": "s3://bucket/exports/session_123.json",
  "created_at": "2025-01-10T12:00:00Z",
  "completed_at": "2025-01-10T12:00:05Z"
}
```

#### Cancel Job
```http
DELETE /api/resource-tools/jobs/{job_id}
```

## Metadata Schema

### Standard Metadata Fields

While metadata is flexible and accepts custom fields, these standard fields are recommended:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `customer_id` | string | Customer identifier | `"cust_12345"` |
| `user_id` | string | User identifier | `"user_67890"` |
| `priority` | string | Priority level | `"high"`, `"medium"`, `"low"` |
| `department` | string | Department/team | `"sales"`, `"support"`, `"engineering"` |
| `category` | string | Conversation category | `"support"`, `"feedback"`, `"inquiry"` |
| `language` | string | Conversation language | `"en"`, `"es"`, `"fr"` |
| `sentiment` | string | Overall sentiment | `"positive"`, `"negative"`, `"neutral"` |
| `resolved` | boolean | Resolution status | `true`, `false` |
| `created_by` | string | Creator identifier | `"user@example.com"` |
| `last_updated` | string (ISO 8601) | Last update timestamp | `"2025-01-10T12:00:00Z"` |

### Custom Metadata

You can add any custom metadata fields specific to your use case:

```json
{
  "session_id": "session_123",
  "metadata": {
    "project_name": "Q1 Campaign",
    "budget_allocated": 5000,
    "stakeholders": ["alice@example.com", "bob@example.com"],
    "custom_tags": {
      "urgency": "high",
      "visibility": "internal"
    }
  }
}
```

## Import/Export Workflows

### Workflow 1: Scheduled Daily Exports

Export all active sessions to cloud storage every day:

1. **Schedule Exports**: Use cron expression `0 0 * * *` (midnight daily)
2. **Storage**: Export to S3, Azure Blob, or Google Cloud Storage
3. **Format**: JSON for full fidelity, CSV for analytics
4. **Monitoring**: Query job status via `/api/resource-tools/jobs/{job_id}`

```bash
# Schedule export for a session
curl -X POST http://localhost:8000/api/resource-tools/export/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "format": "json",
    "destination": "s3://my-bucket/exports/session_123.json",
    "schedule": "0 0 * * *"
  }'
```

### Workflow 2: Webhook-Triggered Imports

Import conversations from external systems via webhooks:

1. **Webhook Endpoint**: Configure external system to POST to `/api/resource-tools/import/trigger`
2. **Source**: Provide URL or cloud storage path
3. **Format**: JSON or CSV
4. **Processing**: Asynchronous import with status tracking

```bash
# Trigger import from webhook
curl -X POST http://localhost:8000/api/resource-tools/import/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "source": "https://external-system.com/export/conversation.json",
    "format": "json",
    "target_session_id": "imported_session_456"
  }'
```

### Workflow 3: Batch Export for Analytics

Export tagged sessions for batch analytics:

1. **Tag Sessions**: Tag sessions for export (e.g., "analytics", "Q1-2025")
2. **Find Tagged**: Use `/api/resource-tools/tags/search?tag=analytics`
3. **Bulk Export**: Schedule exports for all tagged sessions
4. **Dashboard**: Import into analytics dashboard or data warehouse

### Workflow 4: Cross-Platform Migration

Migrate conversations between platforms or environments:

1. **Export**: Export from source environment using `/ai/sessions/export`
2. **Transform**: Apply any necessary transformations
3. **Import**: Import to target environment using `/api/resource-tools/import/trigger`
4. **Metadata**: Preserve metadata and tags during migration

## Dashboard Integration

### Integration Points

The Resource Tools API integrates with the dashboard at `/dashboard` for:

1. **Tag Management UI**: Visual interface for adding/removing tags
2. **Metadata Editor**: Form-based metadata editing
3. **Import/Export Manager**: Track and manage scheduled jobs
4. **Search Interface**: Search sessions by tags and metadata

### Dashboard Features (TODO: issue #36)

- **Tag Cloud**: Visual representation of most-used tags
- **Metadata Filters**: Filter sessions by metadata in real-time
- **Job Monitor**: Real-time job status with progress bars
- **Export History**: View past exports with download links
- **Import Queue**: Manage pending import operations

### API Integration Example

```javascript
// Dashboard JavaScript example
async function addTagToSession(sessionId, tag) {
  const response = await fetch('/api/resource-tools/tags', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, tag: tag })
  });
  return response.json();
}

async function searchByMetadata(filters) {
  const response = await fetch('/api/resource-tools/metadata/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filters: filters })
  });
  return response.json();
}

async function scheduleExport(sessionId, format, destination) {
  const response = await fetch('/api/resource-tools/export/schedule', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      format: format,
      destination: destination
    })
  });
  return response.json();
}
```

## Current Implementation Status

### Implemented (Stubs)
- ✅ `TagManager` class with in-memory storage
- ✅ `MetadataManager` class with basic operations
- ✅ `ImportExportTriggerManager` class with job tracking
- ✅ API endpoint stubs (to be added to `api/index.py`)
- ✅ Documentation and workflow descriptions

### TODO (issue #36)
- ⏳ Persistent storage backend integration
- ⏳ Background job queue for imports/exports
- ⏳ Webhook handlers for external triggers
- ⏳ Dashboard UI components
- ⏳ Advanced search with indexes and queries
- ⏳ Cloud storage integrations (S3, Azure, GCS)
- ⏳ Cron-based scheduling system
- ⏳ Job retry logic and error handling
- ⏳ Export/import progress tracking
- ⏳ Validation schemas for metadata

## Usage Examples

### Example 1: Tag and Export Customer Support Conversations

```python
import requests

BASE_URL = "http://localhost:8000"

# Tag support conversations
sessions = ["session_123", "session_456", "session_789"]
for session_id in sessions:
    requests.post(f"{BASE_URL}/api/resource-tools/tags", json={
        "session_id": session_id,
        "tag": "customer-support"
    })

# Find all support sessions
response = requests.get(f"{BASE_URL}/api/resource-tools/tags/search?tag=customer-support")
support_sessions = response.json()["sessions"]

# Schedule daily exports
for session_id in support_sessions:
    requests.post(f"{BASE_URL}/api/resource-tools/export/schedule", json={
        "session_id": session_id,
        "format": "json",
        "destination": f"s3://support-bucket/{session_id}.json",
        "schedule": "0 0 * * *"
    })
```

### Example 2: Metadata-Based Analytics

```python
import requests

BASE_URL = "http://localhost:8000"

# Set metadata for sessions
sessions_metadata = {
    "session_123": {"priority": "high", "department": "sales"},
    "session_456": {"priority": "high", "department": "engineering"},
    "session_789": {"priority": "low", "department": "sales"}
}

for session_id, metadata in sessions_metadata.items():
    requests.post(f"{BASE_URL}/api/resource-tools/metadata", json={
        "session_id": session_id,
        "metadata": metadata
    })

# Search for high-priority sales conversations
response = requests.post(f"{BASE_URL}/api/resource-tools/metadata/search", json={
    "filters": {"priority": "high", "department": "sales"}
})

high_priority_sales = response.json()["sessions"]
print(f"Found {len(high_priority_sales)} high-priority sales conversations")
```

## Security Considerations

### Authentication & Authorization
- TODO (issue #36): Implement authentication for resource tools endpoints
- Recommended: Use API keys or JWT tokens
- Role-based access control for tag/metadata management

### Data Privacy
- Ensure exported data complies with privacy regulations (GDPR, CCPA)
- Implement data anonymization options for exports
- Secure storage credentials and access tokens

### Rate Limiting
- TODO (issue #36): Implement rate limiting for import/export operations
- Prevent abuse of scheduled exports
- Queue management for concurrent operations

## Performance Considerations

### Scalability
- Current implementation uses in-memory storage (not production-ready)
- TODO (issue #36): Migrate to scalable database (PostgreSQL, MongoDB)
- Implement caching for frequently accessed tags and metadata

### Optimization
- Index metadata fields for fast searching
- Batch operations for bulk tag/metadata updates
- Async processing for large imports/exports

## Related Documentation

- [Integration API](INTEGRATION_API.md) - Platform integration guides
- [Plugin Examples](PLUGIN_EXAMPLES.md) - Plugin development examples
- [Quickstart Guide](QUICKSTART.md) - Getting started with Savrli AI
- Issue #36 - Core storage backend implementation (GitHub)

## Support

For questions or issues related to Resource Tools:
1. Check this documentation
2. Review issue #36 for core implementation details
3. Open a GitHub issue with label `resource-management`
4. Contact the development team

---

**Note**: This is scaffolding documentation. Full implementation will be completed in issue #36.
