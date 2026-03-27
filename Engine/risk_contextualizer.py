import json
import os
from asset_context import get_assets
from utils import now_utc

# ==============================
# 🔹 OUTPUT DIRECTORY
# ==============================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Outputs")


# ==============================
# 🔹 MULTIPLIERS
# ==============================
CRITICALITY_MULTIPLIER = {
    "High": 4,
    "Medium": 2,
    "Low": 1
}

EXPOSURE_MULTIPLIER = {
    "Yes": 1.5,
    "No": 1.0
}


# ==============================
# 🔹 DECISION ENGINE
# ==============================
def get_decision(business_risk):
    if business_risk >= 20000:
        return "Reject"
    elif business_risk >= 12000:
        return "Escalate"
    else:
        return "Approve"


def get_decision_reason(row):
    if row["business_risk"] >= 20000:
        return "Extremely high business risk. Change must not proceed."
    elif row["business_risk"] >= 12000:
        return "High business risk. Requires security approval."
    else:
        return "Risk is acceptable. Proceed with monitoring."


# ==============================
# 🔹 LLM BUSINESS EXPLANATION
# ==============================
def generate_llm_business_explanation(row):
    return (
        f"{row['cve_id']} is a {row['risk_level']} vulnerability affecting a "
        f"{row['asset_type']}. Since the asset is {row['business_criticality']} critical "
        f"and {'internet exposed' if row['internet_exposed']=='Yes' else 'internal'}, "
        f"an attacker can exploit this vulnerability to gain unauthorized access, disrupt services, or compromise sensitive data", 
        f"data confidentiality, or system availability."
    )


# ==============================
# 🔹 MAIN CONTEXTUALIZER
# ==============================
def contextualize():

    # Load technical risk output
    with open(os.path.join(OUTPUT_DIR, "technical_risk.json"), "r", encoding="utf-8") as f:
        tech = json.load(f)

    assets = get_assets()
    contextual_results = []

    # ==============================
    # 🔹 PROCESS EACH ASSET + CVE
    # ==============================
    for asset in assets:
        criticality_factor = CRITICALITY_MULTIPLIER[asset["business_criticality"]]
        exposure_factor = EXPOSURE_MULTIPLIER[asset["internet_exposed"]]

        for cve in tech["results"]:
            base_risk = cve["risk_score"]

            # 🔥 BUSINESS RISK CALCULATION
            business_risk = base_risk * criticality_factor * exposure_factor

            # 🔹 BASE ROW
            row = {
                "asset_id": asset["asset_id"],
                "asset_type": asset["asset_type"],
                "owner": asset["owner"],
                "internet_exposed": asset["internet_exposed"],
                "business_criticality": asset["business_criticality"],
                "cve_id": cve["cve_id"],
                "base_risk": base_risk,
                "business_risk": round(business_risk, 2),
                "risk_level": cve["risk_level"],
                "remediation_sla": cve["remediation_sla"],
                "impact_type": "Confidentiality / Integrity / Availability"
            }

            # ==============================
            # 🔥 DECISION ENGINE
            # ==============================
            row["decision"] = get_decision(row["business_risk"])
            row["decision_reason"] = get_decision_reason(row)

            # ==============================
            # 🔥 EXTRA INTELLIGENCE (FIXED INDENTATION)
            # ==============================
            row["attack_type"] = (
                "Remote Exploit"
                if row["internet_exposed"] == "Yes"
                else "Local/Internal"
            )

            row["confidence"] = (
                "High"
                if row["risk_level"] == "Critical"
                else "Medium"
            )

            # ==============================
            # 🔥 RECOMMENDED ACTION
            # ==============================
            if row["decision"] == "Reject":
                row["recommended_action"] = "Patch immediately before deployment"
            elif row["decision"] == "Escalate":
                row["recommended_action"] = "Review with security team"
            else:
                row["recommended_action"] = "Proceed with monitoring"

            # ==============================
            # 🤖 LLM EXPLANATION
            # ==============================
            row["llm_business_explanation"] = generate_llm_business_explanation(row)

            contextual_results.append(row)

    # ==============================
    # 🔹 SORT BY BUSINESS RISK
    # ==============================
    sorted_results = sorted(
        contextual_results,
        key=lambda x: x["business_risk"],
        reverse=True
    )

    # ==============================
    # 🔹 PRIORITY TAGGING
    # ==============================
    for i, r in enumerate(sorted_results):
        if i < 5:
            r["priority_tag"] = "Top Business Critical"
        elif i < 15:
            r["priority_tag"] = "High Business Risk"
        else:
            r["priority_tag"] = "Normal"

    # ==============================
    # 🔹 OUTPUT
    # ==============================
    output = {
        "metadata": {
            "scan_time": now_utc(),
            "engine": "contextual-risk-engine",
            "model": "business-context-adjusted"
        },
        "results": sorted_results
    }

    # Write JSON output
    with open(os.path.join(OUTPUT_DIR, "contextual_risk.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output


# ==============================
# 🔹 RUN
# ==============================
if __name__ == "__main__":
    out = contextualize()

    print("Top Business Risks:\n")
    for r in out["results"][:10]:
        print(r)