<template>
  <div class="dashboard-wrapper bg-gradient">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state d-flex align-items-center justify-content-center">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading data...</span>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-main p-4">
      <h1 class="dashboard-header text-white mb-4">Serviceman Performance Overview</h1>

      <!-- Metric Summary Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-4">
          <div class="metric-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="metric-icon bg-info rounded-circle p-3 me-3">
                <i class="fas fa-clipboard-list text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Total Requests</h6>
                <h2 class="mb-0 text-black">{{ serviceRequests.length }}</h2>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="metric-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="metric-icon bg-success rounded-circle p-3 me-3">
                <i class="fas fa-hammer text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Active Requests</h6>
                <h2 class="mb-0 text-black">{{ getRequestsByStatus('active').length }}</h2>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="metric-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="metric-icon bg-warning rounded-circle p-3 me-3">
                <i class="fas fa-hourglass-half text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Pending Requests</h6>
                <h2 class="mb-0 text-black">{{ getRequestsByStatus('requested').length }}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Charts -->
      <div class="row g-4 mb-4">
        <div class="col-md-6">
          <div class="analytics-card bg-white rounded-3 p-3">
            <h5 class="analytics-title mb-3">Service Status Distribution</h5>
            <canvas ref="statusChartRef"></canvas>
          </div>
        </div>
        <div class="col-md-6">
          <div class="analytics-card bg-white rounded-3 p-3">
            <h5 class="analytics-title mb-3">Customer Rating Analysis</h5>
            <canvas ref="ratingChartRef"></canvas>
          </div>
        </div>
      </div>

      <!-- Service Request Categories -->
      <div class="service-categories bg-white rounded-3 p-3">
        <ul class="nav nav-pills mb-3" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#activeTab">
              Active
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="pill" data-bs-target="#requestedTab">
              Requested
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="pill" data-bs-target="#completedTab">
              Completed
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="pill" data-bs-target="#withdrawnTab">
              Withdrawn
            </button>
          </li>
        </ul>

        <div class="tab-content" id="serviceTabContent">
          <div v-for="status in ['active', 'requested', 'completed', 'withdrawn']" 
               :key="status"
               :class="['tab-pane fade', status == 'active' ? 'show active' : '']"
               :id="`${status.toLowerCase()}Tab`">
            <div class="row g-3">
              <div v-for="request in getRequestsByStatus(status)" 
                   :key="request.serviceRequest_id" 
                   class="col-md-6 col-lg-4">
                <div class="service-card h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <h6 class="card-title mb-0 text-black">Request #{{ request.serviceRequest_id }}</h6>
                      <span :class="getStatusBadgeClass(status)">
                        {{ status }}
                      </span>
                    </div>
                    <div class="service-info">
                      <p class="mb-2">
                        <i class="fas fa-user me-2"></i>
                        {{ request.customer_name }}
                      </p>
                      <p class="mb-2">
                        <i class="fas fa-wrench me-2"></i>
                        {{ request.service }}
                      </p>
                      <p class="mb-2">
                        <i class="fas fa-map-marker-alt me-2"></i>
                        {{ request.customer_address }}
                      </p>
                      <p class="mb-2">
                        <i class="fas fa-calendar me-2"></i>
                        {{ request.request_begin_date }}
                      </p>
                      <p class="mb-0" v-if="request.rating">
                        <i class="fas fa-star me-2"></i>
                        Rating: {{ request.rating }}/10
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'ServicemanDashboard',
  
  setup() {
    const serviceRequests = ref([]);
    const loading = ref(true);
    const statusChartRef = ref(null);
    const ratingChartRef = ref(null);
    let statusChart = null;
    let ratingChart = null;

    const fetchServiceData = async () => {
      try {
        const servicemanId = localStorage.getItem('service_id');
        const token = localStorage.getItem('service_Token');
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/listServices/${servicemanId}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': token,
            },
          }
        );
        serviceRequests.value = response.data;
        // Initialize charts after data is loaded
      } catch (error) {
        console.error('Error fetching service data:', error);
      } finally {
        loading.value = false;
      }
    };

    const getRequestsByStatus = (status) => {
      return serviceRequests.value.filter(request => 
        request.status.toLowerCase() === status.toLowerCase()
      );
    };

    const getStatusBadgeClass = (status) => {
      const badgeClasses = {
        active: 'badge bg-success',
        requested: 'badge bg-warning text-dark',
        completed: 'badge bg-info',
        withdrawn: 'badge bg-danger'
      };
      return badgeClasses[status] || 'badge bg-secondary';
    };

    const createStatusDistribution = () => {
      if (!statusChartRef.value) return;
      
      if (statusChart) {
        statusChart.destroy();
      }

      const ctx = statusChartRef.value.getContext('2d');
      if (!ctx) return;

      const statusData = {
        'Active': getRequestsByStatus('active').length,
        'Requested': getRequestsByStatus('requested').length,
        'Completed': getRequestsByStatus('completed').length,
        'Withdrawn': getRequestsByStatus('withdrawn').length
      };

      statusChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: Object.keys(statusData),
          datasets: [{
            data: Object.values(statusData),
            backgroundColor: [
              '#198754',
              '#ffc107',
              '#0dcaf0',
              '#dc3545'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });
    };

    const createRatingAnalysis = () => {
      if (!ratingChartRef.value) return;
      
      if (ratingChart) {
        ratingChart.destroy();
      }

      const ctx = ratingChartRef.value.getContext('2d');
      if (!ctx) return;

      const ratings = Array(10).fill(0);
      serviceRequests.value.forEach(request => {
        if (request.rating) {
          ratings[request.rating - 1]++;
        }
      });

      ratingChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Array.from({ length: 10 }, (_, i) => i + 1),
          datasets: [{
            label: 'Number of Ratings',
            data: ratings,
            backgroundColor: '#0d6efd'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      });
    };

    const initializeCharts = () => {
      createStatusDistribution();
      createRatingAnalysis();
    };

    onMounted(() => {
      fetchServiceData().then(() => 
    {
      initializeCharts();
    });
    });

    return {
      serviceRequests,
      loading,
      statusChartRef,
      ratingChartRef,
      getRequestsByStatus,
      getStatusBadgeClass,
    };
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
}

.dashboard-main {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.loading-state {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.metric-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
}

.metric-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.analytics-card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.analytics-title {
  color: #1e40af;
  font-weight: 600;
}

.service-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.service-card:hover {
  transform: translateY(-4px);
}

.service-info p {
  color: #4b5563;
  font-size: 0.875rem;
}

.service-info i {
  color: #1e40af;
  width: 20px;
}

.nav-pills .nav-link {
  color: #1e40af;
  font-weight: 500;
  margin-right: 0.5rem;
}

.nav-pills .nav-link.active {
  background-color: #1e40af;
  color: white;
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 1rem;
  }
  
  .nav-pills {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .nav-link {
    white-space: nowrap;
  }
}

@media print {
  .dashboard-wrapper {
    background: none;
  }
  
  .metric-card,
  .analytics-card,
  .service-card {
    box-shadow: none;
    border: 1px solid #e5e7eb;
  }
  
  .nav-pills .nav-link {
    border: 1px solid #e5e7eb;
  }
}
</style>