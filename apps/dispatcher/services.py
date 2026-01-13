import logging
import threading
from typing import Iterable, List, Set

from django.db import transaction
from django.utils import timezone

from apps.boards.models import Board
from apps.dispatcher.models import TestRequest

logger = logging.getLogger(__name__)


def _cap_set_from_str(cap_str: str) -> Set[str]:
    if not cap_str:
        return set()
    return {cap for cap in cap_str.split(",") if cap}


def _cap_str_from_iterable(caps: Iterable[str]) -> str:
    return ",".join(sorted({cap.strip() for cap in caps if cap.strip()}))


class DispatcherService:
    """Scheduler that assigns queued TestRequests to available boards."""

    def __init__(self):
        self.lock = threading.Lock()

    def queue_requests(self, requests: List[dict]) -> List[TestRequest]:
        """Persist incoming requests and trigger scheduling."""
        to_create: List[TestRequest] = []
        for req in requests:
            to_create.append(
                TestRequest(
                    platform=req["platform"],
                    priority=req.get("priority", 0),
                    timeout=req.get("timeout", 600),
                    required_capabilities=_cap_str_from_iterable(req.get("required_capabilities", [])),
                )
            )
        created = TestRequest.objects.bulk_create(to_create)
        logger.info("Queued %s requests", len(created))
        self.schedule()
        return created

    def schedule(self):
        """Assign queued requests to idle boards."""
        with self.lock:
            with transaction.atomic():
                idle_boards = list(
                    Board.objects.select_for_update(skip_locked=True)
                    .filter(status="IDLE", is_locked=False)
                    .prefetch_related("capabilities")
                )
                queued_requests = list(
                    TestRequest.objects.select_for_update(skip_locked=True)
                    .filter(status="QUEUED")
                    .order_by("-priority", "created_at")
                )

                for board in idle_boards:
                    board_caps = set(board.capabilities.filter(is_active=True).values_list("name", flat=True))
                    match = self._find_best_request(board, board_caps, queued_requests)
                    if match:
                        queued_requests.remove(match)
                        self._dispatch(board, match)

    def _find_best_request(
        self, board: Board, board_caps: Set[str], queued_requests: List[TestRequest]
    ) -> TestRequest | None:
        for req in queued_requests:
            if req.platform != board.platform:
                continue
            required = _cap_set_from_str(req.required_capabilities)
            if required.issubset(board_caps):
                return req
        return None

    def _dispatch(self, board: Board, req: TestRequest):
        """Mark board busy and request running."""
        now = timezone.now()
        logger.info("Dispatching request %s to board %s", req.pk, board.pk)
        board.status = "BUSY"
        board.is_locked = True
        board.last_used_at = now
        board.save(update_fields=["status", "is_locked", "last_used_at"])
        req.status = "RUNNING"
        req.started_at = now
        req.executed_on_board = board
        req.save(update_fields=["status", "started_at", "executed_on_board"])

    def complete_request(self, request_id: int, success: bool = True):
        """Mark a request complete/failed and free the board."""
        with self.lock:
            with transaction.atomic():
                req = TestRequest.objects.select_for_update().get(pk=request_id)
                req.status = "DONE" if success else "FAILED"
                req.completed_at = timezone.now()
                req.save(update_fields=["status", "completed_at"])

                if req.executed_on_board_id:
                    Board.objects.filter(pk=req.executed_on_board_id).update(status="IDLE", is_locked=False)

        self.schedule()

    def status(self):
        queued = TestRequest.objects.filter(status="QUEUED").count()
        running = TestRequest.objects.filter(status="RUNNING").count()
        busy_boards = Board.objects.filter(status="BUSY").count()
        idle_boards = Board.objects.filter(status="IDLE", is_locked=False).count()
        return {
            "queued_requests": queued,
            "running_requests": running,
            "busy_boards": busy_boards,
            "idle_boards": idle_boards,
        }


dispatcher_service = DispatcherService()
