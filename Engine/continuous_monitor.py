from risk_engine import calculate_risk_scores
from risk_contextualizer import contextualize
from summary_generator import generate_summary
from utils import write_json, now_utc


def run_continuous_scan():
    return {
        "run_time": now_utc(),
        "technical": calculate_risk_scores()["metadata"],
        "contextual": contextualize()["metadata"],
        "summary": generate_summary()
    }

if __name__ == "__main__":
    print(run_continuous_scan())

