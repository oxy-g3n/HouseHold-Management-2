<template>
  <div class="service-dashboard">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="text-3xl font-bold">Services Dashboard</h1>
          <p class="text-sm opacity-75">All Available Services</p>
        </div>
        <div class="header-actions">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search services or subservices"
              class="search-input"
              aria-label="Search services or subservices"
            />
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="dashboard-content">
      <!-- Services Grid -->
      <div class="kanban-container" v-if="!loading">
        <div class="kanban-wrapper">
          <div 
            v-for="service in processedServices" 
            :key="service.service_id" 
            class="kanban-column"
          >
            <div class="kanban-card" :class="{ 'active': selectedService?.service_id == service.service_id }">
              <div class="card-header">
                <h3>{{ service.service_info.service_name }}</h3>
              </div>
              <p class="service-description">{{ service.service_info.service_desc }}</p>
              
              <div class="service-meta">
                <span class="date">Created: {{ service.service_info.date_created }}</span>
                <span class="subservice-count">
                  {{ service.subservices.length }} Subservices
                </span>
              </div>
              
              <div class="card-actions">
                <button 
                  @click="toggleSubservices(service.service_id)"
                  class="action-btn secondary"
                  :class="{ 'active': selectedService?.service_id == service.service_id }"
                >
                  {{ selectedService?.service_id == service.service_id ? 'Hide Details' : 'View Details' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else class="loading-state">
        <div class="loader"></div>
        <p>Loading services...</p>
      </div>

      <!-- Slide-out Subservices Panel -->
      <div 
        class="subservices-panel"
        :class="{ 'panel-open': selectedService }"
      >
        <div v-if="selectedService" class="panel-content">
          <div class="panel-header">
            <h2>{{ selectedService.service_info.service_name }} - Subservices</h2>
            <button @click="selectedService = null" class="close-panel">
              <i class="fas fa-times">×</i>
            </button>
          </div>
          
          <div class="subservices-list">
            <div
              v-for="subservice in filteredSubservices" 
              :key="subservice.subservice_id"
              class="subservice-item"
            >
              <div class="subservice-info">
                <h4>{{ subservice.subservice_name }}</h4>
                <p class="base-rate">Base Rate: ${{ subservice.base_rate }}</p>
              </div>
              <div class="subservice-actions">
                <button 
                  @click="viewServicemen(subservice)" 
                  class="action-btn primary"
                >
                  View Servicemen
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Servicemen Panel -->
      <div 
        v-if="selectedSubservice"
        class="servicemen-panel"
        :class="{ 'panel-open': selectedSubservice }"
      >
        <div class="panel-content">
          <div class="panel-header">
            <h2>Servicemen for {{ selectedSubservice.subservice_name }}</h2>
            <button @click="selectedSubservice = null" class="close-panel">
              <i class="fas fa-times">×</i>
            </button>
          </div>
          
          <div class="servicemen-list">
            <div v-if="approvedServicemen.length" class="servicemen-table-container">
              <table class="servicemen-table">
                <thead>
                  <tr>
                    <th @click="sortTable('user_id')">
                      User ID 
                      <span :class="getSortClass('user_id')"></span>
                    </th>
                    <th @click="sortTable('full_name')">
                      Full Name 
                      <span :class="getSortClass('full_name')"></span>
                    </th>
                    <th @click="sortTable('average_rating')">
                      Rating 
                      <span :class="getSortClass('average_rating')"></span>
                    </th>
                    <th @click="sortTable('experience')">
                      Experience 
                      <span :class="getSortClass('experience')"></span>
                    </th>
                    <th @click="sortTable('pin_code')">
                      Pin Code 
                      <span :class="getSortClass('pin_code')"></span>
                    </th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="person in approvedServicemen" :key="person.user_id">
                    <td>{{ person.user_id }}</td>
                    <td>{{ person.full_name }}</td>
                    <td>{{ person.average_rating !== null ? person.average_rating : 'N/A' }}</td>
                    <td>{{ person.experience }} years</td>
                    <td>{{ person.pin_code }}</td>
                    <td>
                      <button 
                        @click="requestServiceman(person.user_id, person.full_name)" 
                        class="action-btn primary"
                        :disabled="!customerApproved"
                      >
                        Request
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="no-servicemen">
              No approved servicemen available for this subservice.
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      rawServices: [],
      allServicemen: [],
      selectedService: null,
      selectedSubservice: null,
      loading: true,
      searchQuery: '',
      sortKey: '',
      sortAsc: true,
      customerApproved: false,
    };
  },
  computed: {
    processedServices() {
      const searchLower = this.searchQuery.toLowerCase();
      return this.rawServices.filter((service) => {
        const serviceMatch = 
          service.service_info.service_name.toLowerCase().includes(searchLower) ||
          service.service_info.service_desc.toLowerCase().includes(searchLower);
        
        const subserviceMatch = service.subservices.some(subservice => 
          subservice.subservice_name.toLowerCase().includes(searchLower)
        );

        return serviceMatch || subserviceMatch;
      });
    },
    filteredSubservices() {
      if (!this.selectedService) return [];
      
      const searchLower = this.searchQuery.toLowerCase();
      return this.selectedService.subservices.filter(subservice => 
        subservice.subservice_name.toLowerCase().includes(searchLower)
      );
    },
    approvedServicemen() {
      return this.allServicemen
        .filter(serviceman => 
          serviceman.service == this.selectedSubservice.subservice_name && 
          serviceman.approval == "1"
        )
        .sort((a, b) => {
          const modifier = this.sortAsc ? 1 : -1;
          if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
          if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
          return 0;
        });
    },
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      try {
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          "http://127.0.0.1:5000/services/listServices",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        if (Array.isArray(response.data)) {
          this.rawServices = response.data;
        } else {
          console.error("Unexpected data format:", response.data);
          this.rawServices = [];
        }
      } catch (error) {
        console.error("Error fetching services:", error);
        this.rawServices = [];
      } finally {
        this.loading = false;
      }
    },
    async fetchServicemen() {
      try {
        const token = localStorage.getItem("cust_Token");
        const response = await axios.get(
          "http://127.0.0.1:5000/users/getProviders",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        if (Array.isArray(response.data)) {
          this.allServicemen = response.data;
          await this.fetchAverageRatings();
        } else {
          console.error("Unexpected data format:", response.data);
          this.allServicemen = [];
        }
      } catch (error) {
        console.error("Error fetching servicemen:", error);
        this.allServicemen = [];
      }
    },
    async fetchAverageRatings() {
      try {
        const token = localStorage.getItem("cust_Token");
        const ratingPromises = this.allServicemen.map(async (serviceman) => {
          try {
            const response = await axios.get(
              `http://127.0.0.1:5000/requests/averageRating/${serviceman.user_id}`,
              {
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `${token}`,
                },
              }
            );
            serviceman.average_rating = response.data?.average_rating ?? null;
          } catch (error) {
            console.error(`Error fetching rating for serviceman ${serviceman.user_id}:`, error);
            serviceman.average_rating = null;
          }
        });

        await Promise.all(ratingPromises);
      } catch (error) {
        console.error("Error fetching average ratings:", error);
      }
    },
    toggleSubservices(serviceId) {
      if (this.selectedService && this.selectedService.service_id == serviceId) {
        this.selectedService = null;
      } else {
        this.selectedService = this.rawServices.find(service => service.service_id == serviceId);
      }
      this.selectedSubservice = null;
    },
    viewServicemen(subservice) {
      this.selectedSubservice = subservice;
    },
    async requestServiceman(userId, serviceman_name) {
      if (!this.customerApproved) {
        alert("You are not approved to make service requests. Please contact support for assistance.");
        return;
      }

      try {
        const token = localStorage.getItem("cust_Token");
        const customerId = localStorage.getItem("cust_id");
        const customerName = localStorage.getItem("cust_Fullname");
        const customerAddress = localStorage.getItem("cust_pin");
        
        const requestData = {
          customer_id: customerId,
          serviceman_id: userId,
          status: "requested",
          service: this.selectedSubservice.subservice_name,
          serviceman_Fullname: serviceman_name,
          cust_Fullname: customerName,
          pin_code: customerAddress,
          subservice_id: this.selectedSubservice.subservice_id
        };

        const response = await axios.post(
          "http://127.0.0.1:5000/requests/addServiceRequest",
          requestData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );

        if (response.status == 201) {
          alert("Service request submitted successfully!");
        } else {
          alert("Failed to submit service request. Please try again.");
        }
      } catch (error) {
        console.error("Error submitting service request:", error);
        alert("An error occurred while submitting the request!");
      }
    },
    sortTable(key) {
      if (this.sortKey == key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },
    getSortClass(key) {
      if (this.sortKey == key) {
        return this.sortAsc ? 'asc' : 'desc';
      }
      return '';
    },
  },
  created() {
    this.fetchServices();
    this.fetchServicemen();
    this.customerApproved = localStorage.getItem("cust_approval") == "1";
  },
};
</script>

