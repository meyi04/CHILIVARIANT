<template>
  <div class="history-container">
    <!-- HEADER -->
    <div class="header-section">
      <h1 class="title">📜 Prediction History</h1>
      <p class="subtitle">Review your previous chili variant predictions and inputs</p>
    </div>

    <!-- FILTERS SECTION -->
    <div class="filters-section">
      <div class="filter-group">
        <label class="filter-label">Filter by Variant</label>
        <select v-model="selectedVariant" class="filter-dropdown">
          <option value="">All Variants</option>
          <option 
            v-for="variant in variants"
            :key="variant"
            :value="variant"
          >
            {{ variant }}
          </option>
        </select>
      </div>

      <div class="date-filter-group">
        <div class="filter-group">
          <label class="filter-label">From Date</label>
          <input type="date" v-model="dateFrom" class="date-input" />
        </div>

        <div class="filter-group">
          <label class="filter-label">To Date</label>
          <input type="date" v-model="dateTo" class="date-input" />
        </div>
      </div>

      <button @click="clearFilters" class="clear-filters-btn">
        🗑️ Clear Filters
      </button>
    </div>

    <!-- STATS -->
    <div v-if="filteredRecords.length > 0" class="stats-section">
      <div class="stat-card">
        <div class="stat-number">{{ filteredRecords.length }}</div>
        <div class="stat-label">Total Records</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ uniqueVariantsCount }}</div>
        <div class="stat-label">Unique Variants</div>
      </div>
    </div>

    <!-- NO RECORDS -->
    <div v-if="filteredRecords.length === 0" class="empty-state">
      <div class="empty-icon">📊</div>
      <h3>No History Found</h3>
      <p>No prediction records match your current filters.</p>
      <button @click="clearFilters" class="cta-button">
        View All Records
      </button>
    </div>

    <!-- HISTORY CARDS -->
    <div v-else class="history-grid">
      <div 
        v-for="(rec, index) in filteredRecords"
        :key="index"
        class="history-card"
      >
        <div class="card-header">
          <div class="variant-badge">
            <span class="variant-icon">🌶️</span>
            <h3 class="variant-name">{{ rec.result }}</h3>
          </div>
          <div class="timestamp">{{ formatDate(rec.time) }}</div>
        </div>

        <div class="card-content">
          <div class="input-summary">
            <div class="input-item">
              <span class="input-label">N-P-K:</span>
              <span class="input-value">{{ rec.input.N }}-{{ rec.input.P }}-{{ rec.input.K }}</span>
            </div>
            <div class="input-item">
              <span class="input-label">pH:</span>
              <span class="input-value">{{ rec.input.pH_Value }}</span>
            </div>
            <div class="input-item">
              <span class="input-label">Temp:</span>
              <span class="input-value">{{ rec.input.Temperature }}°C</span>
            </div>
          </div>

          <details class="details-section">
            <summary class="details-toggle">
              <span>View All Parameters</span>
              <span class="toggle-icon">▼</span>
            </summary>
            
            <div class="parameters-grid">
              <div 
                v-for="(val, key) in rec.input" 
                :key="key"
                class="parameter-item"
              >
                <span class="param-key">{{ formatKey(key) }}</span>
                <span class="param-value">{{ val }} {{ getUnit(key) }}</span>
              </div>
            </div>
          </details>
        </div>

        <div class="card-actions">
          <button @click="copyToClipboard(rec)" class="action-btn">
            📋 Copy
          </button>
          <button @click="deleteRecord(index)" class="action-btn delete">
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HistoryPage',
  data() {
    return {
      records: [],
      selectedVariant: "",
      dateFrom: "",
      dateTo: "",

      variants: [
        "Siling Haba",
        "Django F1",
        "Siling Labuyo",
        "Lado F1",
        "Siling Bilog",
        "Siling Espada",
        "PM999 F1",
        "Siling Tingala",
        "Siling Amkis",
        "Siling Marusot"
      ]
    };
  },

  computed: {
    filteredRecords() {
      let filtered = this.records;

      if (this.selectedVariant) {
        filtered = filtered.filter(r => r.result === this.selectedVariant);
      }

      if (this.dateFrom) {
        const from = new Date(this.dateFrom);
        filtered = filtered.filter(rec => new Date(rec.time) >= from);
      }

      if (this.dateTo) {
        const to = new Date(this.dateTo);
        to.setHours(23, 59, 59, 999); // Include entire end date
        filtered = filtered.filter(rec => new Date(rec.time) <= to);
      }

      return filtered;
    },

    uniqueVariantsCount() {
      const variants = new Set(this.filteredRecords.map(rec => rec.result));
      return variants.size;
    }
  },

  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatKey(key) {
      const keyMap = {
        N: 'Nitrogen',
        P: 'Phosphorus',
        K: 'Potassium',
        pH_Value: 'pH Value',
        Moisture: 'Soil Moisture',
        Temperature: 'Temperature',
        Humidity: 'Humidity',
        Rainfall: 'Rainfall'
      };
      return keyMap[key] || key;
    },

    getUnit(key) {
      const units = {
        N: 'ppm',
        P: 'ppm',
        K: 'ppm',
        pH_Value: '',
        Moisture: '%',
        Temperature: '°C',
        Humidity: '%',
        Rainfall: 'mm'
      };
      return units[key] || '';
    },

    clearFilters() {
      this.selectedVariant = "";
      this.dateFrom = "";
      this.dateTo = "";
    },

    async copyToClipboard(record) {
      const text = `Chili Variant: ${record.result}\nDate: ${this.formatDate(record.time)}\n\nInput Parameters:\n${Object.entries(record.input).map(([key, value]) => `${this.formatKey(key)}: ${value} ${this.getUnit(key)}`).join('\n')}`;
      
      try {
        await navigator.clipboard.writeText(text);
        alert('Record copied to clipboard!');
      } catch (err) {
        console.error('Failed to copy: ', err);
      }
    },

    deleteRecord(index) {
      if (confirm('Are you sure you want to delete this record?')) {
        this.records.splice(index, 1);
        localStorage.setItem('history', JSON.stringify(this.records));
      }
    }
  },

  mounted() {
    let history = JSON.parse(localStorage.getItem("history") || "[]");
    this.records = history.sort((a, b) => new Date(b.time) - new Date(a.time));
  }
};
</script>

