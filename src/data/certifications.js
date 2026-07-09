// src/data/certifications.js

// Impor gambar/logo untuk sertifikasi Anda
import linearAplikasi1 from '../images_webp/linearAplikasi1.4060ae34a5a3157d8c81.webp';
import linearAplikasi2 from '../images_webp/linearAplikasi2.7c3002dfe6d1a2109e17.webp';
import linearFundamental1 from '../images_webp/linearFundamental1.0d05a3b8d6142b7e4d11.webp';
import linearFundamental2 from '../images_webp/linearFundamental2.c1917b3d93ab8b208e29.webp';
import adse from '../images_webp/adse.aaa41c286697de48ac94.webp';
import digistar from '../images_webp/digistar.765f5e76020342992b2a.webp';

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