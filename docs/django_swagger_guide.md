# Implementing Swagger/OpenAPI Documentation in Django

## Overview

This guide shows how to integrate Swagger/OpenAPI documentation into your Django REST Framework test management system using **drf-spectacular**, the modern and actively maintained solution for Django API documentation.

---

## Why drf-spectacular?

| Feature | drf-spectacular | django-rest-swagger |
|---------|-----------------|---------------------|
| **Maintenance** | Active (2024+) | Deprecated |
| **OpenAPI Version** | 3.0+ | 2.0 |
| **Schema Generation** | Automatic + Custom | Manual |
| **Integration** | Built-in with DRF | Separate library |
| **Features** | Rich, modern features | Basic |
| **Performance** | Optimized | Slower |

**Recommendation:** Use **drf-spectacular** for all new projects.

---

## Installation & Setup

### Step 1: Install drf-spectacular

```bash
pip install drf-spectacular
```

### Step 2: Update settings.py

Add to `INSTALLED_APPS`:

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',  # ← Add this
    'corsheaders',
    'django_filters',
    
    # Local apps
    'apps.authentication',
    'apps.boards',
    'apps.test_cases',
    'apps.test_execution',
    'apps.dashboard',
    'apps.configuration',
]
```

### Step 3: Configure REST Framework

```python
# config/settings.py

REST_FRAMEWORK = {
    # Schema generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Filtering & Pagination
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    
    # Other settings
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}
```

### Step 4: Add drf-spectacular Configuration

```python
# config/settings.py

SPECTACULAR_SETTINGS = {
    'TITLE': 'Test Management System API',
    'DESCRIPTION': 'Comprehensive API for managing test cases and execution on multiple hardware boards',
    'VERSION': '1.0.0',
    
    # Servers
    'SERVERS': [
        {
            'url': 'http://localhost:8000',
            'description': 'Local Development server',
        },
        {
            'url': 'https://api.example.com',
            'description': 'Production server',
        },
    ],
    
    # Contact & License
    'CONTACT': {
        'name': 'API Support',
        'email': 'support@example.com',
        'url': 'https://example.com/support',
    },
    'LICENSE': {
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
    
    # Security Schemes
    'AUTHENTICATION_PATTERN': 'Bearer {token}',
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATION_PARAMETERS': True,
    
    # Schema generation options
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE': False,
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.openapi.AutoSchema.postprocess_schema_enum_fields',
        'drf_spectacular.openapi.AutoSchema.postprocess_schema_default_responses',
    ],
    
    # Tags organization
    'TAGS': [
        {
            'name': 'Authentication',
            'description': 'User authentication and token management',
        },
        {
            'name': 'Boards',
            'description': 'Hardware board management and monitoring',
        },
        {
            'name': 'Test Cases',
            'description': 'Test case creation, editing, and management',
        },
        {
            'name': 'Test Execution',
            'description': 'Test execution, monitoring, and control',
        },
        {
            'name': 'Users',
            'description': 'User management (Admin only)',
        },
        {
            'name': 'Dashboard',
            'description': 'Analytics and dashboard endpoints',
        },
    ],
    
    # Metadata extensions
    'EXTENSIONS_TO_SCHEMA_FUNCTION': lambda generator, request, public: {
        'x-logo': {
            'url': 'https://example.com/logo.png',
            'altText': 'Test Management System',
        },
    },
}
```

### Step 5: Configure URLs

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Schema endpoints
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', 
         SpectacularSwaggerView.as_view(url_name='schema'), 
         name='swagger-ui'),
    path('api/v1/schema/redoc/', 
         SpectacularRedocView.as_view(url_name='schema'), 
         name='redoc'),
    
    # API endpoints
    path('api/v1/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.boards.urls')),
    path('api/v1/', include('apps.test_cases.urls')),
    path('api/v1/', include('apps.test_execution.urls')),
    path('api/v1/', include('apps.dashboard.urls')),
    path('api/v1/', include('apps.configuration.urls')),
]
```

---

## API Endpoint Documentation

### Method 1: Docstrings (Automatic)

drf-spectacular automatically extracts docstrings from your views:

