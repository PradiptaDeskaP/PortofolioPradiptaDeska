// src/data/projects.js

// gambar-gambar yang akan digunakan
import projectImage1 from '../images_webp/foto1.200f54a4ffa48e32a3ff.webp';
import projectImage2 from '../images_webp/foto2.d8e82be01ae77cc6c40f.webp';
import projectImage3 from '../images_webp/kupon.webp';
import frameImage from '../images_webp/bingkaifoto.3486378b97855acf3346.webp';
import avatarImage from '../images_webp/avatar.d48a5d00518492bfe234.webp';
import logoPython from '../images_webp/logo_python2.619e73b0bd6dc257548b.webp';
import logoPowerbi from '../images_webp/powerbi.af208df23f726c9d033e.webp';
import logoMysql from '../images_webp/mysql.7c08cca32a24231460fe.webp';
import logoSheets from '../images_webp/logo_sheets.ad592eca753fbffe95a1.webp';
import logoExcel from '../images_webp/logo_excel.314b8bee69b3ced04794.webp';
import logoR from '../images_webp/logo_R.b2c7b2e680afaf1d930f.webp';
import logoLooker from '../images_webp/looker.webp';
import logoColab from '../images_webp/colab.webp';

import klasifikasi1 from '../images_webp/klasifikasi1.webp';
import klasifikasi2 from '../images_webp/klasifikasi2.578f59b04a5e57f2a020.webp';

import clustering1 from '../images_webp/clustering1.f5bf33eb12d399e27d55.webp';
import clustering2 from '../images_webp/clustering2.ea75f411b059ef8fde4a.webp';
import clustering3 from '../images_webp/clustering3.2f2ee483484719838da5.webp';

import app1 from '../images_webp/app1.7e771dfc1d239ca5b121.webp';
import app2 from '../images_webp/app2.4bfc0f598ed23498c0d7.webp';
import app3 from '../images_webp/app3.b3359d710bd0d4f278c7.webp';

