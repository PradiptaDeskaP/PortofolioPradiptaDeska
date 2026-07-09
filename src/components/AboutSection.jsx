// src/components/AboutSection.jsx

import React from "react";
import "./AboutSection.css";
import myPhoto from "../images_webp/foto1.200f54a4ffa48e32a3ff.webp";
import frameImage from "../images_webp/bingkaifoto.3486378b97855acf3346.webp";

const AboutSection = () => {
  return (
    <section className="about-container">
      {/* Judul di Tengah Atas */}
      <div className="about-title-wrapper">
        <div className="corner-accent-box">
          <h4>About Myself</h4>
        </div>
      </div>
      {/* Intro di Kiri Atas */}
      <div className="about-intro">
        <p>
          Hi, I’m Pradipta Deska – I’m someone who believes that great analysis
          is part creativity, part empathy, and part coffee-fueled hustle.
        </p>
      </div>
      <div className="about-image-wrapper">
        {/* Foto orang sekarang menjadi background-image dari div ini */}
        <div
          className="about-image-person"
          style={{ backgroundImage: `url(${myPhoto})` }}
        ></div>

        {/* Bingkai tetap sebagai img di atasnya */}
        <img
          src={frameImage}
          alt="Bingkai Foto"
          className="about-image-frame"
        />
      </div>
      {/* Konten Utama di Kiri Bawah */}
      <div className="about-main-content">
        <h2>Transforming Ideas into Data-Driven Insights</h2>
        <p>
        With a strong foundation in programming and a keen interest in practical applications of technology, I strive to bring data to life through interactive dashboards and predictive models, helping businesses and organizations make informed, data-backed decisions.
        </p>
        {/* Konten Utama di Kiri Bawah 
        <button className="btn-start-project">Start Your Project</button> */}
      </div>
      {/* Detail di Kanan */}
      <div className="about-details">
        <p>
        Hi, I’m Pradipta Deska – a passionate Data Scientist and Technology enthusiast.
        </p>
        <p>
        I am currently a 6th-semester student at the Department of Data Science Technology, Faculty of Advanced Technology and Multidisciplinary, Universitas Airlangga. I specialize in Data Science, Machine Learning, and Programming, and I am continuously honing my skills in data analysis, statistics, and algorithm design.
        </p>
        {/* Detail di Kanan 
        <a href="#readmore" className="read-more-link">
          Read More ↓
        </a> */}
      </div>
    </section>
  );
};

export default AboutSection;