```python
# apps/boards/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Board
from .serializers import BoardSerializer

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing hardware boards.
    
    Boards represent evaluation modules (EVMs) connected via UART ports.
    They can execute test cases and report real-time status updates.
    """
    
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_fields = ['connection_status', 'is_active', 'location']
    search_fields = ['name', 'serial_number', 'location']
    ordering_fields = ['created_at', 'name', 'connection_status']
    
    @extend_schema(
        description='Retrieve a list of all boards',
        parameters=[
            OpenApiParameter(
                name='connection_status',
                description='Filter by board connection status',
                required=False,
                enum=['CONNECTED', 'DISCONNECTED', 'OFFLINE', 'ERROR'],
            ),
            OpenApiParameter(
                name='is_active',
                description='Filter by active status',
                required=False,
                type=bool,
            ),
        ],
        tags=['Boards'],
    )
    def list(self, request, *args, **kwargs):
        """List all registered boards with filtering options."""
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        description='Retrieve details of a specific board',
        tags=['Boards'],
    )
    def retrieve(self, request, *args, **kwargs):
        """Get detailed information about a specific board."""
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        description='Get real-time board status',
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'board_id': {'type': 'integer'},
                    'status': {'type': 'string'},
                    'is_online': {'type': 'boolean'},
                    'last_heartbeat': {'type': 'string', 'format': 'date-time'},
                    'cpu_load': {'type': 'number'},
                    'temperature': {'type': 'number'},
                },
            },
        },
        tags=['Boards'],
    )
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get real-time status of a specific board."""
        board = self.get_object()
        return Response({
            'board_id': board.id,
            'status': board.connection_status,
            'is_online': board.connection_status == 'CONNECTED',
            'last_heartbeat': board.last_heartbeat,
        })
    
    @extend_schema(
        description='Get board activity logs',
        tags=['Boards'],
    )
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Retrieve activity logs for a specific board."""
        board = self.get_object()
        logs = board.boardlog_set.all().order_by('-created_at')
        return Response(logs.values())
    
    @extend_schema(
        description='Get capabilities supported by this board',
        tags=['Boards'],
    )
    @action(detail=True, methods=['get'])
    def capabilities(self, request, pk=None):
        """List all capabilities supported by this board."""
        board = self.get_object()
        capabilities = board.capabilities.all()
        return Response(
            {cap.id: cap.name for cap in capabilities}
        )
    
    @extend_schema(
        description='Lock board for exclusive use',
        request=None,
        responses={200: {'type': 'object', 'properties': {'is_locked': {'type': 'boolean'}}}},
        tags=['Boards'],
    )
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Lock a board to prevent concurrent test execution."""
        board = self.get_object()
        board.is_locked = True
        board.save()
        return Response({'is_locked': board.is_locked})
    
    @extend_schema(
        description='Unlock board',
        request=None,
        tags=['Boards'],
    )
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """Unlock a board."""
        board = self.get_object()
        board.is_locked = False
        board.save()
        return Response({'is_locked': board.is_locked})
```

### Method 2: @extend_schema Decorator

Use `@extend_schema` for detailed documentation:

```python
# apps/test_execution/views.py

from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

class TestRunViewSet(viewsets.ModelViewSet):
    """Manage test case execution on boards."""
    
    queryset = TestRun.objects.all()
    serializer_class = TestRunSerializer
    
    @extend_schema(
        summary='Start test execution',
        description='Initiate a new test run on a specific board',
        request=StartTestSerializer,
        responses={
            201: TestRunSerializer,
            400: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'},
                    'errors': {'type': 'object'},
                },
            },
            409: {
                'type': 'object',
                'properties': {
                    'detail': {
                        'type': 'string',
                        'example': 'Board is currently executing a test',
                    },
                },
            },
        },
        tags=['Test Execution'],
    )
    def create(self, request, *args, **kwargs):
        """
        Start a new test execution.
        
        The request must contain:
        - board_id: ID of the board to run test on
        - test_case_id: ID of the test case to execute
        - parameters (optional): Test-specific parameters
        
        The board must:
        - Be connected and online
        - Have all required capabilities
        - Not be locked by another user
        - Not be executing another test
        """
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        description='Pause ongoing test execution',
        request=None,
        responses={200: TestRunSerializer},
        tags=['Test Execution'],
    )
    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Pause a running test."""
        testrun = self.get_object()
        if testrun.status != 'IN_PROGRESS':
            return Response(
                {'detail': 'Only in-progress tests can be paused'},
                status=status.HTTP_400_BAD_REQUEST
            )
        testrun.pause()
        return Response(TestRunSerializer(testrun).data)
    
    @extend_schema(
        description='Resume paused test execution',
        request=None,
        responses={200: TestRunSerializer},
        tags=['Test Execution'],
    )
    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """Resume a paused test."""
        testrun = self.get_object()
        if testrun.status != 'PAUSED':
            return Response(
                {'detail': 'Only paused tests can be resumed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        testrun.resume()
        return Response(TestRunSerializer(testrun).data)
    
    @extend_schema(
        description='Kill/terminate test execution',
        request=None,
        responses={200: TestRunSerializer},
        tags=['Test Execution'],
    )
    @action(detail=True, methods=['post'])
    def kill(self, request, pk=None):
        """Forcefully terminate a test."""
        testrun = self.get_object()
        if testrun.status not in ['IN_PROGRESS', 'PAUSED']:
            return Response(
                {'detail': 'Only active tests can be killed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        testrun.kill()
        return Response(TestRunSerializer(testrun).data)
    
    @extend_schema(
        description='Get live test execution logs',
        responses={'200': {'type': 'string'}},
        tags=['Test Execution'],
    )
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Stream test output logs."""
        testrun = self.get_object()
        return Response(testrun.get_logs())
    
    @extend_schema(
        description='Get detailed test results',
        tags=['Test Execution'],
    )
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get assertion-level results."""
        testrun = self.get_object()
        results = testrun.results.all()
        return Response(
            TestResultSerializer(results, many=True).data
        )
```

