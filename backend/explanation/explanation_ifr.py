import pandas as pd
import numpy as np
import joblib
import shap

from rules.rules_ifr import apply_ifr_rules

SCHEMES_IFR = [
    "PMAYG",
    "PMKISAN",
    "MGNREGA_INDIV",
    "NRLM_INDIV",
    "DDUGKY",
    "EMRS",
    "PREMATRIC_ST",
    "POSTMATRIC_ST",
    "NATFELLOWSHIP_ST",
    "NSAP",
    "PMGKAY",
    "TRIBALPROD_INDIV",
]

IMPACT_IFR = {
    "PMAYG": {
        "reason": "Kutcha or weak housing makes the household eligible for PMAY–G.",
        "benefit": "Support to construct or upgrade a pucca house.",
        "impact": "Improves long-term housing security and dignity."
    },
    "PMKISAN": {
        "reason": "Cultivable land and farming livelihood detected.",
        "benefit": "Direct income support to farmer household.",
        "impact": "Reduces seasonal financial stress and supports cultivation."
    },
    "MGNREGA_INDIV": {
        "reason": "Low income or wage labour dependence.",
        "benefit": "Guaranteed wage employment for willing workers.",
        "impact": "Stabilises income and helps meet basic needs."
    },
    "NRLM_INDIV": {
        "reason": "Self-Help Group membership in the household.",
        "benefit": "Access to SHG-based credit and livelihood support.",
        "impact": "Strengthens women’s economic role and resilience."
    },
    "DDUGKY": {
        "reason": "Youth in the age band for skill training.",
        "benefit": "Skill development and placement support.",
        "impact": "Improves employability and non-farm livelihoods."
    },
    "EMRS": {
        "reason": "ST household with school-going children.",
        "benefit": "Residential schooling under EMRS.",
        "impact": "Improves education outcomes for tribal children."
    },
    "PREMATRIC_ST": {
        "reason": "ST child at pre-matric education level.",
        "benefit": "Scholarship support for school education.",
        "impact": "Reduces dropouts and encourages continued schooling."
    },
    "POSTMATRIC_ST": {
        "reason": "ST student in higher secondary or beyond.",
        "benefit": "Scholarship for post-matric education.",
        "impact": "Improves access to higher education and careers."
    },
    "NATFELLOWSHIP_ST": {
        "reason": "ST candidate with graduation or higher.",
        "benefit": "Fellowship for advanced studies/research.",
        "impact": "Builds long-term academic and leadership capacity."
    },
    "NSAP": {
        "reason": "Elderly, widow or disabled member in household.",
        "benefit": "Social pension support.",
        "impact": "Provides minimum income security to vulnerable persons."
    },
    "PMGKAY": {
        "reason": "Low-income household with food security needs.",
        "benefit": "Free/subsidised food grain support.",
        "impact": "Reduces hunger and improves nutritional security."
    },
    "TRIBALPROD_INDIV": {
        "reason": "Livelihood depends on NTFP/forest produce/handicrafts.",
        "benefit": "Support for marketing and value addition of tribal products.",
        "impact": "Enhances income from traditional livelihoods."
    },
}

def explain_ifr_row(row: pd.DataFrame):
    """
    row: single-row DataFrame with ORIGINAL IFR columns.
    returns: list of dicts per scheme
    """
    df = apply_ifr_rules(row.copy())

    label_cols = [c for c in df.columns if c.startswith("label_")]
    feature_cols = [c for c in df.columns if c not in label_cols]

    pre = joblib.load("models/ifr_models/ifr_preprocessor.joblib")
    X = pre.transform(df[feature_cols])

    try:
        feature_names = joblib.load("models/ifr_models/ifr_feature_names.joblib")
    except:
        try:
            feature_names = pre.get_feature_names_out()
        except:
            feature_names = [f"f_{i}" for i in range(X.shape[1])]

    results = []

    for scheme in SCHEMES_IFR:
        model_path = f"models/ifr_models/ifr_model_{scheme}.joblib"
        label_col = f"label_{scheme}"

        try:
            model = joblib.load(model_path)
        except FileNotFoundError:
            continue

        prob = float(model.predict_proba(X)[0, 1])
        eligible = prob >= 0.5

        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X)[0]
        idx_sorted = np.argsort(np.abs(shap_vals))[::-1][:3]

        top_features = []
        for idx in idx_sorted:
            top_features.append({
                "feature": feature_names[idx],
                "contribution": float(shap_vals[idx])
            })

        meta = IMPACT_IFR.get(scheme, {
            "reason": "Eligibility based on livelihood and vulnerability.",
            "benefit": "Direct household-level support.",
            "impact": "Improves long-term livelihood security."
        })

        results.append({
            "scheme": scheme,
            "probability": prob,
            "eligible": "YES" if eligible else "NO",
            "top_features": top_features,
            "reason": meta["reason"],
            "benefit": meta["benefit"],
            "impact": meta["impact"],
        })

    return results
