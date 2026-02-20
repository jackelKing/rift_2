import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div style={{ 
      display: "flex", 
      justifyContent: "center", 
      alignItems: "center", 
      minHeight: "100vh",
      flexDirection: "column",
      gap: "20px"
    }}>
      <h1 style={{ color: "white" }}>TEST PAGE</h1>
      <button
        onClick={() => alert("WORKS!")}
        style={{
          padding: "14px 40px",
          background: "red",
          color: "white",
          border: "none",
          cursor: "pointer",
          fontSize: "20px"
        }}
      >
        CLICK ME
      </button>
    </div>
  );
}