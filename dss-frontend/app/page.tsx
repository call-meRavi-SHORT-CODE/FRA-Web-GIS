"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

type Claim = {
  id: string;
  name: string;
  type: string;
  village: string;
  status: string;
  schemes: string[];
};

type SchemeName = "PMAY-G" | "PM-KISAN" | "MGNREGA" | "JJM" | "DAJGUA";

export default function DSSPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("dss");

  const handleLogout = () => {
    router.push("/");
  };

  // --------------- STATE ---------------
  const [claimType, setClaimType] = useState("all");
  const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);


  // Dummy data (replace with Supabase fetch later)
  const claims = [
    {
      id: "IFR-001",
      name: "Nek Ram",
      type: "IFR",
      village: "Lakkarmandi",
      status: "Accepted",
      schemes: ["PMAY-G", "PM-KISAN", "MGNREGA"],
    },
    {
      id: "CR-005",
      name: "Village Community",
      type: "CR",
      village: "Padhrotu",
      status: "Accepted",
      schemes: ["DAJGUA", "JJM"],
    },
  ];

  const filteredClaims =
    claimType === "all"
      ? claims
      : claims.filter((c) => c.type === claimType);


      const schemeInfo: Record<SchemeName, {
    reason: string;
    benefits: string;
    impact: string;
    suggestion: string;
  }> = {
  "PMAY-G": {
    reason: "Beneficiary has kutcha or semi-pucca house and low income.",
    benefits: "₹1.3–1.95 lakh for construction of pucca house.",
    impact: "Improves housing security and reduces vulnerability.",
    suggestion: "Assist claimant to open bank account if not available."
  },
  "PM-KISAN": {
    reason: "Claimant depends on agriculture for livelihood.",
    benefits: "₹6,000 per year income support.",
    impact: "Ensures stable seasonal income.",
    suggestion: "Link land record after IFR approval."
  },
  "MGNREGA": {
    reason: "Livelihood vulnerability and need for wage support.",
    benefits: "100 days guaranteed wage employment.",
    impact: "Strengthens income security.",
    suggestion: "Prioritize forest restoration activities."
  },
  "JJM": {
    reason: "Village lacks adequate water supply coverage.",
    benefits: "Tap water connection for all households.",
    impact: "Improves health and reduces drudgery.",
    suggestion: "Train community water committee."
  },
  "DAJGUA": {
    reason: "Need for community governance strengthening.",
    benefits: "Funding for Gram Sabha-led development.",
    impact: "Improves local self-governance.",
    suggestion: "Conduct regular meetings for monitoring."
  }
};


  return (
    <div style={{ padding: "20px" }}>
      {/* ---------------- NAVBAR ---------------- */}
      <nav
        style={{
          background: "#003366",
          color: "white",
          padding: "10px 20px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderRadius: "6px",
        }}
      >
        <div style={{ display: "flex", gap: "20px", alignItems: "center" }}>
        

          {/* ------------ TABS ------------- */}
          <div style={{ display: "flex", gap: "15px" }}>
            <button
              onClick={() => setActiveTab("dss")}
              style={{
                background: activeTab === "dss" ? "#005bb5" : "transparent",
                color: "white",
                padding: "6px 14px",
                borderRadius: "4px",
                border: "1px solid white",
                cursor: "pointer",
              }}
            >
              Decision Support System
            </button>

            <button
              onClick={() => setActiveTab("cri")}
              style={{
                background: activeTab === "cri" ? "#005bb5" : "transparent",
                color: "white",
                padding: "6px 14px",
                borderRadius: "4px",
                border: "1px solid white",
                cursor: "pointer",
              }}
            >
              CRI – Community Resilience Index
            </button>
          </div>
        </div>

        {/* RIGHT SECTION */}
        <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
          <select style={{ padding: "6px" }}>
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
            <option value="or">ଓଡ଼ିଆ</option>
          </select>

          <button
            onClick={handleLogout}
            style={{
              background: "white",
              color: "#003366",
              padding: "6px 14px",
              borderRadius: "4px",
              border: "none",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Logout
          </button>
        </div>
      </nav>

      {/* ========================================================= */}
      {/* ==================== DSS TAB CONTENT ==================== */}
      {/* ========================================================= */}
      {activeTab === "dss" && (
        <>
          {/* ---------------- STATS CARDS ---------------- */}
          <div
            style={{
              display: "flex",
              gap: "20px",
              marginTop: "25px",
              marginBottom: "25px",
            }}
          >
            {[
              { label: "Accepted IFR Claims", value: 120 },
              { label: "Accepted CR Claims", value: 45 },
              { label: "Accepted CFR Claims", value: 18 },
              { label: "Total Schemes Available", value: 23 },
            ].map((item, idx) => (
              <div
                key={idx}
                style={{
                  flex: 1,
                  background: "#e8f1ff",
                  padding: "20px",
                  borderRadius: "8px",
                  boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
                }}
              >
                <h3 style={{ color: "#003366" }}>{item.label}</h3>
                <p
                  style={{
                    fontSize: "24px",
                    fontWeight: "bold",
                    marginTop: "10px",
                  }}
                >
                  {item.value}
                </p>
              </div>
            ))}
          </div>

          {/* ---------------- FILTER BAR ---------------- */}
          <div
            style={{
              marginBottom: "15px",
              display: "flex",
              gap: "10px",
              alignItems: "center",
              marginTop: "20px",
            }}
          >
            <strong>Filter :</strong>

            {/* Claim Type */}
            <select
              value={claimType}
              onChange={(e) => setClaimType(e.target.value)}
              style={{ padding: "8px", flex: 0.5 }}
            >
              <option value="all">All</option>
              <option value="IFR">IFR</option>
              <option value="CR">CR</option>
              <option value="CFR">CFR</option>
            </select>

            {/* LOCATION FILTERS */}
            <select style={{ padding: "8px", flex: 0.5 }}>
              <option>Select State</option>
              <option>Madhya Pradesh</option>
              <option>Maharashtra</option>
              <option>Chhattisgarh</option>
            </select>

            <select style={{ padding: "8px", flex: 0.5 }}>
              <option>Select District</option>
              <option>Bhopal</option>
              <option>Sehore</option>
            </select>

            <select style={{ padding: "8px", flex: 0.5 }}>
              <option>Select Block / Taluka</option>
              <option>Berasia</option>
            </select>

            <select style={{ padding: "8px", flex: 0.5 }}>
              <option>Select Village</option>
              <option>Lakkarmandi</option>
              <option>Padhrotu</option>
            </select>
          </div>

          {/* ---------------- CLAIMS TABLE ---------------- */}
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              background: "white",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
            }}
          >
            <thead>
              <tr style={{ background: "#003366", color: "white" }}>
                <th style={{ padding: "10px" }}>Claim ID</th>
                <th>Name / Community</th>
                <th>Type</th>
                <th>Village</th>
                <th>Status</th>
                <th>Schemes</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {filteredClaims.map((claim) => (
                <tr key={claim.id}>
                  <td style={{ padding: "10px" }}>{claim.id}</td>
                  <td>{claim.name}</td>
                  <td>{claim.type}</td>
                  <td>{claim.village}</td>
                  <td>{claim.status}</td>
                  <td>{claim.schemes.join(", ")}</td>
                  <td>
                    <button
                      onClick={() => setSelectedClaim(claim)}
                      style={{
                        padding: "6px 10px",
                        background: "#0071bc",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                      }}
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* ---------------- MODAL ---------------- */}
          {selectedClaim && (
  <div
    style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: "rgba(0,0,0,0.5)",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 9999,
    }}
    onClick={() => setSelectedClaim(null)}
  >
    <div
      style={{
        background: "white",
        padding: "25px",
        borderRadius: "8px",
        width: "650px",
        maxHeight: "85vh",
        overflowY: "auto",
      }}
      onClick={(e) => e.stopPropagation()}
    >
      <h2>Claim Details</h2>

      <p><strong>Name:</strong> {selectedClaim.name}</p>
      <p><strong>Type:</strong> {selectedClaim.type}</p>
      <p><strong>Village:</strong> {selectedClaim.village}</p>

      <h3 style={{ marginTop: "20px" }}>Recommended Schemes</h3>

      {selectedClaim.schemes.map((schemeName: string, i: number) => {
        const info = schemeInfo[schemeName as SchemeName];
        return (
          <div
            key={i}
            style={{
              marginBottom: "18px",
              padding: "15px",
              background: "#f4f9ff",
              borderRadius: "6px",
              border: "1px solid #d8e6ff",
            }}
          >
            <h4 style={{ marginBottom: "8px", color: "#003366" }}>
              {schemeName}
            </h4>

            <p><strong>Reason:</strong> {info?.reason || "N/A"}</p>
            <p><strong>Benefits:</strong> {info?.benefits || "N/A"}</p>
            <p><strong>Impact:</strong> {info?.impact || "N/A"}</p>
          </div>
        );
      })}

      <button
        onClick={() => setSelectedClaim(null)}
        style={{
          marginTop: "15px",
          padding: "8px 12px",
          background: "#003366",
          color: "white",
          borderRadius: "4px",
          border: "none",
          cursor: "pointer",
        }}
      >
        Close
      </button>
    </div>
  </div>
          )}
        </>
      )}

      {/* ========================================================= */}
      {/* ==================== CRI TAB CONTENT ==================== */}
      {/* ========================================================= */}
      {activeTab === "cri" && (
        <>
          <h2 style={{ marginTop: "20px", color: "#003366" }}>
            Community Resilience Index (CRI)
          </h2>

          <p>
            CRI helps assess village-level resilience using infrastructure,
            livelihood, education, health, geo-data, and FRA rights distribution.
          </p>

          <div
            style={{
              marginTop: "20px",
              background: "#f0f6ff",
              padding: "20px",
              borderRadius: "8px",
            }}
          >
            <h3>Sample CRI Score</h3>
            <p style={{ fontSize: "32px", fontWeight: "bold" }}>68 / 100</p>
            <p>Resilience Level: Moderate</p>
          </div>
        </>
      )}
    </div>
  );
}