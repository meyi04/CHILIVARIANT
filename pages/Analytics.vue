<template>
  <div class="analytics-container">
    <!-- HEADER SECTION -->
    <div class="header-section">
      <h1 class="title">📊 Analytics Dashboard</h1>
      <p class="subtitle">Comprehensive insights into your chili variant predictions</p>
    </div>

    <!-- FILTERS SECTION -->
    <div class="filters-section">
      <div class="filter-group">
        <label class="filter-label">Filter by Variant</label>
        <select v-model="selectedVariant" class="filter-dropdown">
          <option value="">All Variants</option>
          <option v-for="v in variants" :key="v" :value="v">{{ v }}</option>
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

    <!-- STATISTICS CARDS -->
    <div class="stats-grid">
      <div class="stat-card primary">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <div class="stat-number">{{ filteredRecords.length }}</div>
          <div class="stat-label">Total Predictions</div>
        </div>
      </div>

      <div class="stat-card success">
        <div class="stat-icon">🏆</div>
        <div class="stat-content">
          <div class="stat-number">{{ mostFrequent || '—' }}</div>
          <div class="stat-label">Most Recommended</div>
        </div>
      </div>

      <div class="stat-card info">
        <div class="stat-icon">📅</div>
        <div class="stat-content">
          <div class="stat-number">{{ firstPrediction || '—' }}</div>
          <div class="stat-label">First Prediction</div>
        </div>
      </div>

      <div class="stat-card warning">
        <div class="stat-icon">🕒</div>
        <div class="stat-content">
          <div class="stat-number">{{ latestPrediction || '—' }}</div>
          <div class="stat-label">Latest Prediction</div>
        </div>
      </div>
    </div>

    <!-- CHARTS SECTION -->
    <div class="charts-section">
      <!-- PIE CHART -->
      <div class="chart-container">
        <div class="chart-header">
          <h3>Variant Distribution</h3>
          <div class="chart-subtitle">Breakdown of recommended chili variants</div>
        </div>
        <div class="chart-wrapper">
          <Pie :data="pieData" :options="pieOptions" />
        </div>
      </div>

      <!-- BAR CHART -->
      <div class="chart-container">
        <div class="chart-header">
          <h3>Variant Comparison</h3>
          <div class="chart-subtitle">Count of predictions per variant</div>
        </div>
        <div class="chart-wrapper">
          <Bar :data="barData" :options="barOptions" />
        </div>
      </div>

      <!-- LINE CHART -->
      <div class="chart-container full-width">
        <div class="chart-header">
          <h3>Predictions Timeline</h3>
          <div class="chart-subtitle">Prediction activity over time</div>
        </div>
        <div class="chart-wrapper">
          <Line :data="lineData" :options="lineOptions" />
        </div>
      </div>
    </div>

    <!-- EMPTY STATE -->
    <div v-if="filteredRecords.length === 0" class="empty-state">
      <div class="empty-icon">📊</div>
      <h3>No Analytics Data</h3>
      <p>No prediction records found for the selected filters.</p>
      <button @click="clearFilters" class="cta-button">
        View All Data
      </button>
    </div>
  </div>
</template>

<script>
import { Pie, Bar, Line } from "vue-chartjs";
import {
  Chart,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title
} from "chart.js";

Chart.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title
);

