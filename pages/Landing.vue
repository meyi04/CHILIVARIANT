<template>
  <div class="landing-container">
    <!-- Background with gradient -->
    <div class="background-gradient"></div>
    
    <!-- Main content -->
    <div class="landing-content">
      <!-- Logo -->
      <div class="logo-container">
        <img 
          src="/logo.png" 
          alt="Chili Recommendation System" 
          class="logo"
          @error="handleImageError"
        />
      </div>

      <!-- Title and Description -->
      <div class="text-content">
   
        <p class="subtitle">Intelligent Chili Variant Recommendation System</p>
        <p class="description">
          Get personalized chili cultivation recommendations based on soil conditions, 
          climate data, and environmental factors for optimal growth and yield.
        </p>
      </div>

      <!-- Get Recommendation Button -->
      <button 
        class="recommendation-btn" 
        @click="getRecommendation"
        :disabled="loading"
      >
        <span v-if="!loading">Get Recommendation</span>
        <div v-else class="loading-spinner">
          <div class="spinner"></div>
          <span>Loading...</span>
        </div>
      </button>

      <!-- Loading Progress Bar -->
      <div v-if="loading" class="progress-container">
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: progress + '%' }"
          ></div>
        </div>
        <p class="progress-text">{{ Math.round(progress) }}%</p>
      </div>
    </div>

    <!-- Decorative Elements -->
    <div class="floating-elements">
      <div class="floating-element element-1"></div>
      <div class="floating-element element-2"></div>
      <div class="floating-element element-3"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      loading: false,
      progress: 0
    }
  },
  methods: {
    async getRecommendation() {
      this.loading = true;
      this.progress = 0;
      
      // Simulate loading progress
      const interval = setInterval(() => {
        this.progress += Math.random() * 25;
        if (this.progress >= 100) {
          this.progress = 100;
          clearInterval(interval);
          
          // Navigate to home after completion
          setTimeout(() => {
            this.$router.push('/home');
          }, 500);
        }
      }, 250);
    },
    
    handleImageError(event) {
      console.error('Logo image not found. Please add logo.png to public folder');
      // Fallback to text logo
      event.target.style.display = 'none';
      const logoContainer = event.target.parentElement;
      logoContainer.innerHTML = `
        <div class="text-logo">
          <span class="logo-icon">🌶️</span>
          <span class="logo-text">ChiliAI</span>
        </div>
      `;
    }
  }
}
</script>

<style scoped>
.landing-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #c51a1aff 0%, #052b01ff 100%);
}

.background-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(3, 135, 42, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(4, 154, 37, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(6, 234, 97, 0.2) 0%, transparent 50%);
  animation: gradientShift 10s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.landing-content {
  text-align: center;
  z-index: 2;
  position: relative;
  max-width: 600px;
  padding: 2rem;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  max-width: 250px;
  height: auto;
  filter: drop-shadow(0 8px 25px rgba(255, 255, 255, 0.5));
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.text-content {
  margin-bottom: 3rem;
}

.title {
  font-size: 3.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1.5rem;
  font-weight: 300;
  letter-spacing: 0.5px;
}

.description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 0;
}

.recommendation-btn {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  border: none;
  padding: 1.2rem 3rem;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
  position: relative;
  overflow: hidden;
}

.recommendation-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
}

.recommendation-btn:active:not(:disabled) {
  transform: translateY(-1px);
}

.recommendation-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.progress-container {
  margin-top: 2rem;
  width: 100%;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6b6b, #ee5a24);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin: 0;
}

.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.floating-element {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.element-1 {
  width: 100px;
  height: 100px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.element-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 10%;
  animation-delay: -2s;
}

.element-3 {
  width: 70px;
  height: 70px;
  bottom: 20%;
  left: 20%;
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

/* Text logo fallback styles */
.text-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 4rem;
  filter: drop-shadow(0 8px 25px rgba(0, 0, 0, 0.2));
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Responsive Design */
@media (max-width: 768px) {
  .landing-content {
    padding: 1rem;
    max-width: 90%;
  }
  
  .title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .description {
    font-size: 1rem;
  }
  
  .recommendation-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
  
  .logo {
    max-width: 120px;
  }
}
</style>