import pandas as pd

"""
Columns for CR (lowercase after normalization):
community_name
village
gram_panchayat
tehsil
district
fdst_or_otfd
nistar_rights
minor_forest_produce
grazing
community_uses
pastoral_access
habitat_rights
biodiversity_access
other_traditional_rights
ntfp_dependency_percent
agriculture_dependency_percent
wagelabour_dependency_percent
distance_to_road_km
distance_to_water_km
distance_to_school_km
distance_to_health_km
total_households
st_hh_percent
shg_vo_presence
drought_or_flood_prone
"""

def apply_cr_rules(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # defaults for key columns
    defaults = {
        "ntfp_dependency_percent": 0.0,
        "wagelabour_dependency_percent": 0.0,
        "st_hh_percent": 0.0,
        "distance_to_water_km": 0.0,
        "distance_to_road_km": 0.0,
        "shg_vo_presence": "no",
        "drought_or_flood_prone": "no",
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    # lowercase all string values
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip().str.lower()

    # ------------------------------
    # 7 CR scheme label definitions
    # ------------------------------

    # 1) Jal Jeevan Mission (JJM) – poor water access or drought/flood prone
    df["label_JJM"] = (
        (df["distance_to_water_km"].astype(float) > 1.0) |
        (df["drought_or_flood_prone"].isin(["drought", "flood", "both", "yes"]))
    ).astype(int)

    # 2) PM-JANMAN – very high ST concentration (e.g. > 70%)
    df["label_PMJANMAN"] = (df["st_hh_percent"].astype(float) > 70.0).astype(int)

    # 3) DAJGUA – tribal village development: > 40% ST households
    df["label_DAJGUA"] = (df["st_hh_percent"].astype(float) > 40.0).astype(int)

    # 4) MGNREGA – community assets in high wage-labour dependent villages
    df["label_MGNREGA_COMM"] = (
        df["wagelabour_dependency_percent"].astype(float) > 30.0
    ).astype(int)

    # 5) NRLM – Village Organisations (SHG/VO presence)
    df["label_NRLM_VO"] = (df["shg_vo_presence"] == "yes").astype(int)

    # 6) Institutional Support for Tribal Products – community level
    df["label_TRIBALPROD_COMM"] = (
        df["ntfp_dependency_percent"].astype(float) > 30.0
    ).astype(int)

    # 7) Grant-in-Aid – VO + drought/flood prone
    df["label_GRANTINAID_VO"] = (
        (df["shg_vo_presence"] == "yes") &
        (df["drought_or_flood_prone"].isin(["drought", "flood", "both", "yes"]))
    ).astype(int)

    return df
