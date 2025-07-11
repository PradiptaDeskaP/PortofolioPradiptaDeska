// src/data/certifications.js

// Impor gambar/logo untuk sertifikasi Anda
import linearAplikasi1 from '../images/linearAplikasi1.png';
import linearAplikasi2 from '../images/linearAplikasi2.png';
import linearFundamental1 from '../images/linearFundamental1.png';
import linearFundamental2 from '../images/linearFundamental2.png';
import adse from '../images/adse.png';
import digistar from '../images/digistar.png';

export const certificationsData = [
  {
    id: "meta-data-analyst",
    title: "Linear Regression in Machine Learning_Application",
    issuer: "Digitalent by Komdigi", // Penerbit sertifikat
    date: "Oktober 2023",
    credentialId: "19510458840-390/FGA/BLSDM.Komdigi/2025", // Ganti dengan ID asli
    imageSrc: linearAplikasi1,
    skills: [
      "Regresi Linier: Penerapan model regresi untuk memprediksi variabel numerik",
      "Logistic Regression: Digunakan untuk klasifikasi dalam machine learning",
      "Evaluasi dan Pengujian Model: Metode untuk mengevaluasi akurasi dan performa model linear dalam aplikasi",
      "Pemrograman dengan Tools seperti R, Python, dan lainnya untuk membangun dan melatih model linear.",
    ],
  },
  {
    id: "dicoding-ml-developer",
    title: "SAP Analytics Cloud",
    issuer: "ASEAN DATA SCIENCE EXPLORER",
    date: "April 2024",
    imageSrc: adse,
    skills: [
      "Penggunaan bahasa pemrograman seperti Python, R, dan SQL untuk memanipulasi dan menganalisis data.",
      "Penggunaan statistik deskriptif untuk menggambarkan pola dalam data dan mengidentifikasi hubungan antara variabel",
      "Pengenalan pada platform cloud computing dan big data tools seperti Hadoop dan Spark yang digunakan untuk pemrosesan data dalam skala besar",
      "Implementasi teknik pemodelan prediktif untuk meramalkan tren dan hasil berdasarkan data yang ada",
    ],
  },
  {
    id: "dicoding-ml-developer",
    title: "Digistar Class",
    issuer: "Digistar By Telkom",
    date: "Oktober 2024",
    imageSrc: digistar,
    skills: [
      "Kolaborasi tim dalam proyek teknologi",
      "Penyelesaian masalah terkait aplikasi digital dan komunikasi teknis dalam tim",
      "Pengenalan dasar aplikasi berbasis web atau mobile",
      
    ],

  },
  
];