import "./globals.css";
import Link from "next/link";
// import "../tailwind.css";


export const metadata = {
  title: "FRA WebGIS",
  description: "Forest Rights Act WebGIS Portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0 }}>
        {/* --- White Logo/Title Strip --- */}
        <div
          style={{
            // position:"fixed",
            background: "#ffffff",
            padding: "10px 30px",
            display: "flex",
            alignItems: "center", 
            justifyContent: "space-between",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)", // subtle shadow
          }}
        >
          {/* Ministry Logo only */}
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
  <img src="/ministry-logo.png" alt="Ministry Logo" width="30" />
  <div>
    <p style={{ color: "black", margin: 0, fontSize: "14px" }}>
      जनजातीय कार्य मंत्रालय
    </p>
    <h2
      style={{
        color: "black",
        margin: 0,
        fontSize: "16px",
        fontWeight: "bold",
        lineHeight: "1.2",
      }}
    >
      MINISTRY OF TRIBAL AFFAIRS
    </h2>
  </div>
</div>

          {/* FRA Atlas title */}
          <h2 style={{ margin: 0, fontSize: "20px", color: "#003366" }}>FRA Web GIS</h2>
        </div>

        

        {/* --- Main Page Content --- */}
        <main>{children}</main>
      </body>
    </html>
  );
}
