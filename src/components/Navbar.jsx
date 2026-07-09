import React, { useState, useEffect } from "react";
import { Link, scroller } from 'react-scroll';
import "./Navbar.css"; // Kita akan menggunakan CSS yang sama

const Navbar = () => {
  // State untuk melacak kondisi scroll
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState("");
  const [pillStyle, setPillStyle] = useState({ left: 0, width: 0, opacity: 0 });
  const [hoverPillStyle, setHoverPillStyle] = useState({ left: 0, width: 0, opacity: 0 });
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [curtainState, setCurtainState] = useState("idle"); // "idle", "covering", "revealing"

  const handleMobileNav = (to) => {
    const targetOffset = to === "profil" ? -100 : -80;
    if (window.innerWidth < 768) {
      setCurtainState("covering");
      
      // Step 2: At 750ms, close mobile menu and scroll under the curtain
      setTimeout(() => {
        setIsMobileMenuOpen(false);
        scroller.scrollTo(to, {
          spy: true,
          smooth: false, // Instant scroll under the curtain
          offset: targetOffset,
        });
        
        // Step 3: Transition to revealing state (slide columns up to exit)
        setCurtainState("revealing");
      }, 750);

      // Step 4: At 1600ms, reset curtain back to bottom instantly
      setTimeout(() => {
        setCurtainState("idle");
      }, 1600);
    } else {
      // Desktop: normal smooth scroll
      scroller.scrollTo(to, {
        spy: true,
        smooth: true,
        offset: targetOffset,
        duration: 500,
      });
    }
  };

  // Theme state
  const [theme, setTheme] = useState(() => {
    return sessionStorage.getItem('theme') || 'dark';
  });

  // Clean up old localStorage theme to prevent conflicts for existing visitors
  useEffect(() => {
    localStorage.removeItem('theme');
  }, []);

  useEffect(() => {
    if (theme === 'dark') {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    sessionStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  // Update posisi pill aktif secara dinamis
  useEffect(() => {
    const updatePill = () => {
      const activeEl = document.querySelector(".nav-links a.active");
      if (activeEl) {
        setPillStyle({
          left: activeEl.offsetLeft,
          width: activeEl.offsetWidth,
          opacity: 1,
        });
      } else {
        setPillStyle((prev) => ({ ...prev, opacity: 0 }));
      }
    };

    // Jalankan langsung dan beri sedikit penundaan agar render selesai
    updatePill();
    const timer = setTimeout(updatePill, 60);

    window.addEventListener("resize", updatePill);

    return () => {
      window.removeEventListener("resize", updatePill);
      clearTimeout(timer);
    };
  }, [activeSection, isScrolled]);

  const handleSetActive = (to) => {
    setActiveSection(to);
  };

  const handleMouseEnter = (e) => {
    // Ambil element link 'a' di dalam li untuk menghitung offset yang presisi
    const linkEl = e.currentTarget.querySelector("a");
    if (linkEl) {
      setHoverPillStyle({
        left: linkEl.offsetLeft,
        width: linkEl.offsetWidth,
        opacity: 1,
      });
    }
  };

  const handleMouseLeave = () => {
    setHoverPillStyle((prev) => ({ ...prev, opacity: 0 }));
  };

  // Kunci scroll body saat menu mobile terbuka
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isMobileMenuOpen]);

  return (
    <header className="navbar-container">
      {/* Theme Toggle Button */}
      <button 
        className="theme-toggle-btn" 
        onClick={toggleTheme}
        aria-label={theme === 'light' ? "Switch to Dark Mode" : "Switch to Light Mode"}
      >
        {theme === 'light' ? (
          <svg className="theme-icon sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
        ) : (
          <svg className="theme-icon moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        )}
      </button>

      {/* Tombol Menu Mobile (Pojok Kanan Atas) */}
      <button 
        className="mobile-menu-trigger" 
        onClick={() => setIsMobileMenuOpen(true)}
        aria-label="Buka Menu"
      >
        <span>MENU</span>
        <svg className="menu-burger-icon" width="20" height="14" viewBox="0 0 20 14" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M1 1H19M1 7H19M1 13H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
      </button>

      {/* Navbar Desktop standard */}
      <nav className={`navbar-content ${isScrolled ? "scrolled" : ""}`}>
        {/* Bagian Link Navigasi */}
        <ul className="nav-links" onMouseLeave={handleMouseLeave}>
          {/* Container for liquid indicators (gooey filter) */}
          <div className="nav-indicators-container">
            <div className="active-pill-indicator" style={pillStyle}></div>
            <div className="hover-pill-indicator" style={hoverPillStyle}></div>
          </div>

          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="profil"
              spy={true}
              smooth={true}
              offset={-100}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              Home
            </Link>
          </li>
          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="about"
              spy={true}
              smooth={true}
              offset={-80}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              About
            </Link>
          </li>
          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="experiences"
              spy={true}
              smooth={true}
              offset={-80}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              Experiences
            </Link>
          </li>
          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="projects"
              spy={true}
              smooth={true}
              offset={-80}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              Project
            </Link>
          </li>
          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="certifications"
              spy={true}
              smooth={true}
              offset={-80}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              Certification
            </Link>
          </li>
          <li onMouseEnter={handleMouseEnter}>
            <Link
              to="stats"
              spy={true}
              smooth={true}
              offset={-80}
              duration={500}
              activeClass="active"
              onSetActive={handleSetActive}
            >
              Stats
            </Link>
          </li>
        </ul>
      </nav>

      {/* Full-Screen Mobile Menu Overlay */}
      <div className={`mobile-menu-overlay ${isMobileMenuOpen ? "open" : ""}`}>
        <div className="mobile-menu-inner">
          
          {/* Header Area */}
          <div className="mobile-menu-header">
            <div className="mobile-menu-logo">
              <svg className="pd-logo" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="100" rx="15" fill="#111" />
                <path d="M28 25H50C59.3888 25 67 32.6112 67 42C67 51.3888 59.3888 59 50 59H40V75H28V25ZM40 47H50C52.7614 47 55 44.7614 55 42C55 39.2386 52.7614 37 50 37H40V47Z" fill="white" />
                <path d="M50 25C63.8071 25 75 36.1929 75 50C75 63.8071 63.8071 75 50 75" stroke="white" strokeWidth="6" strokeLinecap="round" />
              </svg>
            </div>
            <div className="mobile-menu-title">
              PRADIPTA DESKA / 2026
            </div>
          </div>

          {/* Close Button Block */}
          <div className="close-btn-container">
            <button className="mobile-menu-close" onClick={() => setIsMobileMenuOpen(false)}>
              CLOSE <span className="close-x">✕</span>
            </button>
          </div>

          {/* Numbered Menu Links */}
          <nav className="mobile-menu-nav">
            <div className="mobile-menu-item">
              <span className="item-number">01</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#profil" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("profil");
                  }}
                >
                  Home
                </a>
              </div>
            </div>
            <div className="mobile-menu-item">
              <span className="item-number">02</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#about" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("about");
                  }}
                >
                  About
                </a>
              </div>
            </div>
            <div className="mobile-menu-item">
              <span className="item-number">03</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#experiences" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("experiences");
                  }}
                >
                  Experiences
                </a>
              </div>
            </div>
            <div className="mobile-menu-item">
              <span className="item-number">04</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#projects" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("projects");
                  }}
                >
                  Project
                </a>
              </div>
            </div>
            <div className="mobile-menu-item">
              <span className="item-number">05</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#certifications" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("certifications");
                  }}
                >
                  Certification
                </a>
              </div>
            </div>
            <div className="mobile-menu-item">
              <span className="item-number">06</span>
              <div className="menu-link-wrapper">
                <a 
                  href="#stats" 
                  onClick={(e) => {
                    e.preventDefault();
                    handleMobileNav("stats");
                  }}
                >
                  Stats
                </a>
              </div>
            </div>
          </nav>

          {/* Social Buttons Footer */}
          <div className="mobile-menu-footer">
            <a href="https://github.com/PradiptaDeskaP" target="_blank" rel="noopener noreferrer" className="social-button">
              <svg className="social-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
              <span>GITHUB</span>
            </a>
            <a href="https://www.linkedin.com/in/pradiptadeskapryanda/" target="_blank" rel="noopener noreferrer" className="social-button">
              <svg className="social-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                <rect x="2" y="9" width="4" height="12"></rect>
                <circle cx="4" cy="4" r="2"></circle>
              </svg>
              <span>LINKEDIN</span>
            </a>
          </div>

        </div>
      </div>

      {/* Curtain Transition Overlay for Mobile Navigation */}
      <div className={`transition-curtain ${curtainState}`}>
        <div className="curtain-column">
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block bg"></div>
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block bg"></div>
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block bg"></div>
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
        </div>
        <div className="curtain-column">
          <div className="curtain-block accent"></div>
          <div className="curtain-block bg"></div>
          <div className="curtain-block bg"></div>
        </div>
      </div>

      {/* SVG filter for liquid gooey effect */}
      <svg style={{ position: 'absolute', width: 0, height: 0, pointerEvents: 'none' }} aria-hidden="true" focusable="false">
        <defs>
          <filter id="gooey-navbar">
            <feGaussianBlur in="SourceGraphic" stdDeviation="4.5" result="blur" />
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9" result="goo" />
            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
          </filter>
        </defs>
      </svg>
    </header>
  );
};

export default Navbar;
