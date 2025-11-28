import pandas as pd

def apply_cfr_rules(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]

    # Fill missing defaults
    defaults = {
        "seasonal_income_forest_percent": 0,
        "forest_condition": "",
        "fire_incidents_5yrs": "no",
        "water_availability_in_forest": "",
        "water_supply_coverage": "",
        "electricity_supply_coverage": "",
        "road_access_condition": "",
        "major_ntfps_collected": "",
        "gramsabha_meeting_frequency": "",
        "frc_formed": "",
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    # Convert all string columns to lowercase
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # ---------- LABEL DEFINITIONS ----------
    # Synthetic rule-based labels (for ML training)

    df["label_jjm"] = (
        df["water_supply_coverage"].isin(["none", "partial"])
        | df["water_availability_in_forest"].isin(["low"])
    ).astype(int)

    df["label_pmjanman"] = (
        df["forest_condition"].isin(["degraded"])
        | df["major_ntfps_collected"] != ""
    ).astype(int)

    df["label_dajgua"] = (
        df["fire_incidents_5yrs"].isin(["yes"])
        | df["gramsabha_meeting_frequency"].isin(["rare"])
    ).astype(int)

    df["label_mgnrega_community"] = (
        df["road_access_condition"].isin(["poor"])
        | df["electricity_supply_coverage"].isin(["none"])
    ).astype(int)

    df["label_nrlm_community"] = (
        df["frc_formed"].isin(["yes"])
    ).astype(int)

    df["label_tribalprod_community"] = (
        df["major_ntfps_collected"] != ""
    ).astype(int)

    df["label_ngogrant"] = (
        df["forest_condition"].isin(["degraded"])
        & df["fire_incidents_5yrs"].isin(["yes"])
    ).astype(int)

    return df
