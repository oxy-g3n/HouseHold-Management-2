<template>
  <div class="dashboard-container bg-gradient">
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay d-flex align-items-center justify-content-center">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Loading dashboard...</span>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="dashboard-content p-4">
      <h1 class="dashboard-title text-white mb-4">Service Request Overview</h1>
      
      <!-- Summary Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-4">
          <div class="summary-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="summary-icon bg-primary rounded-circle p-3 me-3">
                <i class="fas fa-tasks text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Total Requests</h6>
                <h2 class="mb-0">{{ requests.length }}</h2>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="summary-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="summary-icon bg-success rounded-circle p-3 me-3">
                <i class="fas fa-play-circle text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Active Requests</h6>
                <h2 class="mb-0">{{ getRequestsByStatus('active').length }}</h2>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="summary-card bg-white rounded-3 p-3 h-100">
            <div class="d-flex align-items-center">
              <div class="summary-icon bg-warning rounded-circle p-3 me-3">
                <i class="fas fa-clock text-white"></i>
              </div>
              <div>
                <h6 class="text-muted mb-1">Pending Requests</h6>
                <h2 class="mb-0">{{ getRequestsByStatus('requested').length }}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Section -->
      <div class="analytics-section row g-4 mb-4">
        <div class="col-md-6">
          <div class="chart-card bg-white rounded-3 p-3">
            <h5 class="chart-title mb-3">Request Distribution</h5>
            <canvas ref="statusChartRef"></canvas>
          </div>
        </div>
        <div class="col-md-6">
          <div class="chart-card bg-white rounded-3 p-3">
            <h5 class="chart-title mb-3">Service Categories</h5>
            <canvas ref="servicesChartRef"></canvas>
          </div>
        </div>
      </div>

      <!-- Request Tabs -->
      <div class="request-tabs-container bg-white rounded-3 p-3">
        <ul class="nav nav-pills mb-3" id="requestTabs" role="tablist">
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
          <li class="nav-item" role="presentation">
            <button class="nav-link" data-bs-toggle="pill" data-bs-target="#rejectedTab">
              Rejected
            </button>
          </li>
        </ul>

        <div class="tab-content" id="requestTabsContent">
          <div v-for="status in ['active', 'requested', 'completed', 'withdrawn', 'rejected']" 
               :key="status"
               :class="['tab-pane fade', status === 'active' ? 'show active' : '']"
               :id="`${status}Tab`">
            <div class="row g-3">
              <div v-for="request in getRequestsByStatus(status)" 
                   :key="request.serviceRequest_id" 
                   class="col-md-6 col-lg-4">
                <div class="request-card h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <h6 class="card-title mb-0">#{{ request.serviceRequest_id }}</h6>
                      <span :class="getStatusBadgeClass(status)">
                        {{ status.charAt(0).toUpperCase() + status.slice(1) }}
                      </span>
                    </div>
                    <div class="request-details">
                      <p class="mb-2">
                        <i class="fas fa-user-tie me-2"></i>
                        {{ request.serviceman_name }}
                      </p>
                      <p class="mb-2">
                        <i class="fas fa-tools me-2"></i>
                        {{ request.service }}
                      </p>
                      <p class="mb-2">
                        <i class="fas fa-calendar-alt me-2"></i>
                        {{ formatDate(request.request_begin_date) }}
                      </p>
                      <p class="mb-0" v-if="request.rating !== null">
                        <i class="fas fa-star me-2"></i>
                        {{ request.rating }}/10
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

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  name: 'ServiceDashboard',
  
  setup() {
    const requests = ref([]);
    const loading = ref(true);
    const statusChartRef = ref(null);
    const servicesChartRef = ref(null);
    let statusChart = null;
    let servicesChart = null;

    const fetchRequests = async () => {
      try {
        const customerId = localStorage.getItem('cust_id');
        const token = localStorage.getItem('cust_Token');
        const response = await axios.get(
          `http://127.0.0.1:5000/provision_requests/get_consumer_requests/${customerId}`,
          {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': token,
            },
          }
        );
        requests.value = response.data;
        initializeCharts();
      } catch (error) {
        console.error('Failed to fetch requests:', error);
      } finally {
        loading.value = false;
      }
    };

    const getRequestsByStatus = (status) => {
      return requests.value.filter(request => request.status.toLowerCase() === status.toLowerCase());
    };

    const getStatusBadgeClass = (status) => {
      const classes = {
        active: 'badge bg-success',
        requested: 'badge bg-warning text-dark',
        completed: 'badge bg-primary',
        withdrawn: 'badge bg-secondary',
        rejected: 'badge bg-danger'
      };
      return classes[status] || 'badge bg-secondary';
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return new Date(dateString).toLocaleDateString('en-US', options);
    };

    const initializeCharts = () => {
      createStatusChart();
      createServicesChart();
    };

    const createStatusChart = () => {
      if (statusChart) {
        statusChart.destroy();
      }

      const statusCounts = {
        Active: getRequestsByStatus('active').length,
        Requested: getRequestsByStatus('requested').length,
        Completed: getRequestsByStatus('completed').length,
        Withdrawn: getRequestsByStatus('withdrawn').length,
        Rejected: getRequestsByStatus('rejected').length
      };

      statusChart = new Chart(statusChartRef.value, {
        type: 'doughnut',
        data: {
          labels: Object.keys(statusCounts),
          datasets: [{
            data: Object.values(statusCounts),
            backgroundColor: [
              '#198754', // success
              '#ffc107', // warning
              '#0d6efd', // primary
              '#6c757d', // secondary
              '#dc3545'  // danger
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

    const createServicesChart = () => {
      if (servicesChart) {
        servicesChart.destroy();
      }

      const serviceCount = {};
      requests.value.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });

      servicesChart = new Chart(servicesChartRef.value, {
        type: 'bar',
        data: {
          labels: Object.keys(serviceCount),
          datasets: [{
            label: 'Number of Requests',
            data: Object.values(serviceCount),
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

    onMounted(() => {
      fetchRequests().then(() => 
    {
      initializeCharts();
    });
    });

    return {
      requests,
      loading,
      statusChartRef,
      servicesChartRef,
      getRequestsByStatus,
      getStatusBadgeClass,
      formatDate
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: #1e40af;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-title {
  color: #000000;
  font-weight: 600;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.summary-card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: transform 0.2s;
  background-color: #ffffff;
}

.summary-card h6 {
  color: #000000;
  font-weight: 500;
}

.summary-card h2 {
  color: #000000;
  font-weight: 600;
}

.summary-card:hover {
  transform: translateY(-5px);
}

.summary-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  height: 100%;
  background-color: #ffffff;
}

.chart-title {
  color: #000000;
  font-weight: 600;
}

.request-card {
  background-color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  transition: transform 0.2s;
}

.request-card:hover {
  transform: translateY(-5px);
}

.request-card .card-title {
  color: #000000;
  font-weight: 600;
}

.nav-pills .nav-link {
  color: #000000;
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  font-weight: 500;
}

.nav-pills .nav-link.active {
  background-color: #1a237e;
  color: #ffffff;
}

.request-details p {
  color: #000000;
  font-size: 0.875rem;
  font-weight: 400;
}

.request-details i {
  width: 20px;
  text-align: center;
  color: #1a237e;
}

.request-tabs-container {
  background-color: #ffffff;
}

.card-body {
  background-color: #ffffff;
}

.badge {
  font-weight: 500;
}

/* Status badge overrides for better contrast */
.badge.bg-warning {
  color: #000000 !important;
}

.badge.bg-secondary {
  color: #ffffff !important;
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }
  
  .nav-pills {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .nav-pills .nav-link {
    white-space: nowrap;
  }
  
  .chart-card {
    margin-bottom: 1rem;
  }
}

/* Print styles for better readability */
@media print {
  .dashboard-container {
    background: none;
  }
  
  .dashboard-content {
    padding: 0;
  }
  
  .request-card,
  .summary-card,
  .chart-card {
    box-shadow: none;
    border: 1px solid #000000;
  }
  
  .nav-pills .nav-link {
    color: #000000;
    border: 1px solid #000000;
  }
}
</style>