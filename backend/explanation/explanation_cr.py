import pandas as pd
import numpy as np
import joblib
import shap

from rules.rules_cr import apply_cr_rules

CR_SCHEMES = [
    "JJM",
    "PMJANMAN",
    "DAJGUA",
    "MGNREGA_COMM",
    "NRLM_VO",
    "TRIBALPROD_COMM",
    "GRANTINAID_VO",
]

CR_IMPACT = {
    "JJM": {
        "reason": "Village shows poor or distant access to safe water sources, or is drought/flood prone.",
        "benefit": "Improved drinking water supply and household tap connections.",
        "impact": "Reduces water stress and improves community health."
    },
    "PMJANMAN": {
        "reason": "High concentration of ST households in the village.",
        "benefit": "Targeted tribal village development under PM-JANMAN.",
        "impact": "Enhances basic services and socio-economic status of tribal communities."
    },
    "DAJGUA": {
        "reason": "Village has significant tribal presence needing focused development.",
        "benefit": "Converged tribal area development (infrastructure, services, livelihoods).",
        "impact": "Improves long-term living conditions in tribal hamlets."
    },
    "MGNREGA_COMM": {
        "reason": "High dependency on wage labour in the community.",
        "benefit": "Creation of community assets via MGNREGA (ponds, roads, land development).",
        "impact": "Supports livelihoods while building durable infrastructure."
    },
    "NRLM_VO": {
        "reason": "Presence of SHG/VO federations in the village.",
        "benefit": "Strengthening of SHG institutions and village organisations under NRLM.",
        "impact": "Improves financial inclusion, women’s empowerment and local governance."
    },
    "TRIBALPROD_COMM": {
        "reason": "Community shows high dependency on NTFP for livelihoods.",
        "benefit": "Support for NTFP collection, value-addition and marketing.",
        "impact": "Increases and stabilises incomes from forest-based products."
    },
    "GRANTINAID_VO": {
        "reason": "SHG/VO present in an environmentally vulnerable (drought/flood prone) village.",
        "benefit": "Grant-in-aid to voluntary organisations working for ST welfare.",
        "impact": "Strengthens resilience and welfare programmes for tribal communities."
    },
}

def explain_cr_row(row: pd.DataFrame):
    """
    Explain ALL CR schemes for a single community row.

    Parameters
    ----------
    row : pd.DataFrame
        Single-row DataFrame from FINAL_CR_FormB.csv

    Returns
    -------
    list of dicts:
        [
          {
            "scheme": ...,
            "probability": ...,
            "eligible": "YES"/"NO",
            "top_features": [ {"feature": ..., "contribution": ...}, ... ],
            "reason": ...,
            "benefit": ...,
            "impact": ...
          },
          ...
        ]
    """
    # 1) Apply rules to create labels and normalized features
    df = apply_cr_rules(row.copy())

    # 2) Split features / labels
    label_cols = [c for c in df.columns if c.startswith("label_")]
    feature_cols = [c for c in df.columns if c not in label_cols]

    # 3) Load preprocessor and transform
    pre = joblib.load("models/cr_models/cr_preprocessor.joblib")
    X = pre.transform(df[feature_cols])

    # 4) Load feature names (for SHAP)
    try:
        feature_names = joblib.load("models/cr_models/cr_feature_names.joblib")
    except:
        try:
            feature_names = pre.get_feature_names_out()
        except:
            feature_names = [f"f_{i}" for i in range(X.shape[1])]

    results = []

    # 5) For each scheme, load model, predict, explain
    for scheme in CR_SCHEMES:
        model_path = f"models/cr_models/cr_model_{scheme}.joblib"
        try:
            model = joblib.load(model_path)
        except FileNotFoundError:
            # model not trained (e.g. single-class label)
            continue

        # probability and eligibility
        prob = float(model.predict_proba(X)[0, 1])
        eligible = prob >= 0.5

        # SHAP explanation
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X)[0]
        idx_sorted = np.argsort(np.abs(shap_vals))[::-1][:3]

        top_features = []
        for idx in idx_sorted:
            top_features.append({
                "feature": feature_names[idx],
                "contribution": float(shap_vals[idx])
            })

        impact_info = CR_IMPACT.get(scheme, {
            "reason": "Community vulnerability and infrastructure gaps.",
            "benefit": "Community-level development and welfare support.",
            "impact": "Improves collective resilience and living standards."
        })

        results.append({
            "scheme": scheme,
            "probability": prob,
            "eligible": "YES" if eligible else "NO",
            "top_features": top_features,
            "reason": impact_info["reason"],
            "benefit": impact_info["benefit"],
            "impact": impact_info["impact"],
        })

    return results
