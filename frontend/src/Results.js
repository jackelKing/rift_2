import { useNavigate } from "react-router-dom";
import NairaButton from "./NairaButton";
import Galaxy from "./Galaxy";

export default function Results({ analysisResult }) {
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

  return (
    <div className="results-page">

      <div className="results-background">
        <Galaxy />
      </div>

      <div className="results-card">

        <h2 className="results-title">Analysis Complete</h2>

        <p className="results-sub">
          {analysisResult
            ? "Fraud patterns successfully detected within the transaction graph."
            : "No analysis data available. Please upload a file first."}
        </p>

        <div className="results-buttons">
          <NairaButton
            text="View Graph"
            icon="📊"
            onClick={() => navigate("/graph")}
          />
          <NairaButton
            text="View Summary"
            icon="📄"
            onClick={() => navigate("/summary")}
          />
          <NairaButton
            text="Download JSON"
            icon="⬇️"
            onClick={downloadJson}
          />
        </div>

      </div>

    </div>
  );
}