import time
from dataclasses import dataclass, field


@dataclass
class MetricsTracker:
    start_time: float = field(default_factory=time.time)
    total_tokens: int = 0
    model: str = ""

    def add_tokens(self, prompt_tokens: int, completion_tokens: int):
        self.total_tokens += prompt_tokens + completion_tokens

    @property
    def latency_ms(self) -> float:
        return (time.time() - self.start_time) * 1000
