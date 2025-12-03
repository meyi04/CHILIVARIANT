<template>
  <div class="page-layout">

    <!-- LEFT CARD -->
    <div class="side-card left-card">
      <div class="card-header">
        <div class="card-icon">🌱</div>
        <h2>Input Guide</h2>
      </div>
      <ul>
        <li><strong>N:</strong> Nitrogen for leaf growth</li>
        <li><strong>P:</strong> Phosphorus for roots</li>
        <li><strong>K:</strong> Potassium for fruits</li>
        <li><strong>pH:</strong> Ideal: 5.5 – 6.8</li>
        <li><strong>Moisture:</strong> Soil water %</li>
        <li><strong>Temperature:</strong> Best: 18°C–30°C</li>
        <li><strong>Humidity:</strong> Affects disease</li>
        <li><strong>Rainfall:</strong> In millimeters</li>
      </ul>
    </div>

    <!-- MAIN CONTAINER -->
    <div class="main-container">
      <!-- HEADER -->
      <div class="header">
        <div class="title-section">
          <h1>🌶️ CHILIVAR-PREDICT</h1>
          <p class="subtitle">Chili Variant Recommendation System</p>
        </div>
        <p class="description">Enter environmental parameters to get the best chili variant for your conditions</p>
      </div>

      <!-- FORM -->
      <form @submit.prevent="predict" class="form-container">
        <div class="form-grid">
          <div v-for="item in fields" :key="item.key" class="input-group">
            <label :for="item.key">{{ item.label }}</label>
            <input 
              type="number" 
              :id="item.key"
              v-model.number="form[item.key]" 
              step="0.1" 
              required 
              class="form-input"
              :class="{ 'input-error': item.key === 'pH_Value' && form.pH_Value > 8 }"
            />
            <div v-if="item.key === 'pH_Value' && form.pH_Value > 8" class="error-text">
              ⚠️ pH should be under 8 for optimal chili growth
            </div>
          </div>
        </div>

        <button 
          type="submit" 
          class="submit-btn" 
          :disabled="isLoading || form.pH_Value > 8"
        >
          <span v-if="!isLoading">🎯 Get Recommendation</span>
          <span v-else class="loading-content">
            <div class="btn-spinner"></div>
            Processing...
          </span>
        </button>
      </form>

      <!-- RESULTS -->
      <div v-if="result" class="results-container">
        <div class="results-header">
          <h3>Recommended Chili Variant</h3>
        </div>
        <div class="prediction-display">
          <div class="variant-result">{{ result }}</div>
          <img 
            v-if="variantImages[result]"
            :src="variantImages[result]"
            :alt="result"
            class="chili-image"
          />
        </div>

        <!-- GROWING GUIDE -->
        <div v-if="variantInfo[result]" class="growing-guide">
          <h4 class="guide-title">🌿 Growing Guide for {{ result }}</h4>
          
          <div class="guide-grid">
            <div class="guide-section">
              <h5>📅 Planting Season</h5>
              <p>{{ variantInfo[result].plantingSeason }}</p>
            </div>
            
            <div class="guide-section">
              <h5>📍 Best Regions</h5>
              <p>{{ variantInfo[result].bestRegions }}</p>
            </div>
            
            <div class="guide-section">
              <h5>⏱️ Growth Duration</h5>
              <p>{{ variantInfo[result].growthDuration }}</p>
            </div>
            
            <div class="guide-section">
              <h5>🌡️ Ideal Temperature</h5>
              <p>{{ variantInfo[result].idealTemperature }}</p>
            </div>
          </div>

          <div class="detailed-info">
            <div class="info-section">
              <h6>💧 Water Requirements</h6>
              <p>{{ variantInfo[result].waterRequirements }}</p>
            </div>
            
            <div class="info-section">
              <h6>🪴 Soil Type</h6>
              <p>{{ variantInfo[result].soilType }}</p>
            </div>
            
            <div class="info-section">
              <h6>☀️ Sunlight Needs</h6>
              <p>{{ variantInfo[result].sunlightNeeds }}</p>
            </div>
            
            <div class="info-section">
              <h6>🌱 Special Care</h6>
              <p>{{ variantInfo[result].specialCare }}</p>
            </div>
          </div>

          <div class="yield-info">
            <h6>📊 Expected Yield & Characteristics</h6>
            <p>{{ variantInfo[result].yieldInfo }}</p>
          </div>
        </div>
      </div>

      <!-- ERROR -->
      <div v-if="error" class="error-message">
        <span class="error-icon">⚠️</span>
        {{ error }}
      </div>
    </div>

    <!-- RIGHT CARD -->
    <div class="side-card right-card">
      <div class="card-header">
        <div class="card-icon">🔥</div>
        <h2>Growth Tips</h2>
      </div>
      <ul>
        <li>🌡️ <strong>Temp:</strong> 20–30°C ideal</li>
        <li>💧 <strong>Moisture:</strong> 40–60% optimal</li>
        <li>☀️ Needs good sunlight</li>
        <li>🌧️ Watch rainfall levels</li>
        <li>🌱 Well-drained soil</li>
        <li>💨 Humidity control</li>
      </ul>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        N: "",
        P: "",
        K: "",
        pH_Value: "",
        Moisture: "",
        Temperature: "",
        Humidity: "",
        Rainfall: ""
      },
      result: "",
      error: "",
      isLoading: false,

      variantImages: {
        "Siling Haba": "/images/siling_haba.jpg",
        "Django F1": "/images/django_f1.jpg",
        "Siling Labuyo": "/images/siling_labuyo.jpg",
        "Lado F1": "/images/lado_f1.jpg",
        "Siling Bilog": "/images/siling_bilog.jpg",
        "Siling Espada": "/images/siling_espada.jpg",
        "PM999 F1": "/images/pm999_f1.jpg",
        "Siling Tingala": "/images/siling_tingala.jpg",
        "Siling Amkis": "/images/siling_amkis.jpg",
        "Siling Marusot": "/images/siling_marusot.jpg"
      },

      // Comprehensive growing information for each variant
      variantInfo: {
        "Siling Haba": {
          plantingSeason: "Year-round in tropical climates, best from January-March and June-August",
          bestRegions: "Central Luzon, CALABARZON, Central Visayas - thrives in warm lowlands",
          growthDuration: "75-90 days to first harvest, continues for 6-8 months",
          idealTemperature: "25-32°C, sensitive to temperatures below 15°C",
          waterRequirements: "Moderate watering - 2-3 times weekly, reduce during rainy season",
          soilType: "Well-drained loamy soil with high organic matter, pH 5.5-6.8",
          sunlightNeeds: "Full sun, 6-8 hours daily minimum",
          specialCare: "Staking recommended for support, watch for aphids and fruit flies",
          yieldInfo: "High yield - 1.5-2 kg per plant. Fruits are 8-12 cm long, mildly spicy (5,000-15,000 SHU)"
        },
        "Django F1": {
          plantingSeason: "Dry season planting preferred - October to February",
          bestRegions: "Ilocos Region, Central Luzon, Cagayan Valley - adaptable to various conditions",
          growthDuration: "65-75 days to maturity, vigorous growth habit",
          idealTemperature: "22-30°C, tolerant of temperature fluctuations",
          waterRequirements: "Regular deep watering, drought tolerant once established",
          soilType: "Fertile, well-drained soil with good moisture retention",
          sunlightNeeds: "Full sun, very heat tolerant",
          specialCare: "Hybrid vigor - resistant to common diseases, minimal pesticide needed",
          yieldInfo: "Excellent yield - 2-2.5 kg per plant. Uniform fruits, high commercial value"
        },
        "Siling Labuyo": {
          plantingSeason: "Throughout the year, peaks during dry months",
          bestRegions: "Nationwide, particularly Bicol, Eastern Visayas, Mindanao",
          growthDuration: "80-100 days, perennial in tropical climates",
          idealTemperature: "20-35°C, very heat tolerant",
          waterRequirements: "Low to moderate - drought resistant, avoid waterlogging",
          soilType: "Adaptable to various soils, prefers slightly acidic to neutral",
          sunlightNeeds: "Full sun to partial shade",
          specialCare: "Minimal care needed, self-seeding, watch for caterpillars",
          yieldInfo: "Moderate yield but continuous - very spicy (80,000-100,000 SHU), small fruits but abundant"
        },
        "Lado F1": {
          plantingSeason: "Year-round except peak rainy season",
          bestRegions: "Central Luzon, Southern Tagalog, urban gardens",
          growthDuration: "70-85 days, compact growth suitable for containers",
          idealTemperature: "24-32°C, protected from strong winds",
          waterRequirements: "Consistent moisture, avoid drying out completely",
          soilType: "Rich, organic soil with good drainage",
          sunlightNeeds: "5-7 hours direct sunlight",
          specialCare: "Good for container gardening, regular feeding recommended",
          yieldInfo: "Good yield - 1-1.5 kg per plant. Medium spice level, attractive color"
        },
        "Siling Bilog": {
          plantingSeason: "Dry to moderate seasons - November to May",
          bestRegions: "Central Visayas, Northern Mindanao, CALABARZON",
          growthDuration: "70-90 days, bushy growth habit",
          idealTemperature: "23-30°C, humid conditions",
          waterRequirements: "Regular watering, sensitive to drought stress",
          soilType: "Moist but well-drained loamy soil",
          sunlightNeeds: "Partial to full sun",
          specialCare: "Pruning helps air circulation, susceptible to fungal diseases in high humidity",
          yieldInfo: "Round fruits, medium yield - versatile for fresh and dried use"
        },
        "Siling Espada": {
          plantingSeason: "Year-round in suitable climates",
          bestRegions: "Bicol Region, Eastern Visayas, spicy cuisine regions",
          growthDuration: "85-100 days, long harvesting period",
          idealTemperature: "25-33°C, warm and humid",
          waterRequirements: "High water needs, consistent moisture required",
          soilType: "Rich, deep soil with high organic content",
          sunlightNeeds: "Full sun, heat loving",
          specialCare: "Needs support for long fruits, regular fertilization",
          yieldInfo: "Long slender fruits (15-20 cm), high yield of very spicy peppers"
        },
        "PM999 F1": {
          plantingSeason: "Optimal during dry cool months - October to March",
          bestRegions: "Benguet, Mountain Province, highland areas",
          growthDuration: "75-85 days, vigorous hybrid",
          idealTemperature: "18-28°C, performs well in cooler climates",
          waterRequirements: "Moderate, well-distributed watering",
          soilType: "Well-drained sandy loam with good fertility",
          sunlightNeeds: "Full sun, adapts to various light conditions",
          specialCare: "Disease resistant, suitable for commercial cultivation",
          yieldInfo: "Commercial grade - uniform fruits, excellent shelf life, high market value"
        },
        "Siling Tingala": {
          plantingSeason: "Traditional planting during summer months",
          bestRegions: "Indigenous areas, backyard gardens, specific local varieties",
          growthDuration: "90-110 days, traditional slow growth",
          idealTemperature: "22-30°C, adapted to local conditions",
          waterRequirements: "Traditional rain-fed or minimal irrigation",
          soilType: "Native soil with minimal amendments",
          sunlightNeeds: "Adapted to local light conditions",
          specialCare: "Heirloom variety, save seeds for next planting",
          yieldInfo: "Traditional yields, unique local characteristics, cultural significance"
        },
        "Siling Amkis": {
          plantingSeason: "Adapted to specific local seasons",
          bestRegions: "Specific localities where traditionally grown",
          growthDuration: "80-95 days, local adaptation",
          idealTemperature: "Local climate adapted",
          waterRequirements: "Natural rainfall pattern adapted",
          soilType: "Local soil conditions",
          sunlightNeeds: "Local light conditions",
          specialCare: "Local growing practices",
          yieldInfo: "Locally adapted yields and characteristics"
        },
        "Siling Marusot": {
          plantingSeason: "Traditional seasonal planting",
          bestRegions: "Specific traditional growing areas",
          growthDuration: "85-105 days, traditional timing",
          idealTemperature: "Locally adapted temperature range",
          waterRequirements: "Traditional water management",
          soilType: "Local soil adaptation",
          sunlightNeeds: "Traditional light adaptation",
          specialCare: "Heritage growing methods",
          yieldInfo: "Traditional yields with unique local traits"
        }
      },

      fields: [
        { label: "Nitrogen (N)", key: "N" },
        { label: "Phosphorus (P)", key: "P" },
        { label: "Potassium (K)", key: "K" },
        { label: "pH Value", key: "pH_Value" },
        { label: "Soil Moisture (%)", key: "Moisture" },
        { label: "Temperature (°C)", key: "Temperature" },
        { label: "Humidity (%)", key: "Humidity" },
        { label: "Rainfall (mm)", key: "Rainfall" }
      ]
    };
  },

  methods: {
    clearForm() {
      this.form = {
        N: "", P: "", K: "", pH_Value: "", 
        Moisture: "", Temperature: "", Humidity: "", Rainfall: ""
      };
    },

    async predict() {
      // Validate pH before submitting
      if (this.form.pH_Value > 8) {
        this.error = "pH should be under 8 for optimal chili growth";
        return;
      }

      this.error = "";
      this.result = "";
      this.isLoading = true;

      try {
        const res = await fetch("http://localhost:5000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form)
        });

        const data = await res.json();

        if (data.error) {
          this.error = data.error;
          return;
        }

        this.result = data.prediction;

        // Save to history
        const history = JSON.parse(localStorage.getItem("history") || "[]");
        history.push({ 
          input: {...this.form}, 
          result: data.prediction, 
          time: new Date().toLocaleString() 
        });
        localStorage.setItem("history", JSON.stringify(history));

        this.clearForm();
      } catch (e) {
        this.error = "Connection error. Please try again.";
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* ===== EXISTING STYLES REMAIN THE SAME ===== */
.page-layout {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 25px;
  min-height: 100vh;
  padding: 30px 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.main-container {
  flex: 1;
  max-width: 700px;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.1),
    0 5px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title-section h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #dc2626;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
  margin: 0 0 20px 0;
}

.description {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  max-width: 500px;
  margin: 0 auto;
}

.form-container {
  margin-bottom: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  letter-spacing: -0.2px;
}

.form-input {
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  background: #f8fafc;
  transition: all 0.2s ease;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #dc2626;
  background: white;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

/* NEW: pH error styling */
.input-error {
  border-color: #dc2626 !important;
  background: #fef2f2 !important;
}

.error-text {
  font-size: 0.8rem;
  color: #dc2626;
  margin-top: 5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
}

.submit-btn {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
  font-family: inherit;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.results-container {
  background: linear-gradient(135deg, #fef2f2, #fff);
  border: 2px solid #fecaca;
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 20px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.results-header h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 20px 0;
  text-align: center;
}

.prediction-display {
  text-align: center;
  margin-bottom: 30px;
}

.variant-result {
  font-size: 1.8rem;
  font-weight: 700;
  color: #dc2626;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.chili-image {
  width: 200px;
  height: 200px;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  border: 3px solid white;
}

/* ===== GROWING GUIDE STYLES ===== */
.growing-guide {
  background: white;
  border-radius: 12px;
  padding: 25px;
  border: 1px solid #e2e8f0;
  margin-top: 20px;
}

.guide-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 25px;
  text-align: center;
  border-bottom: 2px solid #fecaca;
  padding-bottom: 10px;
}

.guide-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.guide-section {
  background: #f8fafc;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #dc2626;
}

.guide-section h5 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.guide-section p {
  font-size: 0.85rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
}

.detailed-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.info-section {
  background: #fef2f2;
  padding: 12px;
  border-radius: 8px;
}

.info-section h6 {
  font-size: 0.8rem;
  font-weight: 600;
  color: #dc2626;
  margin: 0 0 6px 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-section p {
  font-size: 0.8rem;
  color: #57534e;
  line-height: 1.4;
  margin: 0;
}

.yield-info {
  background: linear-gradient(135deg, #fef3c7, #fef7cd);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #fcd34d;
}

.yield-info h6 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #92400e;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.yield-info p {
  font-size: 0.85rem;
  color: #78350f;
  line-height: 1.5;
  margin: 0;
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-weight: 500;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.side-card {
  width: 280px;
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.1),
    0 2px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  position: sticky;
  top: 30px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.card-icon {
  font-size: 1.5rem;
}

.side-card h2 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.side-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side-card li {
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
  color: #475569;
  font-size: 0.9rem;
  line-height: 1.4;
}

.side-card li:last-child {
  border-bottom: none;
}

.side-card li strong {
  color: #dc2626;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 1200px) {
  .page-layout {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .side-card {
    width: 100%;
    max-width: 400px;
    position: static;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 25px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .guide-grid,
  .detailed-info {
    grid-template-columns: 1fr;
  }
  
  .title-section h1 {
    font-size: 1.8rem;
  }
  
  .variant-result {
    font-size: 1.5rem;
  }
  
  .chili-image {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .page-layout {
    padding: 15px;
  }
  
  .main-container {
    padding: 20px;
  }
  
  .title-section h1 {
    font-size: 1.6rem;
  }
  
  .growing-guide {
    padding: 15px;
  }
}
</style>