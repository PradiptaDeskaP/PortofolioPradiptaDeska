import React, { useState, useEffect } from "react";
import { Link } from "react-scroll";
import { motion, AnimatePresence } from "framer-motion";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

import "./HeroSection.css";
import Lanyard from "./Lanyard";
// LiquidEther WebGL diganti dengan CSS-only liquid ether (ringan)

// Import gambar
import heroAvatar from "../images_webp/Foto Ryan Casual.9c58595325675ff1df2c.webp";
import stackImage2 from "../images_webp/foto2.d8e82be01ae77cc6c40f.webp";

import logoLooker from "../images_webp/looker.webp";
import logoPowerbi from "../images_webp/powerbi.af208df23f726c9d033e.webp";
import logoMysql from "../images_webp/mysql.7c08cca32a24231460fe.webp";
import logoExcel from "../images_webp/logo_excel.314b8bee69b3ced04794.webp";
import logoPython from "../images_webp/logo_python2.619e73b0bd6dc257548b.webp";
import logoR from "../images_webp/logo_R.b2c7b2e680afaf1d930f.webp";

// Konten flip text
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

// Simple fade variants untuk smooth transition
const fadeVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: "easeInOut"
    }
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.4,
      ease: "easeInOut"
    }
  },
};

const HeroSection = () => {
  const [displayedTitle, setDisplayedTitle] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [loopNum, setLoopNum] = useState(0);
  const [typingSpeed, setTypingSpeed] = useState(150);

  const currentIndex = loopNum % flipTexts.length;

  const [startBadgeAnim, setStartBadgeAnim] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(
    document.body.classList.contains("dark-mode")
  );

  useEffect(() => {
    setIsDarkMode(document.body.classList.contains("dark-mode"));

    const observer = new MutationObserver(() => {
      setIsDarkMode(document.body.classList.contains("dark-mode"));
    });

    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ["class"]
    });

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    // Check if the preloader has already finished
    if (document.body.classList.contains('app-loaded')) {
      setStartBadgeAnim(true);
      return;
    }

    const handleLoaded = () => {
      setStartBadgeAnim(true);
    };

    document.addEventListener('appLoaded', handleLoaded);
    return () => document.removeEventListener('appLoaded', handleLoaded);
  }, []);

  // GSAP scroll-driven parallax animations
  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);

    const ctx = gsap.context(() => {
      // Parallax untuk background orbs
      gsap.to(".orb-1", {
        yPercent: 30,
        ease: "none",
        scrollTrigger: {
          trigger: ".hero-container-v2",
          start: "top top",
          end: "bottom top",
          scrub: true
        }
      });

      gsap.to(".orb-2", {
        yPercent: -20,
        ease: "none",
        scrollTrigger: {
          trigger: ".hero-container-v2",
          start: "top top",
          end: "bottom top",
          scrub: true
        }
      });

      // Parallax untuk kolom kiri (teks)
      gsap.to(".hero-text-content-v2", {
        yPercent: 12,
        ease: "none",
        scrollTrigger: {
          trigger: ".hero-container-v2",
          start: "top top",
          end: "bottom top",
          scrub: true
        }
      });

      // Parallax untuk stack image
      gsap.to(".image-stack-v2", {
        yPercent: -8,
        ease: "none",
        scrollTrigger: {
          trigger: ".hero-container-v2",
          start: "top top",
          end: "bottom top",
          scrub: true
        }
      });
    });

    return () => ctx.revert();
  }, []);

  // Typing animation effect
  useEffect(() => {
    const handleType = () => {
      const fullText = flipTexts[currentIndex].title;

      if (!isDeleting) {
        // Typing
        setDisplayedTitle(fullText.substring(0, displayedTitle.length + 1));
        setTypingSpeed(100); // Speed while typing

        if (displayedTitle === fullText) {
          // Pause when word is complete
          setTypingSpeed(2500); // Pause for 2.5 seconds
          setIsDeleting(true);
        }
      } else {
        // Deleting      x
        setDisplayedTitle(fullText.substring(0, displayedTitle.length - 1));
        setTypingSpeed(50); // Speed while deleting

        if (displayedTitle === "") {
          setIsDeleting(false);
          setLoopNum((prev) => prev + 1);
          setTypingSpeed(500); // Pause before typing next word
        }
      }
    };

    const timer = setTimeout(handleType, typingSpeed);
    return () => clearTimeout(timer);
  }, [displayedTitle, isDeleting, currentIndex, typingSpeed]);



  return (
    <section className="hero-container-v2">
      {/* Background Elements */}
      {isDarkMode ? (
        <div className="hero-liquid-ether-bg">
          <div className="liquid-blob blob-1"></div>
          <div className="liquid-blob blob-2"></div>
          <div className="liquid-blob blob-3"></div>
          <div className="liquid-blob blob-4"></div>
        </div>
      ) : (
        <>
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
        </>
      )}

      <div className="hero-main-content-v2">
        {/* Kolom Kiri */}
        <motion.div
          className="hero-text-content-v2-wrapper"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          style={{ width: "100%" }}
        >
          <div className="hero-text-content-v2">
            {/* Badge dengan efek glassmorphism */}
            <motion.div
              className={`intro-badge ${startBadgeAnim ? "animate-expand" : "animate-circle"}`}
              whileHover={{ scale: 1.05 }}
            >
              <div className="badge-avatar">
                <img src={heroAvatar} alt="Profile" />
                <span className="status-indicator"></span>
              </div>
              <div className="badge-text-container">
                <span className="badge-text">
                  Hi, I'm <strong>Pradipta Deska Pryanda</strong>
                </span>
              </div>
            </motion.div>

            {/* Main Headline dengan Gradient Text */}
            <div className="headline-container">
              <h1 className="gradient-text">
                {displayedTitle}
                <span className="typing-cursor">|</span>
              </h1>

              <AnimatePresence mode="wait">
                <motion.p
                  key={currentIndex}
                  className="hero-subtitle"
                  variants={fadeVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                >
                  {flipTexts[currentIndex].description}
                </motion.p>
              </AnimatePresence>
            </div>

            {/* CTA Buttons */}
            <div className="hero-ctas">
              <motion.button
                className="btn-primary-gradient"
                whileHover={{
                  scale: 1.05,
                  boxShadow: "0 10px 30px rgba(124, 77, 255, 0.4)",
                }}
                whileTap={{ scale: 0.95 }}
              >
                <span>Download CV</span>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
              </motion.button>

              <Link
                to="projects"
                spy={true}
                smooth={true}
                offset={-80}
                duration={500}
                className="btn-secondary-outline"
              >
                View Projects
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </Link>
            </div>

            {/* Quick Stats */}
            <div className="quick-stats">
              <div className="stat-pill">
                <span className="stat-value">11+</span>
                <span className="stat-label">Projects</span>
              </div>
              <div className="stat-pill">
                <span className="stat-value">3+</span>
                <span className="stat-label">Years Exp</span>
              </div>
              <div className="stat-pill">
                <span className="stat-value">9+</span>
                <span className="stat-label">Certs</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Kolom Kanan - Image Stack dengan Auto-Rotation & Hover Pause */}
        {/* Kolom Kanan - React Bits Lanyard 3D */}
        <motion.div
          className="hero-visual-v2"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <Lanyard 
            frontImage={heroAvatar}
            backImage={stackImage2}
            lanyardWidth={1.2}
            position={[0, 1.0, 12.5]}
            gravity={[0, -35, 0]}
          />
        </motion.div>
      </div>

      {/* Tools Section */}
      <motion.div
        className="tools-showcase"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <p className="tools-label">Trusted Technologies</p>
        <div className="tools-slider">
          <div className="tools-track">
            {[
              { logo: logoLooker, name: "Looker Studio", color: "#4285F4" },
              { logo: logoPowerbi, name: "Power BI", color: "#F2C811" },
              { logo: logoPython, name: "Python", color: "#3776AB" },
              { logo: logoR, name: "R Programming", color: "#276DC3" },
              { logo: logoMysql, name: "MySQL", color: "#00758F" },
              { logo: logoExcel, name: "Excel", color: "#217346" },
            ].map((tool, index) => (
              <div
                key={`orig-${index}`}
                className="tool-card"
                style={{ "--tool-color": tool.color }}
              >
                <img src={tool.logo} alt={tool.name} />
                <span>{tool.name}</span>
              </div>
            ))}
            {[
              { logo: logoLooker, name: "Looker Studio", color: "#4285F4" },
              { logo: logoPowerbi, name: "Power BI", color: "#F2C811" },
              { logo: logoPython, name: "Python", color: "#3776AB" },
              { logo: logoR, name: "R Programming", color: "#276DC3" },
              { logo: logoMysql, name: "MySQL", color: "#00758F" },
              { logo: logoExcel, name: "Excel", color: "#217346" },
            ].map((tool, index) => (
              <div
                key={`dup-${index}`}
                className="tool-card"
                style={{ "--tool-color": tool.color }}
              >
                <img src={tool.logo} alt={tool.name} />
                <span>{tool.name}</span>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </section>
  );
};

export default HeroSection;