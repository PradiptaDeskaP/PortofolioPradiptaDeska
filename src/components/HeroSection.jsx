import React, { useState, useEffect } from "react";
import { Link } from "react-scroll";

import "./HeroSection.css";
import { AnimatedImageStack } from "./AnimatedImageStack";
import { HoverBorderGradient } from "./HoverBorderGradient";

import heroAvatar from "../images/Foto Ryan Casual.jpg";
import stackImage1 from "../images/foto1.jpg"; // Ganti dengan nama file Anda
import stackImage2 from "../images/foto2.jpg"; // Ganti dengan nama file Anda

import logoLooker from "../images/looker.png";
import logoPowerbi from "../images/powerbi2.jpg";
import logoMysql from "../images/mysql.png";
import logoExcel from "../images/logo_excel.png";
import logoPython from "../images/logo_python2.png";
import logoR from "../images/logo_R.png";

// 2. Gunakan VARIABEL hasil impor di dalam array
const stackImages = [
  { src: heroAvatar }, // Bisa menggunakan gambar yang sama
  { src: stackImage2 },
  { src: stackImage1 },
];

const flipTexts = [
  {
    title: "Data Analyst",
    description:
      "Mengkhususkan diri dalam mengubah data kompleks menjadi wawasan yang dapat ditindaklanjuti dan membangun sistem cerdas",
  },
  {
    title: "Business Intelligence",
    description:
    "Saya membangun dan menerapkan model pembelajaran mesin untuk menyelesaikan masalah bisnis dunia nyata secara efisien.",
  },
  {
    title: "Business Analyst",
    description:
      "Menyukai menemukan cerita dan pola dalam data untuk membantu mengambil keputusan strategis perusahaan",
  },
];

const HeroSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipping, setIsFlipping] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsFlipping(true);
      setTimeout(() => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % flipTexts.length);
        setIsFlipping(false);
      }, 500);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="hero-container">
      <div className="hero-main-content">
        {/* === Kolom Kiri: Konten Teks === */}
        <div className="hero-text-content">
          <div className="intro-tag">
            <img
              src={heroAvatar}
              alt="Pradipta Deska Pryanda"
              className="intro-avatar"
            />
            <span>Hi! I am Pradipta Deska Pryanda</span>
          </div>
          <div
            className={`flipping-text-container ${
              isFlipping ? "flipping" : ""
            }`}
          >
            <h1>{flipTexts[currentIndex].title}</h1>
            <p className="hero-description">
              {flipTexts[currentIndex].description}
            </p>
          </div>
          <div className="hero-buttons">
            <HoverBorderGradient as="button" duration={2} borderRadius="8px">
              Download My CV
            </HoverBorderGradient>

            <Link
              to="projects" // ID dari section tujuan
              spy={true}
              smooth={true}
              offset={-80} // Jarak dari atas (agar tidak tertutup navbar)
              duration={500}
              className="btn-secondary" // Gunakan kelas yang sama agar gaya tidak berubah
            >
              Projects
            </Link>
          </div>
        </div>

        {/* === Kolom Kanan: Gambar Utama === */}
        <div className="hero-image-container">
          <AnimatedImageStack items={stackImages} />
        </div>
      </div>

      <div className="bottom-content">
        <div className="tools-section">
          {/* === Kartu Keahlian === */}
          <h4 className="bottom-content-title">Tools & Technologies</h4>
          <div className="expertise-logos">
            <div className="logo-wrapper">
              <img
                src={logoLooker}
                alt="Data Mastery"
                className="expertise-logo"
              />
              <div className="logo-popup">Looker Studio</div>
            </div>
            <div className="logo-wrapper">
              <img
                src={logoPowerbi}
                alt="AI Integration"
                className="expertise-logo"
              />
              <div className="logo-popup">Power Bi</div>
            </div>
            <div className="logo-wrapper">
              <img src={logoMysql} alt="ChatGPT" className="expertise-logo" />
              <div className="logo-popup">Mysql</div>
            </div>
            <div className="logo-wrapper">
              <img src={logoExcel} alt="Langchain" className="expertise-logo" />
              <div className="logo-popup">Excel</div>
            </div>
            <div className="logo-wrapper">
              <img src={logoPython} alt="Python" className="expertise-logo" />
              <div className="logo-popup">Python</div>
            </div>
            <div className="logo-wrapper">
              <img src={logoR} alt="Rstudio" className="expertise-logo" />
              <div className="logo-popup">R</div>
            </div>
          </div>
        </div>

        {/* === Statistik Pengalaman === 
        <div className="experience-snapshot">
          <p className="snapshot-title">Experience Snapshot</p>
          <div className="stats-container">
            <div className="stat-item">
              <span className="stat-number">11+</span>
              <span className="stat-label">Project Completed</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">3+</span>
              <span className="stat-label">Years Experience</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">9+</span>
              <span className="stat-label">Certificates earned</span>
            </div>
          </div>
        </div>
        */}
      </div>
    </section>
  );
};

export default HeroSection;
