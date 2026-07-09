// src/components/ProjectsSection.jsx

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./ProjectsSection.css";
import { projectsData } from "../data/projects";

const ProjectsSection = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  // Auto-slide effect every 5 seconds (paused on hover)
  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % projectsData.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [isPaused]);

  return (
    <section className="projects-section-v2">
      <div className="projects-container-v2">
        
        {/* Sisi Kiri: Judul dan Deskripsi */}
        <div className="projects-left-v2">
          <h2 className="projects-heading-v2">
            Project <br />
            <span className="gradient-text-v2">Sebelumnya</span>
          </h2>
          <div className="explore-arrow-v2">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path 
                d="M7 17L17 7M17 7H7M17 7V17" 
                stroke="currentColor" 
                strokeWidth="2.5" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>

        {/* Sisi Kanan: Slider Showcase */}
        <div 
          className="projects-right-v2"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          <div className="projects-slider-v2">
            <div 
              className="projects-track-v2"
              style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
              {projectsData.map((project, idx) => (
                <div className="project-slide-v2" key={project.id}>
                  <Link to={`/project/${project.id}`} className="project-card-v2">
                    <div className="slide-image-wrapper">
                      <img 
                        src={project.imageSrc} 
                        alt={project.title} 
                        className="slide-image" 
                      />
                      
                      {/* Hover Overlay */}
                      <div className="slide-overlay">
                        <div className="slide-view-btn">
                          <span>View Project</span>
                          <span className="arrow-circle">
                            <svg 
                              className="project-arrow-svg" 
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
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="slide-info">
                      <h3 className="slide-title">
                        {project.title.split("–")[0]}
                      </h3>
                      <div className="slide-meta">
                        <div className="meta-item">
                          <span className="meta-label">Type:</span>
                          <span className="meta-value">{project.category}</span>
                        </div>
                        <div className="meta-item">
                          <span className="meta-label">Tech:</span>
                          <div className="meta-tech-pills">
                            {project.tech?.slice(0, 3).map((t, i) => (
                              <span key={i} className="tech-pill">{t}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          </div>

          {/* Dots Pagination */}
          <div className="projects-pagination-v2">
            {projectsData.map((_, idx) => (
              <button
                key={idx}
                className={`pagination-dot-v2 ${currentIndex === idx ? "active" : ""}`}
                onClick={() => setCurrentIndex(idx)}
                aria-label={`Go to project slide ${idx + 1}`}
              />
            ))}
          </div>
        </div>

      </div>
    </section>
  );
};

export default ProjectsSection;
