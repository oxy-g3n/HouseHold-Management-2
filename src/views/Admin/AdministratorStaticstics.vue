<template>
  <div class="dashboard-wrapper">
    <header class="dashboard-header">
      <h1>Service Management Dashboard</h1>
      <div v-if="loading" class="loading-indicator">
        <div class="loading-spinner"></div>
        <span>Refreshing dashboard data...</span>
      </div>
    </header>

    <div v-if="!loading" class="dashboard-content">
      <!-- KPI Cards -->
      <div class="kpi-container">
        <div class="kpi-card primary">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div class="kpi-details">
            <h3>Total Requests</h3>
            <p>{{ requests.length }}</p>
          </div>
        </div>

        <div class="kpi-card success">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="kpi-details">
            <h3>Completed</h3>
            <p>{{ requests.filter(r => r.status === 'completed').length }}</p>
          </div>
        </div>

        <div class="kpi-card warning">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="kpi-details">
            <h3>Active Requests</h3>
            <p>{{ requests.filter(r => r.status === 'active').length }}</p>
          </div>
        </div>

        <div class="kpi-card info">
          <div class="kpi-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div class="kpi-details">
            <h3>Total Users</h3>
            <p>{{ servicemen.length + customers.length }}</p>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-grid">
        <div class="chart-card">
          <h2>Service Distribution</h2>
          <canvas ref="servicesChartRef"></canvas>
        </div>
        <div class="chart-card">
          <h2>User Growth Timeline</h2>
          <canvas ref="userCreationChartRef"></canvas>
        </div>
      </div>

      <!-- Requests List -->
      <div class="requests-section">
        <div class="requests-header">
          <h2>Service Requests</h2>
          <div class="filter-controls">
            <button 
              v-for="status in ['all', 'active', 'completed']" 
              :key="status"
              @click="filterStatus = status"
              :class="['filter-btn', { active: filterStatus == status }]"
            >
              {{ status.charAt(0).toUpperCase() + status.slice(1) }}
            </button>
          </div>
        </div>

        <div class="requests-grid">
          <div 
            v-for="request in filteredRequests" 
            :key="request.serviceRequest_id"
            class="request-card"
          >
            <div class="request-header">
              <span class="request-id">#{{ request.serviceRequest_id }}</span>
              <span :class="['status-pill', request.status]">{{ request.status }}</span>
            </div>
            
            <div class="request-content">
              <div class="service-type">
                <span class="label">Service:</span>
                <span class="value">{{ request.service }}</span>
              </div>
              
              <div class="customer-info">
                <span class="label">Customer:</span>
                <span class="value">{{ request.customer_name }}</span>
              </div>
              
              <div class="provider-info">
                <span class="label">Provider:</span>
                <span class="value">{{ request.serviceman_name }}</span>
              </div>
              
              <div class="rating-info">
                <span class="label">Rating:</span>
                <span class="value">
                  <template v-if="request.rating !== null">
                    <span class="stars">
                      {{ '★'.repeat(Math.ceil(request.rating/2)) }}{{ '☆'.repeat(5-(Math.ceil(request.rating/2))) }}
                    </span>
                    <span class="rating-number">({{ request.rating }}/10)</span>
                  </template>
                  <span v-else>Not rated</span>
                </span>
              </div>

              <div class="status">
                <span class="label">Status:</span>
                <span class="value">{{ request.status }}</span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios';
import { Colors } from 'chart.js';
import Chart from 'chart.js/auto';
import { ref, onMounted, nextTick, computed } from 'vue';