export const projectsData = [
  {
    id: "halal-ingredients-checker", 
    title: "Optimalisasi Harga untuk Meningkatkan Penjualan: Analisis Produk Dress Wanita di Tokopedia menggunakan K-Nearest Neighbors",
    popupTitle: "Optimalisasi Harga ✨",
    category: "Classification",
    client: "Internal Project",
    duration: "1 Weeks",
    imageSrc: klasifikasi1,
    gallery: [klasifikasi1, klasifikasi2, ], 
    techLogos: [logoPython, logoColab],
    previewLink: "https://bit.ly/3ScGz7u", // Ganti dengan link Anda
    liveLink: "https://colab.research.google.com/drive/1AqggFnGGhfKD4yczWQxGaw_n_fgzrq7b?usp=sharing",
    overview: "Tujuan projek untuk klasifikasi atau regresi. Model yang digunakan untuk memprediksi jumlah produk yang terjual berdasarkan harga khususnya klasifikasi atau regresi yaitu KNN (K-Nearest Neighbors). Dengan variabel yang digunakan diantaranya Jumlah Terjual Produk (Variabel Dependen) dan Harga, lokasi toko, Rating, Nama Produk (Variabel Dependen)",
    problem: "Penjual sering kali kesulitan dalam menentukan harga yang tepat untuk produk mereka agar menarik pembeli dan meningkatkan penjualan. Selanjutnya ingin membuktikan. Apakah harga benarbenar mempengaruhi jumlah produk yang terjual atau tidak",
    goals: [
      "Menganalisis pengaruh harga terhadap jumlah penjualan untuk memahami apakah harga lebih murah selalu lebih baik dalam menarik pembeli.",
      "Menyediakan rekomendasi harga yang lebih efektif, berdasarkan analisis data harga dan penjualan.",
      "Memberikan pemahaman yang lebih baik kepada penjual tentang bagaimana menetapkan harga produk mereka di pasar e-commerce berdasarkan pola penjualan yang teridentifikasi dari data",
      
    ],
    tech: [
        "Python", "TensorFlow & Keras", "Google Cloud Vision API", "Natural Language Processing (NLP)", "PostgreSQL", "Streamlit"
    ]
  },
  {
    id: "global-oil-gas-insight",
    title: "Analisis Sentimen dan Clustering Tweet Terkait Suku Bunga",
    popupTitle: "Clustering Tweet 📊",
    category: "Clustering",
    client: "Personal Project",
    duration: "2 Weeks",
    imageSrc: clustering2,
    gallery: [clustering1, clustering2, clustering3],
    techLogos: [logoPython, logoSheets],
    previewLink: "https://bit.ly/3SeEGqV", // Ganti dengan link Anda
    liveLink: "https://colab.research.google.com/drive/1Kh9pnYXL-oo10Loo07-OuOG-0M2lAsPk?usp=sharing",  // Ganti dengan link Anda
    overview: "Memahami sentimen publik terhadap suku bunga melalui data media sosial, khususnya Twitter, sulit dilakukan karena volume data yang besar dan keberagaman pendapat. Oleh karena itu, diperlukan sistem otomatis untuk menganalisis sentimen dan mengelompokkan tweet berdasarkan topik terkait untuk mempercepat pemahaman dan pengambilan kebijakan yang lebih tepat. ",
    problem: "Dalam era digital saat ini, media sosial, terutama Twitter, telah menjadi salah satu platform utama bagi masyarakat untuk menyampaikan pendapat mereka, termasuk mengenai isu-isu ekonomi seperti suku bunga. Namun, memahami sentimen publik terhadap suku bunga melalui data yang diperoleh dari media sosial sangatlah sulit. Hal ini disebabkan oleh volume data yang sangat besar serta keberagaman pendapat yang ada, yang membuat analisis secara manual menjadi tidak efektif dan memakan waktu. Oleh karena itu, diperlukan sebuah sistem otomatis yang mampu menganalisis sentimen publik, baik yang positif, negatif, maupun netral, terkait suku bunga, serta mengelompokkan tweet-tweet berdasarkan topik yang relevan. Sistem ini diharapkan dapat mempercepat pemahaman terhadap opini publik dan memberikan wawasan yang lebih tajam bagi pengambil kebijakan dalam mengambil keputusan moneter yang tepat dan berdasarkan data yang akurat.",
    goals: [
      "Menganalisis sentimen publik terkait suku bunga (positif, negatif, netral).",
      "Mengelompokkan tweet berdasarkan topik terkait suku bunga.",
      "Memberikan wawasan berbasis data untuk pengambilan kebijakan moneter."
    ],
    tech: [
        "Power BI", "DAX", "SQL"
    ]
  },
  {
    id: "Analisis-Sentimen-dan-Clustering",
    title: "Pengembangan Sistem Deteksi Hoaks Berbahasa Indonesia Menggunakan Model IndoBERT untuk Meningkatkan Literasi Digital dan Integritas Informasi",
    popupTitle: "Clustering Tweet 📊",
    category: "Machine Learning App",
    client: "Personal Project",
    duration: "2 Weeks",
    imageSrc: app1,
    gallery: [app1, app2, app3],
    techLogos: [logoPython, logoColab],
    previewLink: "https://drive.google.com/file/d/1lVJ66z35UsK6WsgpooxjfH0bwNt4Qv80/view?usp=sharing", // Ganti dengan link Anda
    liveLink: "https://hoaxdetector-production.up.railway.app/dashboard",  // Ganti dengan link Anda
    overview: "Proyek ini bertujuan untuk mengembangkan sistem deteksi hoaks khusus untuk berita berbahasa Indonesia dengan menggunakan model IndoBERT, yaitu model bahasa yang dirancang untuk bahasa Indonesia. Sistem ini akan mengklasifikasikan artikel berita sebagai hoaks atau fakta dengan memanfaatkan teknologi Natural Language Processing (NLP) dan teknik machine learning. Dengan memanfaatkan IndoBERT, sistem ini bertujuan untuk mengatasi masalah penyebaran informasi yang salah dan hoaks di platform digital, serta meningkatkan literasi digital dan integritas informasi.",
    problem: "Perkembangan teknologi digital dan media sosial telah mempermudah penyebaran informasi, namun juga menyebabkan penyebaran hoaks—informasi yang salah atau menyesatkan yang dapat memicu ketegangan sosial, ketidakpercayaan, bahkan konflik. Di Indonesia, maraknya hoaks semakin mengkhawatirkan karena rendahnya literasi digital dan cepatnya penyebaran informasi. Oleh karena itu, diperlukan sebuah sistem otomatis yang dapat mendeteksi hoaks secara cepat dan akurat untuk mengurangi dampak negatif dari disinformasi tersebut. Solusinya adalah mengembangkan sistem deteksi hoaks yang efektif menggunakan IndoBERT.",
    goals: [
      "Mendesain dan mengembangkan arsitektur sistem yang efektif untuk mendeteksi hoaks pada berita berbahasa Indonesia dengan menggunakan model IndoBERT.",
      "Melatih dan mengimplementasikan model IndoBERT untuk mengklasifikasikan berita hoaks berbahasa Indonesia, serta melakukan evaluasi kinerja sistem secara menyeluruh.",
      "Mengatasi tantangan dalam deteksi hoaks, terutama untuk berita yang ambigu atau menyesatkan, dan memastikan sistem dapat menangani kasus-kasus tersebut dengan baik."
    ],
    tech: [
        "Power BI", "DAX", "SQL"
    ]
  },
];