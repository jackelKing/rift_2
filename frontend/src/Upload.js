import { useState } from "react";
import { useNavigate } from "react-router-dom";
import NairaButton from "./NairaButton";
import BlurText from "./BlurText";
import Galaxy from "./Galaxy";

export default function Upload({ setAnalysisResult }) {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const navigate = useNavigate();

  const handleDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f && f.name.endsWith(".csv")) {
      setFile(f);
      setFileName(f.name);
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleFileSelect = (e) => {
    const f = e.target.files?.[0];
    if (f && f.name.endsWith(".csv")) {
      setFile(f);
      setFileName(f.name);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(
        `${process.env.REACT_APP_API_URL}/api/analyze/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const json = await res.json();
      console.log("BACKEND RESPONSE:", json);

      setAnalysisResult(json);
      navigate("/results");

    } catch (err) {
      console.error("UPLOAD ERROR:", err);
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

        <div
          className="drop-zone"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <BlurText
            text="Drag & Drop CSV File Here"
            delay={100}
            animateBy="words"
            direction="top"
            className="drop-zone-text"
          />

          <p className="drop-zone-or">or</p>

          <label className="file-input-label">
            <BlurText
              text="Browse File"
              delay={80}
              animateBy="words"
              direction="top"
              className="browse-text"
            />
            <input
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
              hidden
            />
          </label>
        </div>

        {fileName && (
          <>
            <p className="file-name">Selected File: {fileName}</p>
            <NairaButton
              text="Analyze"
              icon="🔍"
              onClick={handleAnalyze}
            />
          </>
        )}

      </div>

    </div>
  );
}