<style scoped>
.service-dashboard {
  min-height: 100vh;
  background-color: #f8fafc;
  color: #1e293b;
}

.dashboard-header {
  background-color: #1e40af;
  padding: 1.5rem;
  color: white;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.search-box {
  position: relative;
  margin-right: 1rem;
}

.search-input {
  background: rgb(255, 254, 254);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: 0.5rem;
  color: black;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.7;
}

.dashboard-content {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  position: relative;
}

.kanban-container {
  overflow-x: auto;
  padding: 1rem 0;
}

.kanban-wrapper {
  display: flex;
  gap: 1.5rem;
  padding: 0.5rem;
}
.kanban-column {
  min-width: 320px;
  max-width: 320px;
  flex: 1;
}

.kanban-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.kanban-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.kanban-card.active {
  border-color: #1e40af;
  box-shadow: 0 4px 6px rgba(30, 64, 175, 0.1);
}

.card-header {
  margin-bottom: 1rem;
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.service-description {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.service-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.action-btn.primary {
  background-color: #1e40af;
  color: white;
}

.action-btn.primary:hover {
  background-color: #1e3a8a;
}

.action-btn.primary:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.action-btn.secondary {
  background-color: #e2e8f0;
  color: #1e293b;
}

.action-btn.secondary:hover {
  background-color: #cbd5e1;
}

.action-btn.secondary.active {
  background-color: #1e40af;
  color: white;
}

.subservices-panel,
.servicemen-panel {
  position: fixed;
  top: 0;
  right: -100%;
  width: 100%;
  max-width: 600px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 6px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 50;
}

.panel-open {
  right: 0;
}

.panel-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.close-panel {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
}

.close-panel:hover {
  color: #1e293b;
}

.subservices-list,
.servicemen-list {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.subservice-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subservice-info h4 {
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.base-rate {
  font-size: 0.875rem;
  color: #64748b;
}

.servicemen-table-container {
  overflow-x: auto;
}

.servicemen-table {
  width: 100%;
  border-collapse: collapse;
}

.servicemen-table th,
.servicemen-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.servicemen-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #1e293b;
  cursor: pointer;
}

.servicemen-table th:hover {
  background-color: #f1f5f9;
}

.asc::after {
  content: " ↑";
}

.desc::after {
  content: " ↓";
}

.no-servicemen {
  text-align: center;
  color: #64748b;
  padding: 2rem;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
}

.loader {
  border: 3px solid #f3f3f3;
  border-radius: 50%;
  border-top: 3px solid #1e40af;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .search-input {
    width: 100%;
  }

  .kanban-column {
    min-width: 280px;
  }

  .subservices-panel,
  .servicemen-panel {
    max-width: 100%;
  }

  .subservice-item {
    flex-direction: column;
    gap: 1rem;
  }

  .subservice-actions {
    width: 100%;
    display: flex;
    justify-content: stretch;
  }

  .subservice-actions button {
    width: 100%;
  }
}
</style>