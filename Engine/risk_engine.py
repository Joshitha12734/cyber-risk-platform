from data_loader import load_nvd_data
from config import OUTPUT_DIR, ENGINE_VERSION, RULESET_VERSION
from utils import write_json, now_utc
import os

# (Optional) LLM import
# If using OpenAI, uncomment and install openai
# from openai import OpenAI
# client = OpenAI(api_key="YOUR_API_KEY")


# ==============================
# 🔹 RISK LEVEL CLASSIFICATION
# ==============================
def get_risk_level(score):
    if score >= 3500:
        return "Critical"
    elif score >= 2500:
        return "High"
    elif score >= 1500:
        return "Medium"
    else:
        return "Low"


# ==============================
# 🔹 SLA MAPPING
# ==============================
def remediation_sla(level):
    return {
        "Critical": "Fix within 24 hours",
        "High": "Fix within 7 days",
        "Medium": "Fix within 14 days",
        "Low": "Fix within 30 days"
    }[level]


# ==============================
# 🔹 LLM EXPLANATION (MOCK / REAL)
# ==============================
def generate_llm_explanation(cve):
    """
    You can replace this with real OpenAI API call later
    """

    # 🔥 MOCK (works without API)
    explanation = (
        f"This vulnerability ({cve['cve_id']}) is considered {cve['risk_level']} risk. "
        f"It is exploitable via {cve.get('attack_vector', 'unknown vector')} and "
        f"has a base severity score of {cve.get('base_score', 'N/A')}. "
        f"If exploited, it could impact system confidentiality, integrity, or availability."
    )

    return explanation


# ==============================
# 🔹 PRIORITIZATION ENGINE
# ==============================
def prioritize_cves(cve_list):
    sorted_list = sorted(cve_list, key=lambda x: x["risk_score"], reverse=True)

    for i, cve in enumerate(sorted_list):
        cve["priority_rank"] = i + 1
        cve["risk_level"] = get_risk_level(cve["risk_score"])

        if i < 5:
            cve["priority_tag"] = "Top Critical"
        elif i < 15:
            cve["priority_tag"] = "High Priority"
        else:
            cve["priority_tag"] = "Normal"

    return sorted_list


# ==============================
# 🔹 MAIN FUNCTION
# ==============================
def calculate_risk_scores():
    data = load_nvd_data(limit=100)
    results = []

    for cve in data["cves"]:
        likelihood = 1

        if cve["attack_vector"] == "NETWORK":
            likelihood += 2
        if cve["attack_complexity"] == "LOW":
            likelihood += 1

        impact = int(cve["base_score"] * 100)
        score = likelihood * impact

        # 🔥 Explainability (without LLM)
        reasons = []
        if cve["attack_vector"] == "NETWORK":
            reasons.append("Network exploitable")
        if cve["attack_complexity"] == "LOW":
            reasons.append("Low complexity")

        results.append({
            "cve_id": cve["cve_id"],
            "risk_score": score,
            "attack_vector": cve["attack_vector"],
            "base_score": cve["base_score"],
            "risk_reason": ", ".join(reasons)
        })

    # ==============================
    # 🔥 PRIORITIZATION
    # ==============================
    results = prioritize_cves(results)

    # ==============================
    # 🔥 ADD SLA + LLM
    # ==============================
    for cve in results:
        cve["remediation_sla"] = remediation_sla(cve["risk_level"])

        # 🔥 LLM EXPLANATION
        cve["llm_explanation"] = generate_llm_explanation(cve)

    # ==============================
    # 🔹 OUTPUT
    # ==============================
    output = {
        "metadata": {
            "scan_time": now_utc(),
            "engine": "technical-risk-engine",
            "engine_version": ENGINE_VERSION,
            "ruleset_version": RULESET_VERSION,
            "total_cves": len(results)
        },
        "results": results
    }

    write_json(os.path.join(OUTPUT_DIR, "technical_risk.json"), output)

    return output


# ==============================
# 🔹 RUN
# ==============================
if __name__ == "__main__":
    calculate_risk_scores()