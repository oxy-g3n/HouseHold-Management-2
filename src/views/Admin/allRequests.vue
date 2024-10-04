<template>
  <div class="dashboard-container">
    <h2>Dashboard</h2>
    
    <div v-if="loading" class="loading">Loading data...</div>
    <div v-else>
       <!-- Stats Cards -->
       <div class="stats-cards">
        <div class="stat-card">
          <h3>Total Requests</h3>
          <p>{{ requests.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Completed Requests</h3>
          <p>{{ requests.filter(r => r.status === 'completed').length }}</p>
        </div>
        <div class="stat-card">
          <h3>Active Requests</h3>
          <p>{{ requests.filter(r => r.status === 'active').length }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Users</h3>
          <p>{{ servicemen.length + customers.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Servicemen</h3>
          <p>{{ servicemen.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Customers</h3>
          <p>{{ customers.length }}</p>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-container">
        <div class="chart">
          <h3>Most Requested Services</h3>
          <canvas ref="servicesChartRef"></canvas>
        </div>
        <div class="chart">
          <h3>User Creation Timeline</h3>
          <canvas ref="userCreationChartRef"></canvas>
        </div>
      </div>

      <!-- Requests Table -->
      <div class="table-container">
        <h3>All Service Requests</h3>
        <table class="requests-table">
          <thead>
            <tr>
              <th @click="sortTable('serviceRequest_id')">Request ID <span :class="getSortClass('serviceRequest_id')"></span></th>
              <th @click="sortTable('customer_id')">Customer ID<span :class="getSortClass('customer_id')"></span></th>
              <th @click="sortTable('customer_name')">Customer Name <span :class="getSortClass('customer_name')"></span></th>
              <th @click="sortTable('serviceman_id')">Serviceman ID<span :class="getSortClass('serviceman_id')"></span></th>
              <th @click="sortTable('serviceman_name')">Serviceman Name <span :class="getSortClass('serviceman_name')"></span></th>
              <th @click="sortTable('service')">Service <span :class="getSortClass('service')"></span></th>
              <th @click="sortTable('status')">Status <span :class="getSortClass('status')"></span></th>
              <th @click="sortTable('rating')">Rating <span :class="getSortClass('rating')"></span></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in sortedRequests" :key="request.serviceRequest_id">
              <td>{{ request.serviceRequest_id }}</td>
              <td>{{ request.customer_id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.serviceman_id }}</td>
              <td>{{ request.serviceman_name }}</td>
              <td>{{ request.service }}</td>
              <td>{{ request.status }}</td>
              <td>{{ request.rating !== null ? request.rating : 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Colors } from 'chart.js';
import Chart from 'chart.js/auto';
import { ref, onMounted, nextTick } from 'vue';

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
        "http://127.0.0.1:5000/users/getServicemen",
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
        "http://127.0.0.1:5000/users/getCustomers",
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
        "http://127.0.0.1:5000/users/getServicemen",
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
        "http://127.0.0.1:5000/users/getCustomers",
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
.dashboard-container {
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

.loading {
  text-align: center;
  padding: 20px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.stats-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #2c3e50;
  border-radius: 5px;
  padding: 20px;
  flex: 1 1 calc(33.333% - 20px);
  min-width: 200px;
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

.table-container {
  background-color: #2c3e50;
  border-radius: 5px;
  overflow-x: auto;
  margin-top: 30px;
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

.requests-table th:hover {
  background-color: #3a536b;
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