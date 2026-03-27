def get_assets():
    return [
        {
            "asset_id": "A1",
            "asset_type": "Web Application",
            "business_criticality": "High",
            "data_sensitivity": "PII",
            "internet_exposed": "Yes",
            "owner": "AppSec Team"
        },
        {
            "asset_id": "A2",
            "asset_type": "Database",
            "business_criticality": "High",
            "data_sensitivity": "PII",
            "internet_exposed": "No",
            "owner": "DB Admin Team"
        },
        {
            "asset_id": "A3",
            "asset_type": "Cloud VM",
            "business_criticality": "Medium",
            "data_sensitivity": "Internal",
            "internet_exposed": "Yes",
            "owner": "Cloud Security Team"
        },
        {
            "asset_id": "A4",
            "asset_type": "Internal Tool",
            "business_criticality": "Low",
            "data_sensitivity": "Internal",
            "internet_exposed": "No",
            "owner": "Engineering Team"
        },
        {
            "asset_id": "A5",
            "asset_type": "Test Server",
            "business_criticality": "Low",
            "data_sensitivity": "None",
            "internet_exposed": "No",
            "owner": "QA / Infra Team"
        }
    ]


if __name__ == "__main__":
    for a in get_assets():
        print(a)
