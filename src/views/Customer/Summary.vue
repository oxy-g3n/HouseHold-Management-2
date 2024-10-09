<template>
  <div class="customer-summary-container">
    <h2>Service Request Summary</h2>
    <div v-if="loading" class="loading" aria-live="polite">Loading summary...</div>
    <div v-else-if="requests.length === 0" class="no-requests" aria-live="polite">No service requests found.</div>
    <div v-else>
      <!-- Charts -->
      <div class="charts-container">
        <div class="chart">
          <h3>Request Status</h3>
          <canvas ref="statusChartRef" class="small-chart"></canvas>
        </div>
        <div class="chart">
          <h3>Most Requested Services</h3>
          <canvas ref="servicesChartRef"></canvas>
        </div>
      </div>

      <!-- Requests Table -->
      <div class="table-container">
        <table class="requests-table">
          <thead>
            <tr>
              <th @click="sortTable('serviceRequest_id')" scope="col">Request ID <span :class="getSortClass('serviceRequest_id')"></span></th>
              <th @click="sortTable('serviceman_name')" scope="col">Serviceman Name <span :class="getSortClass('serviceman_name')"></span></th>
              <th @click="sortTable('serviceman_id')" scope="col">Serviceman ID <span :class="getSortClass('serviceman_id')"></span></th>
              <th @click="sortTable('service')" scope="col">Service <span :class="getSortClass('service')"></span></th>
              <th @click="sortTable('status')" scope="col">Status <span :class="getSortClass('status')"></span></th>
              <th @click="sortTable('rating')" scope="col">Rating <span :class="getSortClass('rating')"></span></th>
              <th @click="sortTable('request_begin_date')" scope="col">Start Date <span :class="getSortClass('request_begin_date')"></span></th>
              <th @click="sortTable('request_end_date')" scope="col">End Date <span :class="getSortClass('request_end_date')"></span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in sortedRequests" :key="request.serviceRequest_id">
              <td>{{ request.serviceRequest_id }}</td>
              <td>{{ request.serviceman_name }}</td>
              <td>{{ request.serviceman_id }}</td>
              <td>{{ request.service }}</td>
              <td>{{ request.status }}</td>
              <td>{{ request.rating !== null ? request.rating : 'N/A' }}</td>
              <td>{{ request.request_begin_date }}</td>
              <td>{{ request.request_end_date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, computed } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const requests = ref([]);
    const loading = ref(true);
    const sortKey = ref('');
    const sortAsc = ref(true);
    const statusChartRef = ref(null);
    const servicesChartRef = ref(null);
    let statusChart = null;
    let servicesChart = null;

    const sortedRequests = computed(() => {
      return [...requests.value].sort((a, b) => {
        const modifier = sortAsc.value ? 1 : -1;
        if (sortKey.value === 'request_begin_date' || sortKey.value === 'request_end_date') {
          return new Date(a[sortKey.value]) - new Date(b[sortKey.value]) * modifier;
        }
        if (a[sortKey.value] < b[sortKey.value]) return -1 * modifier;
        if (a[sortKey.value] > b[sortKey.value]) return 1 * modifier;
        return 0;
      });
    });

    const fetchAllRequests = async () => {
      loading.value = true;
      try {
        const customerId = localStorage.getItem("cust_id");
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/listMyServices/${customerId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        requests.value = response.data;
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        loading.value = false;
      }
    };

    const sortTable = (key) => {
      if (sortKey.value === key) {
        sortAsc.value = !sortAsc.value;
      } else {
        sortKey.value = key;
        sortAsc.value = true;
      }
    };

    const getSortClass = (key) => {
      if (sortKey.value === key) {
        return sortAsc.value ? 'asc' : 'desc';
      }
      return '';
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    };

    const createCharts = () => {
      createStatusChart();
      createServicesChart();
    };

    const createStatusChart = () => {
      if (statusChart) {
        statusChart.destroy();
      }
      const ctx = statusChartRef.value.getContext('2d');
      const statusCount = {};
      requests.value.forEach(request => {
        statusCount[request.status] = (statusCount[request.status] || 0) + 1;
      });
      
      statusChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: Object.keys(statusCount),
          datasets: [{
            data: Object.values(statusCount),
            backgroundColor: [
              'rgba(75, 192, 192, 0.6)',
              'rgba(255, 99, 132, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(54, 162, 235, 0.6)',
            ],
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: 'white'
              }
            }
          }
        }
      });
    };

    const createServicesChart = () => {
      if (servicesChart) {
        servicesChart.destroy();
      }
      const ctx = servicesChartRef.value.getContext('2d');
      const serviceCount = {};
      requests.value.forEach(request => {
        serviceCount[request.service] = (serviceCount[request.service] || 0) + 1;
      });
      
      servicesChart = new Chart(ctx, {
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
                color: 'white'
              },
              ticks: {
                color: 'white'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Service Type',
                color: 'white'
              },
              ticks: {
                color: 'white'
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: 'white'
              }
            }
          }
        }
      });
    };

    onMounted(async () => {
      await fetchAllRequests();
      nextTick(() => {
        if (statusChartRef.value && servicesChartRef.value) {
          createCharts();
        } else {
          console.error('Chart refs not available');
        }
      });
    });

    return {
      requests,
      loading,
      sortedRequests,
      statusChartRef,
      servicesChartRef,
      sortTable,
      getSortClass,
      formatDate,
    };
  }
};
</script>

<style scoped>
.customer-summary-container {
  font-family: Arial, sans-serif;
  background-color: #1e2a3a;
  color: white;
  padding: 20px;
  min-height: 100vh;
}

h2, h3 {
  color: white;
  margin-bottom: 20px;
}

.loading, .no-requests {
  text-align: center;
  padding: 20px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.charts-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.chart {
  background-color: #2c3e50;
  border-radius: 5px;
  padding: 20px;
  flex: 1;
}

.small-chart {
  width: 200px;
  height: 200px;
}

.table-container {
  background-color: #2c3e50;
  border-radius: 5px;
  overflow-x: auto;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table th,
.requests-table td {
  border: 1px solid #4a6278;
  padding: 12px;
  text-align: left;
}

.requests-table th {
  background-color: #34495e;
  color: white;
  cursor: pointer;
}

.requests-table tr:nth-child(even) {
  background-color: #3a536b;
}

.requests-table tr:hover {
  background-color: #4a6278;
}

.asc::after {
  content: ' ▲';
}

.desc::after {
  content: ' ▼';
}
</style>