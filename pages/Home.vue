<template>
  <div class="home-container">

    <!-- HEADER SECTION -->
    <div class="header-section">
      <h1 class="title">🌶 CHILIVAR-PREDICT</h1>
      <p class="subtitle">
        AI-powered chili variant recommendation system based on environmental conditions
      </p>
    </div>

    <!-- CAROUSEL SECTION -->
    <div class="carousel-section">
      <div class="carousel-wrapper">
        <div class="carousel" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
          <div class="slide" v-for="(chili, index) in chiliVariants" :key="index">
            <img :src="chili.img" :alt="chili.name" class="chili-img" />
            <div class="slide-content">
              <h3 class="chili-name">{{ chili.name }}</h3>
              <p class="chili-desc">{{ getChiliDescription(chili.name) }}</p>
            </div>
          </div>
        </div>

        <button class="arrow left" @click="prevSlide">‹</button>
        <button class="arrow right" @click="nextSlide">›</button>
        
        <div class="carousel-dots">
          <span 
            v-for="(dot, index) in chiliVariants" 
            :key="index"
            :class="['dot', { active: currentIndex === index }]"
            @click="currentIndex = index"
          ></span>
        </div>
      </div>
    </div>

    <!-- CTA BUTTON -->
    <div class="cta-section">
      <router-link to="/input">
        <button class="start-btn">
          🚀 Get Started
        </button>
      </router-link>
    </div>

    <!-- CHILI VARIANTS GRID -->
    <div class="info-section">
      <div class="section-header">
        <h2 class="info-title">🌱 Explore Chili Variants</h2>
        <p class="info-subtitle">Discover different chili types and their characteristics</p>
      </div>

      <div class="variant-grid">
        <div class="variant-card" v-for="(item, i) in chiliInfo" :key="i">
          <div class="card-image">
            <img :src="item.img" :alt="item.name" class="variant-img" />
            <div class="card-overlay"></div>
          </div>
          <div class="card-content">
            <h3>{{ item.name }}</h3>
            <p>{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      currentIndex: 0,
      autoSlideInterval: null,

      chiliVariants: [
        { name: "Siling Labuyo", img: "/images/labuyo.jpg" },
        { name: "Siling Haba", img: "/images/siling_haba.jpg" },
        { name: "Django F1", img: "/images/django_f1.jpg" },
        { name: "Lado F1", img: "/images/lado_f1.jpg" },
        { name: "Siling Bilog", img: "/images/siling_bilog.jpg" }
      ],

      chiliInfo: [
        {
          name: "Siling Labuyo",
          img: "/images/labuyo.jpg",
          desc: "A native Filipino chili known for its very strong heat despite its small size."
        },
        {
          name: "Siling Haba",
          img: "/images/siling_haba.jpg",
          desc: "Mildly spicy and commonly used in Filipino dishes such as sinigang and paksiw."
        },
        {
          name: "Django F1",
          img: "/images/django_f1.jpg",
          desc: "A high-yield hybrid chili variety with uniform fruits and moderate heat."
        },
        {
          name: "Lado F1",
          img: "/images/lado_f1.jpg",
          desc: "A long green chili hybrid known for excellent fruit quality and disease resistance."
        },
        {
          name: "Siling Bilog",
          img: "/images/siling_bilog.jpg",
          desc: "Round chili pepper usually used for pickling and traditional sauces."
        },
        {
          name: "Siling Espada",
          img: "/images/siling_espada.jpg",
          desc: "Long sword-shaped chili with medium heat, ideal for drying and processing."
        },
        {
          name: "PM999 F1",
          img: "/images/pm999_f1.jpg",
          desc: "A hybrid chili variant known for high yield and adaptability to hot climates."
        },
        {
          name: "Siling Tingala",
          img: "/images/siling_tingala.jpg",
          desc: "A spicy upward-growing chili variety often found in backyard farms."
        },
        {
          name: "Siling Amkis",
          img: "/images/siling_amkis.jpg",
          desc: "A distinct local chili variety known for its strong aroma and heat."
        },
        {
          name: "Siling Marusot",
          img: "/images/siling_marusot.jpg",
          desc: "A unique local variant recognized by its twisted shape and sharp spiciness."
        },
        {
          name: "Serrano Pepper",
          img: "/images/serrano.jpg",
          desc: "Crunchy and spicy, commonly used in Mexican dishes and fresh salsas."
        },
        {
          name: "Jalapeño",
          img: "/images/jalapeno.jpg",
          desc: "A world-famous chili with moderate heat; great for stuffing and nachos."
        },
        {
          name: "Cayenne Pepper",
          img: "/images/cayenne.jpg",
          desc: "Long and thin chili often dried and ground into powder; strong heat."
        }
      ]
    };
  },

  methods: {
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.chiliVariants.length;
    },
    
    prevSlide() {
      this.currentIndex = (this.currentIndex - 1 + this.chiliVariants.length) % this.chiliVariants.length;
    },

    getChiliDescription(name) {
      const chili = this.chiliInfo.find(item => item.name === name);
      return chili ? chili.desc : 'Discover this amazing chili variant';
    },

    startAutoSlide() {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide();
      }, 4000);
    },

    stopAutoSlide() {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval);
      }
    }
  },

  mounted() {
    this.startAutoSlide();
  },

  beforeUnmount() {
    this.stopAutoSlide();
  }
};
</script>

