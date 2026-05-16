# filename: backend/core/rl_engine.py

from typing import Dict, List
from statistics import mean

TOPIC_GRAPH = {
    "numbers": ["fractions", "equations"],
    "fractions": ["equations", "proportions"],
    "equations": ["inequalities", "systems"],
    "proportions": ["percentages"],
}

def _estimate_mastery(performance: List[dict]) -> float:
    if not performance:
        return 0.3
    scores = [p["score"] for p in performance]
    return max(0.0, min(1.0, mean(scores)))

def _choose_difficulty(mastery: float) -> str:
    if mastery < 0.4:
        return "easy"
    if mastery < 0.7:
        return "medium"
    return "hard"

def suggest_next_topic(history: Dict, recent_performance: List[dict] | None) -> Dict:
    last_topic = history.get("last_topic", "numbers")
    topic_perf = {}

    if recent_performance:
        for p in recent_performance:
            topic_perf.setdefault(p["topic"], []).append(p)

    last_topic_perf = topic_perf.get(last_topic, [])
    mastery = _estimate_mastery(last_topic_perf)
    difficulty = _choose_difficulty(mastery)

    neighbors = TOPIC_GRAPH.get(last_topic, ["numbers"])
    next_topic = neighbors[0] if neighbors else "numbers"

    exercises = [
        f"{next_topic} – {difficulty} practice 1",
        f"{next_topic} – {difficulty} practice 2",
        f"{next_topic} – {difficulty} challenge",
    ]

    rationale = (
        f"Based on your performance in {last_topic} (mastery ~ {round(mastery, 2)}), "
        f"we move to {next_topic} with {difficulty} difficulty."
    )

    return {
        "next_topic": next_topic,
        "difficulty": difficulty,
        "recommended_exercises": exercises,
        "rationale": rationale,
    }
