# import pandas as pd
# import joblib
# import numpy as np

# from rules.rules_cfr import apply_cfr_rules
# # --------------------------
# # Human readable metadata
# # --------------------------
# CFR_META = {
#     "jjm": {
#         "reason": "Village has poor/partial water supply or low water availability.",
#         "benefit": "Improves safe drinking water access and tap connections.",
#         "impact": "Reduces water stress and enhances health outcomes."
#     },
#     "pmjanman": {
#         "reason": "Forest condition degraded / high NTFP collection workload.",
#         "benefit": "Targeted tribal development and basic services improvement.",
#         "impact": "Strengthens socio-economic well-being of tribal communities."
#     },
#     "dajgua": {
#         "reason": "Irregular Gram Sabha / fire incidents indicate governance gaps.",
#         "benefit": "Village development, forest governance and infrastructure support.",
#         "impact": "Improves collective capacity and forest management."
#     },
#     "mgnrega_community": {
#         "reason": "Poor road access or no electricity — infrastructure deficit.",
#         "benefit": "Creation of durable community assets via MGNREGA.",
#         "impact": "Supports livelihoods and boosts village infrastructure."
#     },
#     "nrlm_community": {
#         "reason": "FRC institution formed — strong community governance.",
#         "benefit": "Strengthening of SHG/VO institutions under NRLM.",
#         "impact": "Improves women empowerment and financial inclusion."
#     },
#     "tribalprod_community": {
#         "reason": "High dependency on NTFP collection.",
#         "benefit": "Support for NTFP processing, storage and marketing.",
#         "impact": "Increases income from forest-based livelihoods."
#     },
#     "ngogrant": {
#         "reason": "Degraded forest & fire incidents indicate need for NGO support.",
#         "benefit": "Grant-in-aid for voluntary tribal welfare organisations.",
#         "impact": "Improves resilience and socio-economic support systems."
#     }
# }


# def explain_cfr_row(row):
#     """
#     Explain predictions for ONE CFR row.
#     row must be: df.iloc[0]  (Series)
#     """

#     # Load preprocessor + feature order
#     pre = joblib.load("models/cfr_models/cfr_preprocessor.joblib")
#     feature_cols = joblib.load("models/cfr_models/cfr_features.joblib")

#     # Normalize index names (Series)
#     r = row.copy()
#     # r.index = r.index.str.lower()
#     r.index = r.index.astype(str).str.lower()

#     feature_cols = [c.lower() for c in feature_cols]

#     # Ensure missing features exist
#     for c in feature_cols:
#         if c not in r.index:
#             r[c] = None

#     # Prepare data
#     X = r[feature_cols].to_frame().T
#     Xp = pre.transform(X)

#     schemes = [
#         "jjm",
#         "pmjanman",
#         "dajgua",
#         "mgnrega_community",
#         "nrlm_community",
#         "tribalprod_community",
#         "ngogrant"
#     ]

#     results = []

#     for sch in schemes:
#         model_path = f"models/cfr_models/xgb_{sch}.joblib"

#         try:
#             model = joblib.load(model_path)
#         except:
#             continue

#         prob = float(model.predict_proba(Xp)[0, 1])
#         eligible = "YES" if prob >= 0.5 else "NO"

#         meta = CFR_META.get(sch, {
#             "reason": "Village meets scheme criteria.",
#             "benefit": "Helps community development.",
#             "impact": "Improves overall well-being."
#         })

#         results.append({
#             "scheme": sch.upper(),
#             "probability": prob,
#             "eligible": eligible,
#             "reason": meta["reason"],
#             "benefit": meta["benefit"],
#             "impact": meta["impact"]
#         })

#     return results




import pandas as pd
import joblib
import numpy as np

from rules.rules_cfr import apply_cfr_rules

CFR_META = {
    "jjm": {
        "reason": "Village has poor/partial water supply or low water availability.",
        "benefit": "Improves safe drinking water access and tap connections.",
        "impact": "Reduces water stress and enhances health outcomes."
    },
    "pmjanman": {
        "reason": "Forest condition degraded / high NTFP collection workload.",
        "benefit": "Targeted tribal development and basic services improvement.",
        "impact": "Strengthens socio-economic well-being of tribal communities."
    },
    "dajgua": {
        "reason": "Irregular Gram Sabha / fire incidents indicate governance gaps.",
        "benefit": "Village development, forest governance and infrastructure support.",
        "impact": "Improves collective capacity and forest management."
    },
    "mgnrega_community": {
        "reason": "Poor road access or no electricity — infrastructure deficit.",
        "benefit": "Creation of durable community assets via MGNREGA.",
        "impact": "Supports livelihoods and boosts village infrastructure."
    },
    "nrlm_community": {
        "reason": "FRC institution formed — strong community governance.",
        "benefit": "Strengthening of SHG/VO institutions under NRLM.",
        "impact": "Improves women empowerment and financial inclusion."
    },
    "tribalprod_community": {
        "reason": "High dependency on NTFP collection.",
        "benefit": "Support for NTFP processing, storage and marketing.",
        "impact": "Increases income from forest-based livelihoods."
    },
    "ngogrant": {
        "reason": "Degraded forest & fire incidents indicate need for NGO support.",
        "benefit": "Grant-in-aid for voluntary tribal welfare organisations.",
        "impact": "Improves resilience and socio-economic support systems."
    }
}

def explain_cfr_row(row):
    """
    Explain predictions for ONE CFR row.
    row can be: df.iloc[0] (Series) or df.iloc[[0]] (single-row DataFrame)
    """

    # Ensure row is a Series
    if isinstance(row, pd.DataFrame):
        if len(row) != 1:
            raise ValueError("DataFrame row input must have exactly one row.")
        r = row.iloc[0].copy()
    else:
        r = row.copy()

    # Normalize index/column names
    r.index = r.index.astype(str).str.lower()

    # Load preprocessor + feature order
    pre = joblib.load("models/cfr_models/cfr_preprocessor.joblib")
    feature_cols = joblib.load("models/cfr_models/cfr_features.joblib")
    feature_cols = [c.lower() for c in feature_cols]

    # Ensure missing features exist as np.nan
    for c in feature_cols:
        if c not in r.index:
            r[c] = np.nan

    # Prepare data for model
    X = r[feature_cols].to_frame().T
    try:
        Xp = pre.transform(X)
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return []

    schemes = [
        "jjm",
        "pmjanman",
        "dajgua",
        "mgnrega_community",
        "nrlm_community",
        "tribalprod_community",
        "ngogrant"
    ]

    results = []

    for sch in schemes:
        model_path = f"models/cfr_models/xgb_{sch}.joblib"

        try:
            model = joblib.load(model_path)
        except FileNotFoundError:
            print(f"Warning: Model for {sch} not found at {model_path}")
            continue
        except Exception as e:
            print(f"Error loading model {sch}: {e}")
            continue

        try:
            prob = float(model.predict_proba(Xp)[0, 1])
        except Exception as e:
            print(f"Error predicting with model {sch}: {e}")
            prob = 0.0

        eligible = "YES" if prob >= 0.5 else "NO"

        meta = CFR_META.get(sch, {
            "reason": "Village meets scheme criteria.",
            "benefit": "Helps community development.",
            "impact": "Improves overall well-being."
        })

        results.append({
            "scheme": sch.upper(),
            "probability": prob,
            "eligible": eligible,
            "reason": meta["reason"],
            "benefit": meta["benefit"],
            "impact": meta["impact"]
        })

    if not results:
        print("Warning: No CFR models were loaded for this row.")

    return results