<style scoped>
/* ===== BASE STYLES ===== */
.history-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* ===== HEADER SECTION ===== */
.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 500;
}

/* ===== FILTERS SECTION ===== */
.filters-section {
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 200px;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.filter-dropdown,
.date-input {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  background: white;
  transition: all 0.2s ease;
  font-family: inherit;
}

.filter-dropdown:focus,
.date-input:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.date-filter-group {
  display: flex;
  gap: 15px;
  flex: 2;
}

.clear-filters-btn {
  padding: 12px 20px;
  background: #64748b;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.clear-filters-btn:hover {
  background: #475569;
  transform: translateY(-1px);
}

/* ===== STATS SECTION ===== */
.stats-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: #dc2626;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

/* ===== EMPTY STATE ===== */
.empty-state {
  background: white;
  padding: 60px 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #374151;
  margin-bottom: 10px;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 25px;
}

.cta-button {
  padding: 12px 24px;
  background: linear-gradient(135deg, #dc2626, #ea580c);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

/* ===== HISTORY GRID ===== */
.history-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 25px;
}

.history-card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.history-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* ===== CARD HEADER ===== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f1f5f9;
}

.variant-badge {
  display: flex;
  align-items: center;
  gap: 10px;
}

.variant-icon {
  font-size: 1.5rem;
}

.variant-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.timestamp {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
  text-align: right;
}

/* ===== CARD CONTENT ===== */
.card-content {
  margin-bottom: 20px;
}

.input-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.input-item {
  text-align: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 10px;
}

.input-label {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 4px;
}

.input-value {
  display: block;
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
}

/* ===== DETAILS SECTION ===== */
.details-section {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}

.details-toggle {
  padding: 15px 20px;
  background: #f8fafc;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #374151;
  transition: background 0.2s ease;
}

.details-toggle:hover {
  background: #f1f5f9;
}

.toggle-icon {
  transition: transform 0.3s ease;
}

.details-section[open] .toggle-icon {
  transform: rotate(180deg);
}

.parameters-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  background: white;
}

.parameter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
}

.parameter-item:last-child {
  border-bottom: none;
}

.param-key {
  font-weight: 600;
  color: #374151;
}

.param-value {
  color: #64748b;
  font-weight: 500;
}

/* ===== CARD ACTIONS ===== */
.card-actions {
  display: flex;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #f1f5f9;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #f8fafc;
  transform: translateY(-1px);
}

.action-btn.delete {
  color: #dc2626;
  border-color: #fecaca;
}

.action-btn.delete:hover {
  background: #fef2f2;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 1024px) {
  .history-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }
}

@media (max-width: 768px) {
  .history-container {
    padding: 20px 15px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .date-filter-group {
    flex-direction: column;
  }
  
  .history-grid {
    grid-template-columns: 1fr;
  }
  
  .input-summary {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .timestamp {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .input-summary {
    grid-template-columns: 1fr;
  }
  
  .stats-section {
    flex-direction: column;
  }
  
  .card-actions {
    flex-direction: column;
  }
}
</style>