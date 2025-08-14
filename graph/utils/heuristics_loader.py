from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

import json

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


@dataclass(frozen=True)
class TimeSpec:
    min: int
    max: Optional[int] = None

    def validate(self) -> None:
        if self.min < 0:
            raise ValueError("time.min must be >= 0")
        if self.max is not None and self.max < self.min:
            raise ValueError("time.max must be >= time.min")


@dataclass(frozen=True)
class HeuristicSpec:
    reward: Tuple[int, int]
    time: TimeSpec

    def validate(self) -> None:
        a, b = self.reward
        if a < 0 or b < 0:
            raise ValueError("reward values must be >= 0")
        if a > b:
            raise ValueError("reward min must be <= reward max")
        self.time.validate()


@dataclass(frozen=True)
class HeuristicsConfig:
    version: int
    difficulties: Dict[str, HeuristicSpec]

    def validate(self) -> None:
        if self.version < 1:
            raise ValueError("Unsupported heuristics config version")
        for name, spec in self.difficulties.items():
            if not name:
                raise ValueError("difficulty name cannot be empty")
            spec.validate()


DEFAULT_DATA = {
    "version": 1,
    "difficulties": {
        "easy": {"reward": [100, 500], "time": {"min": 30, "max": None}},
        "medium": {"reward": [500, 2000], "time": {"min": 20, "max": 60}},
        "hard": {"reward": [2000, 5000], "time": {"min": 10, "max": 30}},
    },
}


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        # Fallback to defaults when PyYAML is not installed
        return DEFAULT_DATA
    if not path.exists():
        # Fallback to defaults when file is missing
        return DEFAULT_DATA
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_heuristics_config(config_path: Path) -> HeuristicsConfig:
    data = _load_yaml(config_path)
    try:
        version = int(data.get("version", 1))
        diffs = {}
        for name, entry in data.get("difficulties", {}).items():
            reward = tuple(entry["reward"])  # type: ignore
            time_obj = entry["time"]
            time_spec = TimeSpec(min=int(time_obj["min"]), max=time_obj.get("max"))
            diffs[name] = HeuristicSpec(reward=(int(reward[0]), int(reward[1])), time=time_spec)
        cfg = HeuristicsConfig(version=version, difficulties=diffs)
        cfg.validate()
        return cfg
    except Exception as e:  # Provide helpful error context
        raise ValueError(
            f"Invalid heuristics config at {config_path}: {e}\nRaw: {json.dumps(data, indent=2)}"
        ) from e


def format_heuristics(cfg: HeuristicsConfig) -> str:
    def fmt_range(rng: Tuple[int, int]) -> str:
        return f"{rng[0]}–{rng[1]}"

    def fmt_time(t: TimeSpec) -> str:
        return f"≥{t.min}s" if t.max is None else f"{t.min}–{t.max}s"

    lines = []
    for name, spec in cfg.difficulties.items():
        lines.append(
            f"{name} -> reward {fmt_range(spec.reward)}, time {fmt_time(spec.time)}"
        )
    return "Heuristics:\n" + "\n".join(lines)


def load_and_format_heuristics(project_root: Path) -> str:
    # Allow override via env or defaults later; for now look in graph/config/heuristics.yaml
    config_path = project_root / "graph" / "config" / "heuristics.yaml"
    cfg = load_heuristics_config(config_path)
    return format_heuristics(cfg)
