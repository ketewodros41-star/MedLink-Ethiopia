from __future__ import annotations

from collections import defaultdict


class MetricsRegistry:
    def __init__(self) -> None:
        self.counters: dict[str, int] = defaultdict(int)
        self.latency_totals_ms: dict[str, float] = defaultdict(float)
        self.latency_counts: dict[str, int] = defaultdict(int)

    def incr(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def observe_latency(self, name: str, duration_ms: float) -> None:
        self.latency_totals_ms[name] += duration_ms
        self.latency_counts[name] += 1

    def snapshot(self) -> dict:
        return {
            "counters": dict(self.counters),
            "latency_ms": {
                name: {
                    "count": self.latency_counts[name],
                    "total_ms": round(total, 2),
                    "avg_ms": round(total / self.latency_counts[name], 2) if self.latency_counts[name] else 0.0,
                }
                for name, total in self.latency_totals_ms.items()
            },
        }


metrics_registry = MetricsRegistry()