export default {
  setup() {
    const requests = ref([]);
    const servicemen = ref([]);
    const customers = ref([]);
    const loading = ref(true);
    const sortKey = ref('');
    const sortAsc = ref(true);
    const servicesChartRef = ref(null);
    const userCreationChartRef = ref(null);
    const filterStatus = ref('all');
    

    const sortedRequests = computed(() => {
      return requests.value.slice().sort((a, b) => {
        const modifier = sortAsc.value ? 1 : -1;
        if (a[sortKey.value] < b[sortKey.value]) return -1 * modifier;
        if (a[sortKey.value] > b[sortKey.value]) return 1 * modifier;
        return 0;
      });
    });


const filteredRequests = computed(() => {
  if (filterStatus.value === 'all') return sortedRequests.value;
  return sortedRequests.value.filter(request => request.status === filterStatus.value);
});

    const fetchAllData = async () => {
      loading.value = true;
      try {
        await Promise.all([
          fetchAllRequests(),
          fetchServicemen(),
          fetchCustomers(),
        ]);
        await nextTick();
        createCharts();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please try again.");
      } finally {
        loading.value = false;
      }
    };

    const fetchAllRequests = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/requests/listAllServices",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      requests.value = response.data;
    };

    const fetchServicemen = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/getProviders",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      servicemen.value = response.data;
    };

    const fetchCustomers = async () => {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/getConsumers",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      customers.value = response.data;
    };

    const createCharts = () => {
      createServicesChart();
      createUserCreationChart();
    };

    const createServicesChart = () => {
      if (!servicesChartRef.value) return;

      const ctx = servicesChartRef.value.getContext('2d');
      const serviceCount = {};
      requests.value.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });
      
      new Chart(ctx, {
        type: 'pie',
    data: {
      labels: Object.keys(serviceCount),
      datasets: [{
        data: Object.values(serviceCount),
        backgroundColor: [
          'rgba(100, 181, 246, 0.8)',
          'rgba(144, 202, 249, 0.8)',
          'rgba(187, 222, 251, 0.8)',
          'rgba(79, 195, 247, 0.8)',
          'rgba(129, 212, 250, 0.8)',
        ],
        borderColor: 'white',
        borderWidth: 2
      }]
  },
  options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#2c3e50',
            padding: 20,
            font: {
              size: 14
            }
          }
        }
      }
    }
});

    };

    const createUserCreationChart = () => {
  if (!userCreationChartRef.value) return;

  const ctx = userCreationChartRef.value.getContext('2d');
  const customerData = processUserCreationData(customers.value);
  const servicemanData = processUserCreationData(servicemen.value);
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: generateDateLabels(),
      datasets: [
        {
          label: 'Customers',
          data: customerData,
          borderColor: 'rgba(75, 192, 192, 1)',
          fill: false
        },
        {
          label: 'Servicemen',
          data: servicemanData,
          borderColor: 'rgba(255, 99, 132, 1)',
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Users',
            color: 'white' // Y-axis title color
          },
          ticks: {
            color: 'white' // Y-axis label color
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date',
            color: 'white' // X-axis title color
          },
          ticks: {
            color: 'white' // X-axis label color
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: 'white' // Legend text color
          }
        }
      }
    }
  });
};
    const processUserCreationData = (users) => {
      const dateCounts = {};
      users.forEach(user => {
        const date = new Date(user.date_created).toISOString().split('T')[0];
        dateCounts[date] = (dateCounts[date] || 0) + 1;
      });
      return generateDateLabels().map(date => dateCounts[date] || 0);
    };

    const generateDateLabels = () => {
      const allUsers = [...customers.value, ...servicemen.value];
      const startDate = new Date(Math.min(...allUsers.map(u => new Date(u.date_created))));
      const endDate = new Date();
      const dateLabels = [];
      for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        dateLabels.push(d.toISOString().split('T')[0]);
      }
      return dateLabels;
    };

    onMounted(() => {
      fetchAllData();
    });

    return {
      requests,
      servicemen,
      customers,
      loading,
      sortKey,
      sortAsc,
      servicesChartRef,
      userCreationChartRef,
      fetchAllData,
      createCharts,
      filterStatus,           // Added this
      filteredRequests,       // Added this
    };
  },
  computed: {
    sortedRequests() {
      return this.requests.slice().sort((a, b) => {
        const modifier = this.sortAsc ? 1 : -1;
        if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
        if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
        return 0;
      });
    },
    totalRequests() {
      return this.requests.length;
    },
    completedRequests() {
      return this.requests.filter(r => r.status === 'completed').length;
    },
    activeRequests() {
      return this.requests.filter(r => r.status === 'active').length;
    },
    totalUsers() {
      return this.servicemen.length + this.customers.length;
    },
    totalServicemen() {
      return this.servicemen.length;
    },
    totalCustomers() {
      return this.customers.length;
    },
  },
  methods: {
    async fetchAllData() {
      this.loading = true;
      try {
        await Promise.all([
          this.fetchAllRequests(),
          this.fetchServicemen(),
          this.fetchCustomers(),
        ]);
        this.createCharts();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to fetch data. Please try again.");
      } finally {
        this.loading = false;
      }
    },
    async fetchAllRequests() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/requests/listAllServices",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.requests = response.data;
    },
    async fetchServicemen() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/getProviders",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.servicemen = response.data;
    },
    async fetchCustomers() {
      const token = localStorage.getItem("admin_Token");
      const response = await axios.get(
        "http://127.0.0.1:5000/users/getConsumers",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `${token}`,
          },
        }
      );
      this.customers = response.data;
    },
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },
    getSortClass(key) {
      if (this.sortKey === key) {
        return this.sortAsc ? 'asc' : 'desc';
      }
      return '';
    },
    createCharts() {
      this.createServicesChart();
      this.createUserCreationChart();
    },
    createServicesChart() {
      const ctx = this.$refs.servicesChart.getContext('2d');
      const serviceCount = {};
      this.requests.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });
      
      this.servicesChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: Object.keys(serviceCount),
    datasets: [{
      label: 'Number of Requests',
      data: Object.values(serviceCount),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Number of Requests',
          color: 'white' // Y-axis title color
        },
        ticks: {
          color: 'white' // Y-axis label color
        }
      },
      x: {
        title: {
          display: true,
          text: 'Service Type',
          color: 'white' // X-axis title color
        },
        ticks: {
          color: 'white' // X-axis label color
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          color: 'white' // Legend text color
        }
      }
    }
  }
});
    },
    createUserCreationChart() {
      const ctx = this.$refs.userCreationChart.getContext('2d');
      const customerData = this.processUserCreationData(this.customers);
      const servicemanData = this.processUserCreationData(this.servicemen);
      
      this.userCreationChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.generateDateLabels(),
          datasets: [
            {
              label: 'Customers',
              data: customerData,
              borderColor: 'rgba(75, 192, 192, 1)',
              fill: false
            },
            {
              label: 'Servicemen',
              data: servicemanData,
              borderColor: 'rgba(255, 99, 132, 1)',
              fill: false
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Users'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      });
    },
    processUserCreationData(users) {
      const dateCounts = {};
      users.forEach(user => {
        const date = new Date(user.date_created).toISOString().split('T')[0];
        dateCounts[date] = (dateCounts[date] || 0) + 1;
      });
      return this.generateDateLabels().map(date => dateCounts[date] || 0);
    },
    generateDateLabels() {
      const startDate = new Date(Math.min(...this.customers.concat(this.servicemen).map(u => new Date(u.date_created))));
      const endDate = new Date();
      const dateLabels = [];
      for (let d = startDate; d <= endDate; d.setDate(d.getDate() + 1)) {
        dateLabels.push(d.toISOString().split('T')[0]);
      }
      return dateLabels;
    }
  },
  created() {
    this.fetchAllData();
  },
};
</script>

