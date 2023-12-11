from enum import StrEnum


class JobGroupStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class JobStatus(StrEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
