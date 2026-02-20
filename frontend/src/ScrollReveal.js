import { useEffect, useRef, useMemo } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import './ScrollReveal.css';


gsap.registerPlugin(ScrollTrigger);

const ScrollReveal = ({
  children,
  enableBlur = true,
  baseOpacity = 0.1,
  baseRotation = 3,
  blurStrength = 4,
  containerClassName = '',
  textClassName = ''
}) => {
  const containerRef = useRef(null);

  const splitText = useMemo(() => {
    const text = typeof children === 'string' ? children : '';
    return text.split(/(\s+)/).map((word, index) => {
      if (word.match(/^\s+$/)) return word;
      return (
        <span className="word" key={index}>
          {word}
        </span>
      );
    });
  }, [children]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const ctx = gsap.context(() => {

      gsap.fromTo(
        el,
        { rotate: baseRotation },
        {
          rotate: 0,
          ease: "none",
          scrollTrigger: {
            trigger: el,
            start: "top bottom",
            end: "bottom center",
            scrub: true
          }
        }
      );

      const words = el.querySelectorAll(".word");

      gsap.fromTo(
        words,
        { opacity: baseOpacity },
        {
          opacity: 1,
          stagger: 0.05,
          ease: "none",
          scrollTrigger: {
            trigger: el,
            start: "top bottom-=20%",
            end: "bottom center",
            scrub: true
          }
        }
      );

      if (enableBlur) {
        gsap.fromTo(
          words,
          { filter: `blur(${blurStrength}px)` },
          {
            filter: "blur(0px)",
            stagger: 0.05,
            ease: "none",
            scrollTrigger: {
              trigger: el,
              start: "top bottom-=20%",
              end: "bottom center",
              scrub: true
            }
          }
        );
      }

    }, el);

    return () => ctx.revert();
  }, [children, enableBlur, baseOpacity, baseRotation, blurStrength]);

  return (
    <h2 ref={containerRef} className={`scroll-reveal ${containerClassName}`}>
      <p className={`scroll-reveal-text ${textClassName}`}>
        {splitText}
      </p>
    </h2>
  );
};

export default ScrollReveal;

