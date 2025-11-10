# Resource Tools Documentation

## Overview

This document describes the higher-level resource management features provided by Savrli AI. These tools complement the core resource storage implementation (issue #36) by providing integration points for tagging, metadata management, and import/export workflows.

## Table of Contents

1. [Architecture](#architecture)
2. [Tagging System](#tagging-system)
3. [Metadata Management](#metadata-management)
4. [Import/Export Workflows](#importexport-workflows)
5. [Dashboard Integration](#dashboard-integration)
6. [API Reference](#api-reference)
7. [Future Enhancements](#future-enhancements)

---

## Architecture

The resource tools system is designed as a lightweight layer on top of the core resource storage. It provides:

- **Separation of Concerns**: Business logic for tagging, metadata, and import/export is separate from core storage
- **Extensibility**: Easy to add new resource management features without modifying core code
- **API-First Design**: All features are exposed via REST endpoints for easy integration

### Component Overview

```
┌─────────────────────────────────────┐
│      Dashboard/Frontend Apps       │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│    Resource Tools API Endpoints     │
│  (/api/resource-tools/*)            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Core Resource Storage (issue #36) │
│   (resource_manager.py)             │
└─────────────────────────────────────┘
```

---

## Tagging System

The tagging system allows resources (conversations, sessions, etc.) to be organized with user-defined labels.

### Use Cases

- Categorize conversations by topic (e.g., "customer-support", "sales", "technical")
- Filter resources in dashboards and analytics
- Enable quick search and retrieval
- Support bulk operations on tagged resources

### API Endpoints

#### Add Tags
```http
POST /api/resource-tools/tags/add
Content-Type: application/json

{
  "resource_id": "session-123",
  "tags": ["customer-support", "high-priority"]
}
```

**Response:**
```json
{
  "success": true,
  "resource_id": "session-123",
  "tags": ["customer-support", "high-priority"],
  "message": "Tags added successfully"
}
```

#### Remove Tags
```http
POST /api/resource-tools/tags/remove
Content-Type: application/json

{
  "resource_id": "session-123",
  "tags": ["high-priority"]
}
```

#### Get Tags
```http
GET /api/resource-tools/tags/session-123
```

**Response:**
```json
{
  "success": true,
  "resource_id": "session-123",
  "tags": ["customer-support"]
}
```

### Tag Best Practices

- Use lowercase, hyphenated tags for consistency (e.g., "customer-support" not "Customer Support")
- Limit to 5-10 tags per resource for optimal performance
- Define a tag taxonomy for your organization
- Use hierarchical tags when appropriate (e.g., "support:billing", "support:technical")

---

## Metadata Management

Metadata provides flexible key-value storage for resource attributes beyond the core data model.

### Metadata Schema

While metadata is flexible, recommended fields include:

```json
{
  "created_by": "user@example.com",
  "department": "sales",
  "priority": "high",
  "region": "us-east",
  "custom_field_1": "value1",
  "last_modified_by": "admin@example.com",
  "business_unit": "enterprise"
}
```

### API Endpoints

#### Update Metadata
```http
POST /api/resource-tools/metadata/update
Content-Type: application/json

{
  "resource_id": "session-123",
  "metadata": {
    "priority": "high",
    "region": "us-west",
    "created_by": "user@example.com"
  }
}
```

**Response:**
```json
{
  "success": true,
  "resource_id": "session-123",
  "metadata": {
    "priority": "high",
    "region": "us-west",
    "created_by": "user@example.com"
  },
  "updated_at": "2024-11-10T19:14:54.123Z"
}
```

#### Get Metadata
```http
GET /api/resource-tools/metadata/session-123
```

#### Delete Metadata
```http
DELETE /api/resource-tools/metadata/session-123?keys=priority,region
```

### Metadata Best Practices

- **Indexing**: Index frequently queried metadata fields for better performance
- **Validation**: Implement schema validation for critical metadata fields
- **Versioning**: Consider tracking metadata history for audit trails
- **Size Limits**: Keep individual metadata values under 1KB for optimal performance

---

## Import/Export Workflows

Import/export functionality enables data portability and integration with external systems.

### Supported Formats

| Format | Import | Export | Use Case |
|--------|--------|--------|----------|
| JSON | ✅ | ✅ | API integration, backups |
| CSV | ✅ | ✅ | Spreadsheet analysis, bulk uploads |
| Markdown | ❌ | ✅ | Documentation, reports |

### Export Workflow

```http
POST /api/resource-tools/export
Content-Type: application/json

{
  "resource_ids": ["session-1", "session-2", "session-3"],
  "format": "json",
  "options": {
    "include_metadata": true,
    "include_tags": true,
    "pretty": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "operation": "export",
  "count": 3,
  "message": "Export completed successfully",
  "data": {
    "sessions": [...],
    "exported_at": "2024-11-10T19:14:54.123Z"
  }
}
```

### Import Workflow

```http
POST /api/resource-tools/import
Content-Type: application/json

{
  "source": "json",
  "data": "{\"sessions\": [...]}",
  "options": {
    "overwrite": false,
    "validate": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "operation": "import",
  "count": 5,
  "message": "Imported 5 resources successfully"
}
```

### Export/Import Best Practices

- **Validation**: Always validate imported data before committing
- **Batching**: Process large exports/imports in batches to avoid timeouts
- **Error Handling**: Implement partial success handling for bulk operations
- **Versioning**: Include schema version in export data for compatibility

---

## Dashboard Integration

The resource tools API is designed to integrate seamlessly with dashboard applications.

### Integration Points

#### 1. Resource Listing with Filters

Dashboard can query resources filtered by tags and metadata:

```javascript
// Example dashboard integration
async function loadDashboardData() {
  const resources = await fetch('/api/resources?tags=customer-support&metadata.priority=high');
  const data = await resources.json();
  
  // Render in dashboard UI
  renderResourceTable(data.resources);
}
```

#### 2. Bulk Operations

Dashboard can perform bulk tagging or metadata updates:

```javascript
async function bulkAddTags(resourceIds, tags) {
  const promises = resourceIds.map(id => 
    fetch('/api/resource-tools/tags/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resource_id: id, tags })
    })
  );
  await Promise.all(promises);
}
```

#### 3. Export for Analysis

Dashboard can trigger exports for external analysis:

```javascript
async function exportToCSV(filters) {
  const response = await fetch('/api/resource-tools/export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resource_ids: filters.selectedIds,
      format: 'csv'
    })
  });
  const data = await response.json();
  downloadFile(data.data, 'export.csv');
}
```

### Dashboard Features Enabled

- **Tag Cloud**: Visual representation of popular tags
- **Metadata Editor**: In-line editing of resource metadata
- **Bulk Actions**: Multi-select and bulk tag/metadata operations
- **Export Tools**: One-click export to various formats
- **Import Wizard**: Step-by-step import from external sources

---

## API Reference

### Base URL

```
Production: https://your-deployment.vercel.app/api/resource-tools
Local: http://localhost:8000/api/resource-tools
```

### Authentication

All endpoints require the same authentication as the main Savrli AI API. Include authentication headers as needed:

```http
Authorization: Bearer YOUR_API_TOKEN
```

### Response Format

All endpoints return JSON with a consistent structure:

```json
{
  "success": boolean,
  "message": "string (optional)",
  "data": {} // endpoint-specific data
}
```

### Error Handling

Errors follow HTTP status codes:

- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "success": false,
  "error": "Error message",
  "details": {} // optional error details
}
```

---

## Future Enhancements

### Phase 2 Features

1. **Advanced Search**
   - Full-text search across tags and metadata
   - Boolean operators for complex queries
   - Saved search filters

2. **Tag Hierarchies**
   - Nested tag support (e.g., "support:billing:refunds")
   - Tag relationships and synonyms
   - Auto-tagging based on content

3. **Metadata Schemas**
   - Define required vs. optional metadata fields
   - Type validation (string, number, date, etc.)
   - Custom validation rules

4. **Scheduled Exports**
   - Automatic exports on a schedule
   - Export to cloud storage (S3, GCS, etc.)
   - Email delivery of exports

5. **Import Templates**
   - Pre-built import templates for common sources
   - Custom field mapping
   - Data transformation pipelines

### Phase 3 Features

1. **Resource Analytics**
   - Usage statistics by tag/metadata
   - Trend analysis over time
   - Resource lifecycle tracking

2. **Collaborative Features**
   - Shared tags across users/teams
   - Tag suggestions based on content
   - Collaborative metadata editing

3. **API Versioning**
   - Support for multiple API versions
   - Graceful deprecation of old versions
   - Migration tools for version upgrades

---

## Contributing

To contribute to the resource tools system:

1. Review the core resource storage implementation in `resource_manager.py`
2. Follow the API patterns established in `api/resource_tools.py`
3. Add tests in `tests/test_resource_tools.py`
4. Update this documentation with new features

---

## Related Documentation

- [Integration API](INTEGRATION_API.md) - Plugin system and integrations
- [Quick Start Guide](QUICKSTART.md) - Getting started with Savrli AI
- Issue #36 - Core resource storage implementation

---

## Support

For questions or issues with resource tools:

- Create an issue in the GitHub repository
- Review existing issues for similar problems
- Check the main README for general API documentation
