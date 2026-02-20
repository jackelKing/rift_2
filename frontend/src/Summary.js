export default function Summary({ report }) {
  if (!report || !report.summary) {
    return (
      <div className="results-page">
        <div className="results-card">
          <h2 className="results-title">No Data Available</h2>
          <p className="results-sub">
            Please upload and analyze a dataset first.
          </p>
        </div>
      </div>
    );
  }

  const { summary } = report;

  return (
    <div className="results-page">

      <div className="results-background"></div>

      <div
        className="results-card"
        style={{
          maxWidth: "700px",
          width: "90%",
          textAlign: "left"
        }}
      >
        <h2 className="results-title" style={{ textAlign: "center" }}>
          Financial Network Analysis Summary
        </h2>

        <p
          className="results-sub"
          style={{ textAlign: "center", marginBottom: "40px" }}
        >
          High-level insights extracted from transaction graph
        </p>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "20px"
          }}
        >
          <div className="summary-card">
            <p className="summary-label">Total Accounts</p>
            <p className="summary-value">
              {summary.total_accounts}
            </p>
          </div>

          <div className="summary-card">
            <p className="summary-label">Total Fraud Rings Detected</p>
            <p className="summary-value">
              {summary.total_rings}
            </p>
          </div>

          <div className="summary-card">
            <p className="summary-label">Processing Time</p>
            <p className="summary-value">
              {summary.processing_time_seconds}s
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}