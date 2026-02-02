import os
import redis
from rq import Queue
from datetime import timedelta
from typing import Any, Dict
from ....contracts.heresy_contracts import ArtisanHeresy


class TaskEngine:
    """
    [THE KINETIC DISPATCHER]
    Wraps Redis Queue (RQ) to manage the flow of background time.
    """
    _redis_conn = None

    @classmethod
    def get_redis(cls):
        if not cls._redis_conn:
            url = os.environ.get("REDIS_URL", "redis://localhost:6379")
            cls._redis_conn = redis.from_url(url)
        return cls._redis_conn

    def execute(self, request) -> Any:
        conn = self.get_redis()
        q = Queue(request.queue, connection=conn)

        # 1. Delayed / Scheduled
        if request.delay_seconds > 0:
            job = q.enqueue_in(
                timedelta(seconds=request.delay_seconds),
                request.task,
                *request.args,
                **request.kwargs,
                job_timeout=request.timeout,
                retry=self._get_retry(request)
            )
            return {"status": "scheduled", "job_id": job.get_id(), "eta": f"+{request.delay_seconds}s"}

        # 2. Specific Time
        elif request.schedule_at:
            job = q.enqueue_at(
                request.schedule_at,
                request.task,
                *request.args,
                **request.kwargs,
                job_timeout=request.timeout,
                retry=self._get_retry(request)
            )
            return {"status": "scheduled", "job_id": job.get_id(), "at": request.schedule_at.isoformat()}

        # 3. Immediate Enqueue
        else:
            job = q.enqueue(
                request.task,
                *request.args,
                **request.kwargs,
                job_timeout=request.timeout,
                retry=self._get_retry(request)
            )
            return {"status": "enqueued", "job_id": job.get_id(), "position": len(q)}

    def _get_retry(self, request):
        from rq import Retry
        return Retry(max=request.retries)