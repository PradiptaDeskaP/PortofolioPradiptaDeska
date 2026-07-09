// src/components/TimelineLogo.jsx

import React from 'react';
import { motion, useTransform } from 'framer-motion';

// PASTIKAN ADA KATA 'export' DI SINI
export const TimelineLogo = ({ scrollYProgress, totalItems, index, logoSrc, company }) => {
  const [isDark, setIsDark] = React.useState(document.body.classList.contains('dark-mode'));

  React.useEffect(() => {
    setIsDark(document.body.classList.contains('dark-mode'));
    const observer = new MutationObserver(() => {
      setIsDark(document.body.classList.contains('dark-mode'));
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    return () => observer.disconnect();
  }, []);

  // Menghitung rentang aktif untuk setiap logo berdasarkan posisinya
  const start = index / totalItems;
  const end = (index + 1) / totalItems;

  const baseBorderColor = isDark ? "rgba(255, 255, 255, 0.1)" : "#dee2e6";
  const activeBorderColor = "#7C4DFF"; // Primary design system color

  // Mengubah warna border saat scrollYProgress berada dalam rentang logo ini
  const borderColor = useTransform(
    scrollYProgress,
    [start, (start + end) / 2, end], // Input: Awal, Tengah, Akhir rentang
    [baseBorderColor, activeBorderColor, baseBorderColor]
  );

  return (
    <div className="timeline-logo-wrapper">
      <motion.div 
        className="timeline-logo-border"
        style={{ borderColor }} // Terapkan warna border yang dianimasikan
      />
      <img src={logoSrc} alt={`${company} logo`} className="timeline-logo-img" />
    </div>
  );
};