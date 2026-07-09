// src/pages/CertificationDetailPage.jsx

import React, { useState } from 'react'; // <-- Impor useState
import { useParams, Link } from 'react-router-dom';
import { certificationsData } from '../data/certifications';
import { ImageModal } from '../components/ImageModal'; // <-- Impor komponen modal
import './CertificationDetailPage.css';

const CertificationDetailPage = () => {
  const { certId } = useParams();
  const certification = certificationsData.find(c => c.id === certId);

  // State untuk mengontrol modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (!certification) {
    return <div className='cert-not-found'>Sertifikasi tidak ditemukan! <Link to="/">Kembali</Link></div>;
  }

  // Fungsi untuk membuka modal
  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  // Fungsi untuk menutup modal
  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <> {/* Gunakan Fragment agar bisa merender modal di luar main */}
      <main className="cert-detail-container">
        <Link to="/" className="back-link">← Back to Portfolio</Link>
        <div className="cert-header">
          <img src={certification.imageSrc} alt={`${certification.title} logo`} className="cert-logo-large" />
          <div className="cert-header-text">
            <h1>{certification.title}</h1>
            <p>Issued by {certification.issuer} • {certification.date}</p>
          </div>
        </div>

        <div className="cert-main-content">
          <div className="cert-skills">
            <h3>Skills Learned</h3>
            <ul>
              {certification.skills.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="cert-verification">
            <h3>Credential Details</h3>
            <div className="credential-item">
              <span>Credential ID:</span>
              <p>{certification.credentialId}</p>
            </div>
            {/* Ubah <a> menjadi <button> dan tambahkan onClick */}
            <button onClick={handleOpenModal} className="btn-verify">
              <span>Lihat Detail</span>
              <svg 
                className="btn-arrow-svg" 
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
            </button>
          </div>
        </div>
      </main>

      {/* Render komponen modal di sini */}
      <ImageModal 
        isOpen={isModalOpen} 
        onClose={handleCloseModal} 
        imageSrc={certification.imageSrc} 
      />
    </>
  );
};

export default CertificationDetailPage;