// src/components/CertificationsSection.jsx
import React, { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./CertificationsSection.css";
import { certificationsData } from "../data/certifications";

const CertificationsSection = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleScroll = () => {
      if (window.innerWidth > 768) return; // Only apply parallax on mobile carousel

      const containerRect = container.getBoundingClientRect();
      const containerCenter = containerRect.left + containerRect.width / 2;

      const cards = container.querySelectorAll(".certification-card");
      cards.forEach((card) => {
        const cardRect = card.getBoundingClientRect();
        const cardCenter = cardRect.left + cardRect.width / 2;
        const dist = cardCenter - containerCenter;
        
        // Normalize based on card width
        const progress = dist / cardRect.width;
        
        // Clamp to prevent extreme movement
        const clampedProgress = Math.max(-1.5, Math.min(1.5, progress));
        card.style.setProperty("--scroll-progress", clampedProgress);
      });
    };

    // Initial run
    handleScroll();

    container.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleScroll);

    return () => {
      container.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleScroll);
    };
  }, []);

  return (
    <section className="certifications-section">
      <h2 className="section-title">Certifications</h2>
      <div className="certifications-grid" ref={containerRef}>
        {certificationsData.map((cert, index) => (
          <Link
            to={`/certification/${cert.id}`}
            key={cert.id || index}
            className="certification-card"
          >
            <div className="cert-image-container">
              <img
                src={cert.imageSrc}
                alt={cert.title}
                className="cert-image"
              />
              <div className="cert-card-overlay">
                <div className="verify-button">
                  <span>Lihat Detail</span>
                  <svg 
                    className="arrow-icon-svg" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path 
                      d="M5 12H19M19 12L12 5M19 12L12 19" 
                      stroke="currentColor" 
                      strokeWidth="2.5" 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              </div>
            </div>

            <div className="cert-info">
              <span className="cert-issuer">{cert.issuer}</span>
              <h3 className="cert-title">{cert.title}</h3>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
};

export default CertificationsSection;
