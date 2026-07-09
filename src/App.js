// src/App.js

import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import FollowingPointer from './components/FollowingPointer';
import HomePage from './pages/HomePage'; // Kita akan buat halaman ini
import ProjectDetailPage from './pages/ProjectDetailPage'; // dan ini
import CertificationDetailPage from './pages/CertificationDetailPage';
import Preloader from './components/Preloader';
import './App.css'; // CSS untuk styling halaman

import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const lenisRef = useRef(null);

  useEffect(() => {
    // Inisialisasi Lenis untuk smooth scrolling
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // standard easing function
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
      infinite: false,
    });

    lenisRef.current = lenis;

    // Awalnya matikan scroll saat preloader berjalan
    lenis.stop();

    // Update ScrollTrigger saat terjadi scroll via Lenis
    lenis.on('scroll', ScrollTrigger.update);

    // Integrasi dengan GSAP ticker
    const tick = (time) => {
      lenis.raf(time * 1000);
    };
    gsap.ticker.add(tick);

    // Menonaktifkan lag smoothing agar animasi scroll sinkron dengan render
    gsap.ticker.lagSmoothing(0);

    return () => {
      lenis.destroy();
      gsap.ticker.remove(tick);
    };
  }, []);

  // Nyalakan kembali Lenis scroll dan body overflow saat preloader selesai
  useEffect(() => {
    if (isLoaded) {
      document.body.style.overflow = "unset";
      document.body.classList.add('app-loaded');
      document.dispatchEvent(new CustomEvent('appLoaded'));
      if (lenisRef.current) {
        lenisRef.current.start();
      }
    } else {
      document.body.style.overflow = "hidden";
      document.body.classList.remove('app-loaded');
      if (lenisRef.current) {
        lenisRef.current.stop();
      }
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isLoaded]);

  return (
    <Router>
      <div className="App">
        {/* Preloader overlay di paling atas */}
        <Preloader onComplete={() => setIsLoaded(true)} />
        
        <FollowingPointer />
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/project/:projectId" element={<ProjectDetailPage />} />
          <Route path="/certification/:certId" element={<CertificationDetailPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;