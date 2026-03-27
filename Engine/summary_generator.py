import json, os
from utils import now_utc

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Outputs")

def generate_summary():
    with open(os.path.join(OUTPUT_DIR, "contextual_risk.json")) as f:
        data = json.load(f)["results"]

    summary = {
        "generated_at": now_utc(),
        "organization_overview": {
            "total_assets": len(set(d["asset_id"] for d in data)),
            "total_cves": len(data),
            "total_business_risk": sum(d["business_risk"] for d in data)
        }
    }

    with open(os.path.join(OUTPUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == "__main__":
    print(generate_summary())