<style scoped>
.dashboard-wrapper {
  background-color: #f8fafc;
  min-height: 100vh;
  padding: 2rem;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  color: #1e40af;
  font-size: 2rem;
  font-weight: 600;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #64748b;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #93c5fd;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.kpi-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.1);
}

.kpi-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.kpi-icon .icon {
  width: 24px;
  height: 24px;
}

.kpi-card.primary .kpi-icon { 
  background: #e0f2fe;
  color: #0284c7;
}

.kpi-card.success .kpi-icon {
  background: #dcfce7;
  color: #16a34a;
}

.kpi-card.warning .kpi-icon {
  background: #fef3c7;
  color: #d97706;
}

.kpi-card.info .kpi-icon {
  background: #dbeafe;
  color: #2563eb;
}

.kpi-details h3 {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.kpi-details p {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.chart-card h2 {
  color: #1e40af;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.requests-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.requests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.requests-header h2 {
  color: #1e40af;
  font-size: 1.25rem;
}

.filter-controls {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn.active {
  background: #1e40af;
  color: white;
  border-color: #1e40af;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.request-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.request-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.request-id {
  font-weight: 600;
  color: #1e40af;
}

.status-pill {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-pill.completed {
  background: #dcfce7;
  color: #16a34a;
}

.status-pill.active {
  background: #dbeafe;
  color: #2563eb;
}

.request-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.request-content > div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #64748b;
  font-size: 0.875rem;
}

.value {
  color: #1e293b;
  font-weight: 500;
}

.stars {
  color: #f59e0b;
  letter-spacing: 0.1em;
}

.rating-number {
  color: #64748b;
  margin-left: 0.5rem;
  font-size: 0.875rem;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 1rem;
  }

  .kpi-container {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .requests-grid {
    grid-template-columns: 1fr;
  }

  .requests-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .kpi-card {
    padding: 1rem;
  }

  .kpi-icon {
    width: 40px;
    height: 40px;
  }

  .kpi-icon .icon {
    width: 20px;
    height: 20px;
  }

  .kpi-details h3 {
    font-size: 0.75rem;
  }

  .kpi-details p {
    font-size: 1.25rem;
  }
}
</style>