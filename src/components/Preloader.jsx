// src/components/Preloader.jsx

import React, { useEffect } from "react";
import gsap from "gsap";
import "./Preloader.css";

const greetings = [
  "Hallo",      // Jerman / Awal
  "Hello",      // Inggris
  "Bonjour",    // Prancis
  "Hola",       // Spanyol
  "Konnichiwa", // Jepang
  "Ciao",       // Italia
  "Nǐ Hǎo",     // China
  "Olá",        // Portugal
  "Halo"        // Indonesia / Akhir
];

const Preloader = ({ onComplete }) => {

  useEffect(() => {
    const textEl = document.querySelector(".preloader-text");
    const charWrappers = document.querySelectorAll(".char-wrapper");

    if (!textEl || charWrappers.length === 0) {
      if (onComplete) onComplete();
      return;
    }

    // 1. Calculate positions and prepare variables
    const containerRect = textEl.getBoundingClientRect();
    const containerCenter = containerRect.left + containerRect.width / 2;
    const containerCenterY = containerRect.top + containerRect.height / 2;

    const startPositions = [];

    charWrappers.forEach((wrapper, index) => {
      const dot = wrapper.querySelector(".char-dot");
      const char = wrapper.querySelector(".char");
      const wrapperRect = wrapper.getBoundingClientRect();
      const wrapperCenter = wrapperRect.left + wrapperRect.width / 2;
      const wrapperCenterY = wrapperRect.top + wrapperRect.height / 2;

      // Distance from wrapper center to text center
      const startX = containerCenter - wrapperCenter;
      const startY = containerCenterY - wrapperCenterY;

      // Spread offsets to cluster dots organically at the center
      const spreadOffsetsX = [-18, -6, 2, 10, 22];
      const spreadOffsetsY = [-10, 10, -5, -12, 8];

      const finalStartX = startX + (spreadOffsetsX[index] || 0);
      const finalStartY = startY + (spreadOffsetsY[index] || 0);

      startPositions.push({ x: finalStartX, y: finalStartY });

      // Initialize positions
      gsap.set(dot, { x: finalStartX, y: finalStartY, scale: 0, opacity: 0 });
      gsap.set(char, { opacity: 0, scale: 0.3 });
    });

    const tl = gsap.timeline({
      onComplete: () => {
        if (onComplete) onComplete();
      }
    });

    // 2. Animate dots appearing in a cluster at the center
    tl.to(".char-dot", {
      scale: 1,
      opacity: 1,
      duration: 0.45,
      stagger: 0.06,
      ease: "back.out(1.8)"
    });

    // 3. Playful cluster wiggle/drift (liquid/gooey feel)
    tl.to(".char-dot", {
      x: (i) => startPositions[i].x * 0.9 + (Math.random() * 8 - 4),
      y: (i) => startPositions[i].y * 0.9 + (Math.random() * 8 - 4),
      duration: 0.4,
      ease: "power2.inOut"
    }, "+=0.1")
      .to(".char-dot", {
        x: (i) => startPositions[i].x * 1.05 + (Math.random() * 6 - 3),
        y: (i) => startPositions[i].y * 1.05 + (Math.random() * 6 - 3),
        duration: 0.3,
        ease: "power1.inOut"
      });

    // 4. Morph animation: Dots fly to their respective letter centers
    charWrappers.forEach((wrapper, index) => {
      const dot = wrapper.querySelector(".char-dot");
      const char = wrapper.querySelector(".char");

      // Fly to individual char center (x: 0, y: 0)
      tl.to(dot, {
        x: 0,
        y: 0,
        duration: 0.6,
        ease: "power4.inOut"
      }, `start-morph+=${index * 0.08}`);

      // Expand dot as it merges into character shape
      tl.to(dot, {
        scale: 4,
        opacity: 0,
        duration: 0.35,
        ease: "power2.out"
      }, `start-morph+=${index * 0.08 + 0.45}`);

      // Fade/Scale in the actual character
      tl.to(char, {
        opacity: 1,
        scale: 1,
        duration: 0.35,
        ease: "back.out(1.5)"
      }, `start-morph+=${index * 0.08 + 0.45}`);
    });

    // 5. Cycle other multilingual greetings (replacing textEl with simple text for transitions)
    greetings.forEach((greeting, index) => {
      if (index === 0) return; // Skip "Hallo" as it's already shown

      tl.to(".preloader-text", {
        opacity: 0,
        scale: 0.95,
        duration: 0.12,
        ease: "power2.in",
        onComplete: () => {
          if (textEl) {
            textEl.innerText = greeting;
          }
        }
      }, "+=0.28"); // Stay visible for 280ms

      tl.to(".preloader-text", {
        opacity: 1,
        scale: 1,
        duration: 0.12,
        ease: "power2.out"
      });
    });

    // 6. Slide entire preloader overlay up to reveal landing page content
    tl.to(".preloader-container", {
      yPercent: -100,
      duration: 0.8,
      ease: "power4.inOut"
    }, "+=0.5");

  }, [onComplete]);

  return (
    <div className="preloader-container">
      <div className="preloader-text-container">
        {/* Render "Hallo" split into wrapper spans containing a dot and the character */}
        <h1 className="preloader-text">
          {["H", "a", "l", "l", "o"].map((char, index) => (
            <span key={index} className="char-wrapper">
              <span className="char-dot"></span>
              <span className="char">{char}</span>
            </span>
          ))}
        </h1>
      </div>
    </div>
  );
};

export default Preloader;
