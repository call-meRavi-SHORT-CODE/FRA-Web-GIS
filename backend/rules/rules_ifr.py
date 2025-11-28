import pandas as pd

def apply_ifr_rules(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # make all column names lowercase
    df.columns = [c.strip().lower() for c in df.columns]

    # expected columns in lowercase (your dataset, lowercase version)
    # claimant_name, aadhar_number, phone_number, spouse_name, father_mother_name,
    # address, village, gram_panchayat, tehsil, district, is_st, is_otfd,
    # family_members_names, family_members_ages, habitation_area, cultivation_area,
    # disputed_lands, pattas_or_leases, rehabilitation_land, displacement_details,
    # forest_village_extent, other_traditional_rights, age_of_claimant, gender,
    # marital_status, household_members, elderly_count_60plus, disability_in_household,
    # primary_livelihood, annual_income, cultivable_land_ownership, house_type,
    # electricity_connection, water_source, toilet_available, school_going_children,
    # highest_education_level, shg_membership

    # fill missing important columns with defaults
    defaults = {
        "is_st": "no",
        "is_otfd": "no",
        "cultivation_area": 0,
        "annual_income": 0,
        "age_of_claimant": 0,
        "house_type": "",
        "primary_livelihood": "",
        "shg_membership": "no",
        "school_going_children": "no",
        "highest_education_level": "illiterate",
        "elderly_count_60plus": 0,
        "disability_in_household": "no",
        "household_members": 1,
        "cultivable_land_ownership": "no",
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val

    # lowercase all string values
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].astype(str).str.strip().str.lower()

    st_flag = df["is_st"].isin(["yes", "true", "1"])
    shg_flag = df["shg_membership"].isin(["yes", "true", "1"])

    # education ordering
    edu_levels = [
        "illiterate",
        "primary",
        "middle",
        "high school",
        "higher secondary",
        "diploma",
        "graduation",
        "post graduation",
        "phd",
    ]

    def edu_index(x: str) -> int:
        x = str(x).strip().lower()
        return edu_levels.index(x) if x in edu_levels else 0

    df["edu_index"] = df["highest_education_level"].apply(edu_index)

    # ---------- LABELS (12 IFR schemes) ----------

    # 1. PMAY–G: kutcha house
    df["label_PMAYG"] = (df["house_type"] == "kutcha").astype(int)

    # 2. PM–KISAN: cultivable land + cultivation area > 0 + agri livelihood
    df["label_PMKISAN"] = (
        (df["cultivable_land_ownership"] == "yes") &
        (df["cultivation_area"].astype(float) > 0) &
        (df["primary_livelihood"].isin(["agriculture", "farmer"]))
    ).astype(int)

    # 3. MGNREGA – individual: wage labour or low income
    df["label_MGNREGA_INDIV"] = (
        (df["primary_livelihood"] == "wage labour") |
        (df["annual_income"].astype(float) < 60000)
    ).astype(int)

    # 4. NRLM – individual: SHG membership
    df["label_NRLM_INDIV"] = shg_flag.astype(int)

    # 5. DDU–GKY: youth 18–35
    df["label_DDUGKY"] = (
        (df["age_of_claimant"].astype(float) >= 18) &
        (df["age_of_claimant"].astype(float) <= 35)
    ).astype(int)

    # 6. EMRS: ST + school-going children
    df["label_EMRS"] = (st_flag & (df["school_going_children"] == "yes")).astype(int)

    # 7. Pre-Matric ST: ST + children + edu <= high school
    df["label_PREMATRIC_ST"] = (
        st_flag &
        (df["school_going_children"] == "yes") &
        (df["edu_index"] <= edu_index("high school"))
    ).astype(int)

    # 8. Post-Matric ST: ST + edu >= higher secondary
    df["label_POSTMATRIC_ST"] = (
        st_flag &
        (df["edu_index"] >= edu_index("higher secondary"))
    ).astype(int)

    # 9. National Fellowship ST: ST + grad or above
    df["label_NATFELLOWSHIP_ST"] = (
        st_flag &
        (df["edu_index"] >= edu_index("graduation"))
    ).astype(int)

    # 10. NSAP: age >= 60, elderly or disability
    df["label_NSAP"] = (
        (df["age_of_claimant"].astype(float) >= 60) |
        (df["elderly_count_60plus"].astype(float) > 0) |
        (df["disability_in_household"] == "yes")
    ).astype(int)

    # 11. PMGKAY: low income → food support
    df["label_PMGKAY"] = (
        df["annual_income"].astype(float) < 80000
    ).astype(int)

    # 12. Institutional support for tribal products – individual
    df["label_TRIBALPROD_INDIV"] = (
        st_flag &
        df["primary_livelihood"].isin(["ntfp", "forest produce", "artisan", "handicraft"])
    ).astype(int)

    df.drop(columns=["edu_index"], inplace=True, errors="ignore")

    return df