export default {
  name: 'AnalyticsPage',
  components: {
    Pie,
    Bar,
    Line
  },

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
        "Siling Marusot",
      ],
    };
  },

  computed: {
    filteredRecords() {
      let list = this.records;

      if (this.selectedVariant) {
        list = list.filter((r) => r.result === this.selectedVariant);
      }

      if (this.dateFrom) {
        const from = new Date(this.dateFrom);
        list = list.filter((r) => new Date(r.time) >= from);
      }

      if (this.dateTo) {
        const to = new Date(this.dateTo);
        to.setHours(23, 59, 59, 999);
        list = list.filter((r) => new Date(r.time) <= to);
      }

      return list;
    },

    mostFrequent() {
      if (!this.filteredRecords.length) return null;

      const count = {};
      this.filteredRecords.forEach((r) => {
        count[r.result] = (count[r.result] || 0) + 1;
      });

      return Object.keys(count).reduce((a, b) =>
        count[a] > count[b] ? a : b
      );
    },

    firstPrediction() {
      if (!this.filteredRecords.length) return null;
      const sorted = [...this.filteredRecords].sort((a, b) => new Date(a.time) - new Date(b.time));
      return new Date(sorted[0].time).toLocaleDateString();
    },

    latestPrediction() {
      if (!this.filteredRecords.length) return null;
      const sorted = [...this.filteredRecords].sort((a, b) => new Date(b.time) - new Date(a.time));
      return new Date(sorted[0].time).toLocaleDateString();
    },

    // Chart Data and Options
    pieData() {
      const counts = this.countVariants();
      return {
        labels: Object.keys(counts),
        datasets: [
          {
            data: Object.values(counts),
            backgroundColor: [
              "#ff6b6b", "#4dabf7", "#51cf66", "#ffa94d", "#845ef7",
              "#f06595", "#ffd43b", "#63e6be", "#ff922b", "#339af0",
              "#20c997", "#e64980"
            ],
            borderColor: '#ffffff',
            borderWidth: 2
          }
        ]
      };
    },

    pieOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              font: {
                family: 'Inter',
                size: 12
              },
              padding: 20
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: { family: 'Inter' },
            bodyFont: { family: 'Inter' }
          }
        }
      };
    },

    barData() {
      const counts = this.countVariants();
      return {
        labels: Object.keys(counts),
        datasets: [
          {
            label: "Prediction Count",
            data: Object.values(counts),
            backgroundColor: "#4dabf7",
            borderColor: "#339af0",
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      };
    },

    barOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: { family: 'Inter' },
            bodyFont: { family: 'Inter' }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              font: { family: 'Inter' }
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: { family: 'Inter' }
            }
          }
        }
      };
    },

    lineData() {
      const grouped = {};
      const sortedRecords = [...this.filteredRecords].sort((a, b) => new Date(a.time) - new Date(b.time));
      
      sortedRecords.forEach((rec) => {
        const day = new Date(rec.time).toLocaleDateString();
        grouped[day] = (grouped[day] || 0) + 1;
      });

      return {
        labels: Object.keys(grouped),
        datasets: [
          {
            label: "Predictions",
            data: Object.values(grouped),
            borderColor: "#ff6b6b",
            backgroundColor: "rgba(255, 107, 107, 0.1)",
            tension: 0.4,
            fill: true,
            pointBackgroundColor: "#ff6b6b",
            pointBorderColor: "#ffffff",
            pointBorderWidth: 2
          }
        ]
      };
    },

    lineOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleFont: { family: 'Inter' },
            bodyFont: { family: 'Inter' }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              font: { family: 'Inter' }
            }
          },
          x: {
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            ticks: {
              font: { family: 'Inter' }
            }
          }
        }
      };
    }
  },

  methods: {
    countVariants() {
      const count = {};
      this.filteredRecords.forEach((r) => {
        count[r.result] = (count[r.result] || 0) + 1;
      });
      return count;
    },

    clearFilters() {
      this.selectedVariant = "";
      this.dateFrom = "";
      this.dateTo = "";
    }
  },

  mounted() {
    this.records = JSON.parse(localStorage.getItem("history") || "[]");
  }
};
</script>

<style scoped>
/* ===== BASE STYLES ===== */
.analytics-container {
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

/* ===== STATS GRID ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.stat-card.primary {
  border-left: 4px solid #dc2626;
}

.stat-card.success {
  border-left: 4px solid #059669;
}

.stat-card.info {
  border-left: 4px solid #2563eb;
}

.stat-card.warning {
  border-left: 4px solid #d97706;
}

.stat-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 5px;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 600;
}

/* ===== CHARTS SECTION ===== */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.chart-container {
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.chart-container.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 5px;
}

.chart-subtitle {
  font-size: 0.9rem;
  color: #64748b;
}

.chart-wrapper {
  height: 300px;
  position: relative;
}

.chart-container.full-width .chart-wrapper {
  height: 350px;
}

/* ===== EMPTY STATE ===== */
.empty-state {
  background: white;
  padding: 60px 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  grid-column: 1 / -1;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
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

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 1024px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .analytics-container {
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
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .chart-container {
    padding: 20px;
  }
  
  .chart-wrapper {
    height: 250px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.8rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .chart-wrapper {
    height: 200px;
  }
}
</style>