---

## Custom Serializer Documentation

```python
# apps/test_execution/serializers.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import TestRun, TestResult

class TestResultSerializer(serializers.ModelSerializer):
    """Detailed result of a single assertion."""
    
    class Meta:
        model = TestResult
        fields = [
            'id',
            'assertion_name',
            'expected_value',
            'actual_value',
            'result_type',
            'error_message',
            'execution_time',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class TestRunSerializer(serializers.ModelSerializer):
    """Test execution instance with real-time updates."""
    
    board_name = serializers.CharField(
        source='board.name',
        read_only=True,
        help_text='Name of the hardware board'
    )
    test_case_name = serializers.CharField(
        source='test_case.name',
        read_only=True,
        help_text='Name of the test case'
    )
    results = TestResultSerializer(
        many=True,
        read_only=True,
        help_text='Assertion-level test results'
    )
    status = serializers.ChoiceField(
        choices=['PENDING', 'IN_PROGRESS', 'PAUSED', 'COMPLETED', 'FAILED', 'KILLED', 'ERROR'],
        help_text='Current execution status'
    )
    progress_percentage = serializers.IntegerField(
        help_text='Execution progress (0-100%)',
        min_value=0,
        max_value=100
    )
    
    class Meta:
        model = TestRun
        fields = [
            'id',
            'board_id',
            'board_name',
            'test_case_id',
            'test_case_name',
            'status',
            'progress_percentage',
            'current_assertion',
            'start_time',
            'end_time',
            'duration',
            'stdout_log',
            'stderr_log',
            'exit_code',
            'error_message',
            'result_summary',
            'results',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'board_name',
            'test_case_name',
            'start_time',
            'end_time',
            'duration',
            'stdout_log',
            'stderr_log',
            'exit_code',
            'created_at',
            'updated_at',
        ]
```

---

## Generating the OpenAPI Schema File

Run the management command to generate the OpenAPI schema:

```bash
# Generate YAML schema
python manage.py spectacular --file openapi.yaml

# Generate JSON schema
python manage.py spectacular --file openapi.json --format json
```

This creates a standalone file that can be shared or consumed by other tools.

---

## Accessing Documentation

After setup, access the documentation at:

### Swagger UI
```
http://localhost:8000/api/v1/schema/swagger-ui/
```

### ReDoc (Alternative UI)
```
http://localhost:8000/api/v1/schema/redoc/
```

### Raw OpenAPI Schema
```
http://localhost:8000/api/v1/schema/
```

---

## Advanced Configuration

### Custom Response Documentation

```python
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    responses={
        200: OpenApiResponse(
            description='Test completed successfully',
            response=TestRunSerializer,
        ),
        429: OpenApiResponse(
            description='Too many requests - rate limit exceeded',
            response={
                'type': 'object',
                'properties': {
                    'detail': {
                        'type': 'string',
                        'example': 'Request was throttled. Expected available in 60 seconds.',
                    },
                    'retry_after': {'type': 'integer'},
                },
            },
        ),
        500: OpenApiResponse(
            description='Internal server error',
            response={
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'},
                },
            },
        ),
    }
)
def create(self, request):
    pass
```

### Request/Response Examples

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    request=StartTestSerializer,
    responses=TestRunSerializer,
    examples=[
        OpenApiExample(
            'Success Example',
            value={
                'board_id': 1,
                'test_case_id': 5,
                'parameters': {
                    'timeout': 30,
                    'retry_count': 3,
                },
            },
            request_only=True,
        ),
    ],
)
def create(self, request):
    pass
```

### Operation-Level Tags & Summary

```python
@extend_schema(
    summary='Execute Test',
    description='Start a new test run on a specified board with detailed execution control',
    tags=['Test Execution'],
    operation_id='test_runs_create',
)
def create(self, request):
    pass
