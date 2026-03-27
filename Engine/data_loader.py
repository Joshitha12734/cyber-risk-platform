import json
from datetime import datetime
from config import NVD_PATH

def load_nvd_data(limit=None):
    with open(NVD_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cves = []

    for v in raw.get("vulnerabilities", []):
        metrics = v["cve"]["metrics"].get("cvssMetricV31", [])
        if not metrics:
            continue

        cvss = metrics[0]["cvssData"]

        cves.append({
            "cve_id": v["cve"]["id"],
            "attack_vector": cvss.get("attackVector", "UNKNOWN"),
            "attack_complexity": cvss.get("attackComplexity", "UNKNOWN"),
            "privileges_required": cvss.get("privilegesRequired", "UNKNOWN"),
            "user_interaction": cvss.get("userInteraction", "UNKNOWN"),
            "base_score": cvss.get("baseScore", 0)
        })

        if limit and len(cves) >= limit:
            break

    return {
        "metadata": {
            "source": "NVD",
            "ingested_at": datetime.utcnow().isoformat(),
            "total_records": len(cves)
        },
        "cves": cves
    }

