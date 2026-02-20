import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";
import "./CipherIntro.css";

export default function CipherIntro() {
  const navigate = useNavigate();
  const introRef = useRef(null);

  useEffect(() => {
    const tl = gsap.timeline();

    tl.fromTo(
      ".cipher-logo",
      { opacity: 0, scale: 0.9 },
      {
        opacity: 1,
        scale: 1,
        duration: 1.5,
        ease: "power4.out"
      }
    )
      .to(".light-sweep", {
        x: "200%",
        duration: 1.2,
        ease: "power2.inOut"
      })
      .to(introRef.current, {
        opacity: 0,
        duration: 1.5,
        delay: 1
      });

    setTimeout(() => {
      navigate("/");
    }, 5000);
  }, [navigate]);

  return (
    <div ref={introRef} className="cipher-intro">
      <div className="logo-wrapper">
        <h1 className="cipher-logo">
          CIPHERFLOW
          <span className="light-sweep"></span>
        </h1>
      </div>
    </div>
  );
}
