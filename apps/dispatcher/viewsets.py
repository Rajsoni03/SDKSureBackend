from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.dispatcher.models import TestRequest
from apps.dispatcher.serializers import (
    CompleteRequestSerializer,
    DispatchRequestSerializer,
    TestRequestSerializer,
)
from apps.dispatcher.services import dispatcher_service


class DispatcherViewSet(viewsets.ViewSet):
    """Submit dispatch requests and inspect dispatcher state."""

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Return current dispatcher status and recent requests."""
        qs = TestRequest.objects.order_by("-created_at")[:50]
        return Response({"status": dispatcher_service.status(), "recent_requests": TestRequestSerializer(qs, many=True).data})

    def create(self, request):
        """Submit a batch of requests for scheduling."""
        payload = request.data.get("requests") if isinstance(request.data, dict) else request.data
        if not isinstance(payload, list):
            return Response(
                {"detail": "Send a list of requests or wrap them under the 'requests' key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DispatchRequestSerializer(data=payload, many=True)
        serializer.is_valid(raise_exception=True)

        created = dispatcher_service.queue_requests(serializer.validated_data)
        return Response(
            {
                "queued": len(created),
                "request_ids": [req.pk for req in created],
                "status": dispatcher_service.status(),
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=["post"])
    def complete(self, request):
        """Mark a request done/failed and free the board."""
        serializer = CompleteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dispatcher_service.complete_request(
            request_id=serializer.validated_data["request_id"],
            success=serializer.validated_data.get("success", True),
        )
        return Response(dispatcher_service.status())

    @action(detail=False, methods=["post"])
    def reschedule(self, _request):
        """Manually trigger scheduling."""
        dispatcher_service.schedule()
        return Response(dispatcher_service.status())
