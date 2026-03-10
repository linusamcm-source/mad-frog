from dataclasses import dataclass, field
from enum import Enum


class Phase(Enum):
    DISCOVERY = "discovery"
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"


@dataclass
class Decision:
    id: str
    phase: Phase
    summary: str
    rationale: str


@dataclass
class Checkpoint:
    phase: Phase
    timestamp: str
    label: str
    metadata: dict = field(default_factory=dict)


@dataclass
class ProjectRecord:
    name: str
    workspace: str
    current_phase: Phase = Phase.DISCOVERY
    decisions: list[Decision] = field(default_factory=list)
    checkpoints: list[Checkpoint] = field(default_factory=list)
