import './App.css';
import Galaxy from "./Galaxy";
import BlurText from "./BlurText";
import Intro from "./Intro";
import SplitText from "./SplitText";
import NairaButton from "./NairaButton";
import GraphView from "./GraphView";

import { Routes, Route, useNavigate } from "react-router-dom";
import { useState } from "react";

/* ================= TABLE STYLES ================= */

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "15px",
  background: "#1a1f2e",
  color: "white"
};

const cellHeader = {
  border: "1px solid #444",
  padding: "10px",
  background: "#2c344d",
  fontWeight: "bold"
};

const cell = {
  border: "1px solid #444",
  padding: "10px"
};

/* ================= LANDING PAGE ================= */

function Landing() {
  const navigate = useNavigate();
  const [showIntro, setShowIntro] = useState(true);

  return (
    <>
      {showIntro && <Intro onComplete={() => setShowIntro(false)} />}

      <div className="page">
        <section className="hero-network">
          <div className="hero-overlay">
            <div className="hero-content-left">

              <SplitText
                text="CIPHERFLOW"
                tag="h1"
                className="hero-title"
                delay={0.05}
                duration={1.2}
                ease="power4.out"
                from={{ opacity: 0, y: 100 }}
                to={{ opacity: 1, y: 0 }}
              />

              <h2 className="hero-sub">
                Fraud Leaves Patterns. We Decode Them.
              </h2>

              <p className="hero-desc">
                Detect cycles. Smurfing. Layering.
                Visualize hidden financial structures instantly.
              </p>

              <div style={{ marginTop: "40px" }}>
                <NairaButton
                  text="Explore"
                  icon="🚀"
                  onClick={() => navigate("/explore")}
                />
              </div>

            </div>
          </div>
        </section>
      </div>
    </>
  );
}

/* ================= UPLOAD PAGE ================= */

function Upload({ setAnalysisResult }) {
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const f = e.target.files?.[0];
    if (f && f.name.endsWith(".csv")) {
      setFile(f);
      setFileName(f.name);
    } else {
      alert("Please select a valid CSV file");
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8023/analyze", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();

      setAnalysisResult(data);
      localStorage.setItem("analysisResult", JSON.stringify(data));

      navigate("/results");

    } catch (error) {
      console.error(error);
      alert("Analysis failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-background">
        <Galaxy />
      </div>

      <div className="upload-content">

        <BlurText
          text="Upload Transaction Dataset"
          delay={120}
          animateBy="words"
          direction="top"
          className="upload-title"
        />

        <p className="upload-sub">
          CSV must contain transaction_id, sender_id, receiver_id, amount, timestamp.
        </p>

        <label className="file-input-label">
          Browse File
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            hidden
          />
        </label>

        {fileName && (
          <>
            <p className="file-name">Selected File: {fileName}</p>

            {!loading ? (
              <NairaButton
                text="Analyze"
                icon="🔍"
                onClick={handleAnalyze}
              />
            ) : (
              <p style={{ marginTop: "20px" }}>Analyzing dataset...</p>
            )}
          </>
        )}

      </div>
    </div>
  );
}

/* ================= RESULTS PAGE ================= */

function Results({ analysisResult }) {
  const navigate = useNavigate();

  const downloadJson = () => {
    if (!analysisResult) return;

    const blob = new Blob(
      [JSON.stringify(analysisResult, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "analysis_result.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!analysisResult) {
    return (
      <div className="results-page">
        <div className="results-card">
          <h2>No Data</h2>
          <NairaButton text="Go Back" icon="←" onClick={() => navigate("/")} />
        </div>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="results-background">
        <Galaxy />
      </div>

      <div className="results-card">
        <h2 className="results-title">Analysis Complete</h2>

        <div className="results-buttons">
          <NairaButton text="View Graph" icon="📊" onClick={() => navigate("/graph")} />
          <NairaButton text="View Summary" icon="📄" onClick={() => navigate("/summary")} />
          <NairaButton text="Download JSON" icon="⬇️" onClick={downloadJson} />
        </div>
      </div>
    </div>
  );
}

/* ================= SUMMARY PAGE ================= */

function Summary({ analysisResult }) {
  const navigate = useNavigate();

  if (!analysisResult) {
    return (
      <div className="results-page">
        <div className="results-card">
          <h2>No Data</h2>
          <NairaButton text="Go Back" icon="←" onClick={() => navigate("/")} />
        </div>
      </div>
    );
  }

  const { summary, fraud_rings, suspicious_accounts } = analysisResult;

  return (
    <div className="results-page">
      <div className="results-background">
        <Galaxy />
      </div>

      <div className="results-card" style={{ maxWidth: "1100px", overflowX: "auto" }}>
        <h2 className="results-title">Financial Forensics Summary</h2>

        {summary && (
          <>
            <h3 style={{ marginTop: "30px" }}>Overall Metrics</h3>
            <table style={tableStyle}>
              <tbody>
                {Object.entries(summary).map(([key, value]) => (
                  <tr key={key}>
                    <td style={cellHeader}>{key}</td>
                    <td style={cell}>{value !== null ? value.toString() : "N/A"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}

        {fraud_rings?.length > 0 && (
          <>
            <h3 style={{ marginTop: "40px" }}>Fraud Rings</h3>
            <table style={tableStyle}>
              <thead>
                <tr>
                  <th style={cellHeader}>Ring ID</th>
                  <th style={cellHeader}>Pattern</th>
                  <th style={cellHeader}>Risk</th>
                  <th style={cellHeader}>Members</th>
                </tr>
              </thead>
              <tbody>
                {fraud_rings.map(ring => (
                  <tr key={ring.ring_id}>
                    <td style={cell}>{ring.ring_id}</td>
                    <td style={cell}>{ring.pattern_type}</td>
                    <td style={cell}>{ring.risk_score}</td>
                    <td style={cell}>{ring.member_accounts.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}

        {suspicious_accounts?.length > 0 && (
          <>
            <h3 style={{ marginTop: "40px" }}>Suspicious Accounts</h3>
            <table style={tableStyle}>
              <thead>
                <tr>
                  <th style={cellHeader}>Account</th>
                  <th style={cellHeader}>Score</th>
                  <th style={cellHeader}>Patterns</th>
                  <th style={cellHeader}>Ring</th>
                </tr>
              </thead>
              <tbody>
                {suspicious_accounts.map(acc => (
                  <tr key={acc.account_id}>
                    <td style={cell}>{acc.account_id}</td>
                    <td style={cell}>{acc.suspicion_score}</td>
                    <td style={cell}>{acc.detected_patterns.join(", ")}</td>
                    <td style={cell}>{acc.ring_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}

        <div style={{ marginTop: "40px" }}>
          <NairaButton text="Go Back" icon="←" onClick={() => navigate("/results")} />
        </div>

      </div>
    </div>
  );
}

/* ================= ROUTING ================= */

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(() => {
    const saved = localStorage.getItem("analysisResult");
    return saved ? JSON.parse(saved) : null;
  });

  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/explore" element={<Upload setAnalysisResult={setAnalysisResult} />} />
      <Route path="/results" element={<Results analysisResult={analysisResult} />} />
      <Route path="/graph" element={<GraphView analysisResult={analysisResult} />} />
      <Route path="/summary" element={<Summary analysisResult={analysisResult} />} />
    </Routes>
  );
}