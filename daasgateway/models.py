import asyncio
from typing import List, Dict, Any, NoReturn, Optional
from uuid import UUID

from pydantic import BaseModel, PrivateAttr, Field

from daasgateway.services import DaaSGatewayAPIService
from daasgateway.enums import JobStatus, JobGroupStatus


class JobGroup(BaseModel):
    uuid: UUID
    status: JobGroupStatus = Field(default=JobGroupStatus.PENDING)

    _jobs: List["Job"] = PrivateAttr(default_factory=list)

    @property
    def jobs(self) -> List["Job"]:
        return self._jobs

    @property
    def failed_jobs(self) -> List["Job"]:
        return [job for job in self._jobs if job.status == JobStatus.FAILED]

    @property
    def num_failed_jobs(self) -> int:
        return len(self.failed_jobs)

    async def wait_until_completed(
        self, poll_interval: float = 1.0, timeout: float = 60.0
    ) -> NoReturn:
        async with asyncio.timeout(timeout):
            while self.status != JobGroupStatus.COMPLETED:
                job_group_data = await DaaSGatewayAPIService.get_job_group_status(
                    self.uuid
                )
                self._parse_data(job_group_data)
                await asyncio.sleep(poll_interval)

    def _parse_data(self, data: Dict[str, Any]) -> NoReturn:
        self.status = JobGroupStatus(data["job_group_status"])
        self._jobs = [
            Job(
                job_group_uuid=self.uuid,
                uuid=job_data["uuid"],
                status=JobStatus(job_data["job_status"]),
                status_code=job_data["job_status_code"],
            )
            for job_data in data["jobs"]
        ]


class Job(BaseModel):
    job_group_uuid: UUID
    uuid: UUID
    status: JobStatus = Field(default=JobStatus.PENDING)
    status_code: Optional[int] = Field(default=None)

    _payload: Optional[Dict[str, Any]] = PrivateAttr(default=None)
    _response: Optional[Dict[str, Any]] = PrivateAttr(default=None)

    @property
    async def payload(self) -> Dict[str, Any]:
        if not self._payload:
            self._payload = await DaaSGatewayAPIService.get_job_request_payload(
                self.job_group_uuid, self.uuid
            )
        return self._payload

    @property
    async def response(self) -> Dict[str, Any]:
        if not self._response:
            self._response = await DaaSGatewayAPIService.get_job_response(
                self.job_group_uuid, self.uuid
            )
        return self._response
