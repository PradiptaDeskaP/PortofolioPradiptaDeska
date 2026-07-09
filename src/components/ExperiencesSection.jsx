// src/components/ExperiencesSection.jsx

import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion"; // <-- Impor hooks animasi
import { experiencesData } from "../data/experiences";
import { TimelineLogo } from "./TimelineLogo";
import "./ExperiencesSection.css";

const ExperiencesSection = () => {
  // 1. Buat ref untuk container utama sebagai target scroll
  const containerRef = useRef(null);

  // 2. Lacak progress scroll di dalam container
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start center", "end end"], // Animasi dimulai saat tengah container masuk layar
  });

  // 3. Ubah nilai progress (0-1) menjadi tinggi garis (0% - 100%)
  const beamProgress = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <section className="experiences-section">
      <div className="experiences-title-wrapper">
        <div className="corner-accent-box">
          <h2>Experiences</h2>
        </div>
      </div>
      {/* 4. Terapkan ref ke container timeline */}
      <div className="timeline-container" ref={containerRef}>
        {/* Garis statis abu-abu di belakang */}
        <div className="timeline-line"></div>
        {/* Garis biru animasi yang akan tumbuh */}
        <motion.div
          className="timeline-animated-beam"
          style={{ scaleY: beamProgress }}
        />

        {experiencesData.map((exp, index) => (
          <div
            key={index}
            className={`timeline-item timeline-item-${exp.side}`}
          >
            <TimelineLogo
              scrollYProgress={scrollYProgress}
              totalItems={experiencesData.length}
              index={index}
              logoSrc={exp.logo}
              company={exp.company}
            />
            <div className="timeline-content">
              <span className="timeline-date">{exp.date}</span>
              <h3>{exp.title}</h3>
              <p>{exp.company}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ExperiencesSection;