<style scoped>
/* ===== BASE STYLES ===== */
.home-container {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* ===== HEADER SECTION ===== */
.header-section {
  text-align: center;
  margin-bottom: 50px;
}

.title {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 15px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1.2rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
  font-weight: 500;
}

/* ===== CAROUSEL SECTION ===== */
.carousel-section {
  margin-bottom: 50px;
}

.carousel-wrapper {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 8px 16px rgba(0, 0, 0, 0.08);
  background: white;
}

.carousel {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  height: 500px;
}

.slide {
  min-width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chili-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.slide-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
  padding: 30px;
  text-align: left;
}

.chili-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: white;
}

.chili-desc {
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.5;
  margin: 0;
}

/* ===== CAROUSEL CONTROLS ===== */
.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.arrow:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
}

.arrow.left { 
  left: 20px; 
}

.arrow.right { 
  right: 20px; 
}

.carousel-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot.active {
  background: white;
  transform: scale(1.2);
}

.dot:hover {
  background: rgba(255, 255, 255, 0.8);
}

/* ===== CTA BUTTON ===== */
.cta-section {
  text-align: center;
  margin-bottom: 60px;
}

.start-btn {
  padding: 18px 40px;
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  color: white;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 
    0 8px 25px rgba(220, 38, 38, 0.3),
    0 4px 12px rgba(220, 38, 38, 0.2);
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 
    0 15px 35px rgba(220, 38, 38, 0.4),
    0 8px 20px rgba(220, 38, 38, 0.3);
}

.start-btn:active {
  transform: translateY(-1px);
}

/* ===== INFO SECTION ===== */
.info-section {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.info-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 15px;
  background: linear-gradient(135deg, #059669, #10b981);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.info-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  max-width: 500px;
  margin: 0 auto;
}

/* ===== VARIANT GRID ===== */
.variant-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  padding: 0 10px;
}

.variant-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
}

.variant-card:hover {
  transform: translateY(-8px);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 8px 16px -4px rgba(0, 0, 0, 0.1);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.variant-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.variant-card:hover .variant-img {
  transform: scale(1.1);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.1));
}

.card-content {
  padding: 25px;
}

.card-content h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.card-content p {
  color: #64748b;
  line-height: 1.5;
  margin: 0;
  font-size: 0.95rem;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 1024px) {
  .carousel-wrapper {
    max-width: 95%;
  }
  
  .carousel {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 30px 15px;
  }
  
  .title {
    font-size: 2.2rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .carousel {
    height: 350px;
  }
  
  .chili-name {
    font-size: 1.6rem;
  }
  
  .chili-desc {
    font-size: 1rem;
  }
  
  .arrow {
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
  }
  
  .start-btn {
    padding: 16px 32px;
    font-size: 1.2rem;
  }
  
  .info-title {
    font-size: 2rem;
  }
  
  .variant-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.8rem;
  }
  
  .carousel {
    height: 300px;
  }
  
  .slide-content {
    padding: 20px;
  }
  
  .chili-name {
    font-size: 1.3rem;
  }
  
  .variant-grid {
    grid-template-columns: 1fr;
  }
  
  .card-content {
    padding: 20px;
  }
}
</style>