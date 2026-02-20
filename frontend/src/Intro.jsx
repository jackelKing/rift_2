import { useEffect, useState } from "react";
import "./Intro.css";
import introSound from "./intro-sound.mp3";

export default function Intro({ onComplete }) {
  const [phase, setPhase] = useState("start");

  useEffect(() => {
    // Play sound
    const audio = new Audio(introSound);
    audio.volume = 0.6;
    audio.play().catch(() => {}); // catch autoplay block silently

    // All timings +0.2s from original
    const t1 = setTimeout(() => setPhase("beam"),  500);   // was 300
    const t2 = setTimeout(() => setPhase("text"),  1500);  // was 900
    const t3 = setTimeout(() => setPhase("glow"),  1800);  // was 1600
    const t4 = setTimeout(() => setPhase("done"),  3400);  // was 3200
    const t5 = setTimeout(() => onComplete?.(),    3800);  // was 3600

    return () => [t1, t2, t3, t4, t5].forEach(clearTimeout);
  }, [onComplete]);

  return (
    <div className={`intro-wrapper ${phase === "done" ? "intro-fade-out" : ""}`}>
      <div className="intro-bg" />

      <div className={`intro-beam ${phase !== "start" ? "intro-beam-active" : ""}`} />

      <div className={`intro-logo ${phase === "text" || phase === "glow" || phase === "done" ? "intro-logo-visible" : ""}`}>
        <span className="intro-cipher">CIPHER</span>
        <span className="intro-flow">FLOW</span>
      </div>

      <div className={`intro-glow ${phase === "glow" || phase === "done" ? "intro-glow-active" : ""}`} />

      <div className="intro-scanlines" />
    </div>
  );
}