```

---

## Authentication Documentation

```python
# config/settings.py

SPECTACULAR_SETTINGS = {
    # ... other settings ...
    
    # Authentication scheme configuration
    'SECURITY': [
        {
            'bearerAuth': []
        }
    ],
    
    'COMPONENTS': {
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Enter your JWT token',
            },
        },
    },
}
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/generate-api-docs.yml

name: Generate API Documentation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Generate OpenAPI schema
      run: |
        python manage.py spectacular --file openapi.yaml
    
    - name: Upload schema artifact
      uses: actions/upload-artifact@v2
      with:
        name: openapi-schema
        path: openapi.yaml
    
    - name: Commit schema changes
      if: github.ref == 'refs/heads/main'
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add openapi.yaml
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update API documentation" && git push)
```

---

## Schema Customization

### Exclude Endpoints from Documentation

```python
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)  # Hide from schema
def some_internal_view(request):
    pass
```

### Organize Endpoints with Tags

```python
SPECTACULAR_SETTINGS = {
    'TAGS': [
        {
            'name': 'Authentication',
            'description': 'User authentication and token management',
            'externalDocs': {
                'description': 'Learn more',
                'url': 'https://docs.example.com/auth',
            },
        },
        {
            'name': 'Boards',
            'description': 'Hardware board management',
        },
        {
            'name': 'Test Execution',
            'description': 'Test execution lifecycle',
        },
    ],
}
```

### Custom Field Descriptions

```python
class BoardSerializer(serializers.ModelSerializer):
    connection_status = serializers.CharField(
        help_text='Current connection status: CONNECTED, DISCONNECTED, OFFLINE, or ERROR',
        read_only=True,
    )
    baud_rate = serializers.IntegerField(
        help_text='UART baud rate (default: 115200)',
        default=115200,
    )
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'connection_status', 'baud_rate']
```

---

## Testing Documentation

```python
# tests/test_schema.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class SchemaTestCase(TestCase):
    """Test API schema generation."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_schema_generation(self):
        """Verify OpenAPI schema is accessible."""
        response = self.client.get('/api/v1/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('openapi', response.json())
    
    def test_swagger_ui_accessible(self):
        """Verify Swagger UI is accessible."""
        response = self.client.get('/api/v1/schema/swagger-ui/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_redoc_accessible(self):
        """Verify ReDoc is accessible."""
        response = self.client.get('/api/v1/schema/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

---

## Troubleshooting

### Issue: TypeError on Field Validation

**Cause:** Foreign key fields not properly serialized

**Solution:**
```python
class BoardSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'created_by']
```

### Issue: Missing Documentation for Custom Actions

**Solution:** Use `@extend_schema` on custom actions:
```python
@extend_schema(
    description='Your custom action description',
    tags=['Your Tag'],
)
@action(detail=True, methods=['post'])
def custom_action(self, request, pk=None):
    pass
```

### Issue: Complex Nested Responses

**Solution:** Create separate serializers:
```python
class NestedSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()

class MainSerializer(serializers.Serializer):
    nested = NestedSerializer()
```

---

## Production Best Practices

1. **Version Your API:** Use semantic versioning in `VERSION` setting
2. **Document Breaking Changes:** Maintain changelog for API versions
3. **Use Authentication Schemes:** Properly document auth requirements
4. **Rate Limiting:** Document rate limits in schema
5. **Error Responses:** Document all possible error codes
6. **Examples:** Provide realistic examples for all endpoints
7. **Server URLs:** List all available server environments

---

## Integration with Frontend

Your React frontend can consume the schema:

```typescript
// src/services/api/openapi.ts

export async function fetchOpenAPISchema() {
  const response = await fetch('http://localhost:8000/api/v1/schema/');
  return response.json();
}

// Use Swagger UI in React
import SwaggerUI from "swagger-ui-react"
import "swagger-ui-react/swagger-ui.css"

export const APIDocumentation = () => (
  <SwaggerUI url="http://localhost:8000/api/v1/schema/" />
)
```

---

## Summary

| Step | Command/Action |
|------|---|
| **Install** | `pip install drf-spectacular` |
| **Configure** | Add to `INSTALLED_APPS` and `REST_FRAMEWORK` |
| **Add URLs** | Include schema endpoints |
| **Document** | Use `@extend_schema` decorator |
| **Generate** | `python manage.py spectacular --file openapi.yaml` |
| **View** | Visit `/api/v1/schema/swagger-ui/` |

drf-spectacular automatically generates OpenAPI 3.0 documentation from your DRF views, decorators, and serializers, making your API fully documented with minimal effort.
