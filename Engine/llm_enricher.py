import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "Outputs")

input_file = os.path.join(OUTPUT_DIR, "contextual_risk.json")
output_file = os.path.join(OUTPUT_DIR, "final_risk.json")

with open(input_file) as f:
    data = json.load(f)

def generate_explanation(row):
    return f"""
This vulnerability ({row['cve_id']}) impacts a {row['asset_type']} owned by {row['owner']}.
The asset is {'internet exposed' if row['internet_exposed']=='Yes' else 'internal'} 
and has {row['business_criticality']} business importance.

This increases the likelihood of exploitation and potential business impact such as:
- Data breach
- Service disruption
- Financial loss
- Regulatory penalties

Overall, this is categorized as {row['risk_level']} risk and requires immediate attention.
"""

def generate_action(row):
    if row["risk_level"] == "Critical":
        return "🚨 Immediate patching required. Escalate to security leadership."
    elif row["risk_level"] == "High":
        return "⚠️ Prioritize remediation within SLA."
    elif row["risk_level"] == "Medium":
        return "🛠️ Fix in next patch cycle."
    else:
        return "📊 Monitor risk."

for row in data["results"]:
    row["llm_business_explanation"] = generate_explanation(row)
    row["recommended_action"] = generate_action(row)

with open(output_file, "w") as f:
    json.dump(data, f, indent=2)

print("✅ LLM enrichment complete!")