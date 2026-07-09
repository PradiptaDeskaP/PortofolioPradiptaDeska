// src/pages/HomePage.jsx
import React, { useEffect } from 'react';
import HeroSection from '../components/HeroSection';
import AboutSection from '../components/AboutSection';
import ProjectsSection from '../components/ProjectsSection';
import ExperiencesSection from '../components/ExperiencesSection';
import CertificationsSection from '../components/CertificationsSection';
import GithubActivity from '../components/GithubActivity';

import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const HomePage = () => {
  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);

    const ctx = gsap.context(() => {
      // 1. Animasi About Section
      gsap.fromTo(
        ['#about .about-title-wrapper', '#about .about-intro', '#about .about-image-wrapper', '#about .about-main-content', '#about .about-details'],
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#about',
            start: "top 80%",
            toggleActions: "play none none none"
          }
        }
      );

      // 2. Animasi Experiences Section
      gsap.fromTo(
        '#experiences .experiences-title-wrapper',
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#experiences',
            start: "top 80%",
            toggleActions: "play none none none"
          }
        }
      );

      gsap.fromTo(
        '#experiences .timeline-item',
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.2,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#experiences .timeline-container',
            start: "top 75%",
            toggleActions: "play none none none"
          }
        }
      );

      // 3. Animasi Projects Section
      gsap.fromTo(
        '#projects .projects-title',
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#projects',
            start: "top 80%",
            toggleActions: "play none none none"
          }
        }
      );

      gsap.fromTo(
        '#projects .project-card',
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#projects .projects-grid',
            start: "top 75%",
            toggleActions: "play none none none"
          }
        }
      );

      // 4. Animasi Certifications Section
      gsap.fromTo(
        '#certifications .section-title',
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#certifications',
            start: "top 80%",
            toggleActions: "play none none none"
          }
        }
      );

      gsap.fromTo(
        '#certifications .certification-card',
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#certifications .certifications-grid',
            start: "top 75%",
            toggleActions: "play none none none"
          }
        }
      );

      // 5. Animasi Github Activity Section
      gsap.fromTo(
        ['#stats .github-title', '#stats .github-stats-grid', '#stats .terminal-box'],
        { opacity: 0, y: 45 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: '#stats',
            start: "top 80%",
            toggleActions: "play none none none"
          }
        }
      );
    });

    return () => ctx.revert();
  }, []);

  return (
    <main>
      {/* Bungkus setiap section dengan div yang memiliki id */}
      <div id="profil">
        <HeroSection />
      </div>
      <div id="about">
        <AboutSection />
      </div>
      <div id="experiences">
        <ExperiencesSection />
      </div>
      <div id="projects">
        <ProjectsSection />
      </div>
      <div id="certifications">
        <CertificationsSection />
      </div>
      <div id="stats">
        <GithubActivity />
      </div>
    </main>
  );
};

export default HomePage;