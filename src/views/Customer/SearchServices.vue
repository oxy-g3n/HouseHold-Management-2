<template>
  <div class="services-container">
    <div class="header">
      <div class="logo-section">
        <h1>Services</h1>
        <p>All Available Services</p>
      </div>
      <div class="search-create-container">
        <label for="search-input" class="sr-only">Search services or subservices</label>
        <input
          id="search-input"
          type="text"
          class="form-control search-input"
          placeholder="Search services or subservices"
          v-model="searchQuery"
          aria-label="Search services or subservices"
        />
      </div>
    </div>

    <div class="content-container">
      <div class="services-grid-container">
        <div v-if="processedServices.length" class="services-grid">
          <div
            v-for="service in processedServices"
            :key="service.service_id"
            class="service-card"
            @click="toggleSubservices(service.service_id)"
            tabindex="0"
            role="button"
            :aria-expanded="selectedService && selectedService.service_id === service.service_id"
            :aria-controls="`subservices-${service.service_id}`"
          >
            <div class="service-content">
              <h2>{{ service.service_info.service_name }}</h2>
              <p>{{ service.service_info.service_desc }}</p>
              <p>Created: {{ service.service_info.date_created }}</p>
            </div>
          </div>
        </div>
        <div v-else-if="loading" class="loading" aria-live="polite">Loading services...</div>
        <div v-else class="no-services" aria-live="polite">No services available.</div>
      </div>

      <div v-if="selectedService" class="subservices-container" :id="`subservices-${selectedService.service_id}`">
        <h3>Subservices for {{ selectedService.service_info.service_name }}</h3>
        <table class="subservices-table">
          <thead>
            <tr>
              <th scope="col">Subservice Name</th>
              <th scope="col">Base Rate</th>
              <th scope="col">View Servicemen</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subservice in filteredSubservices" :key="subservice.subservice_id">
              <td>{{ subservice.subservice_name }}</td>
              <td>${{ subservice.base_rate }}</td>
              <td>
                <button @click="viewServicemen(subservice)" class="btn btn-primary">
                  View Servicemen
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="selectedSubservice" class="servicemen-container">
        <h3>Servicemen for {{ selectedSubservice.subservice_name }}</h3>
        <table class="servicemen-table" v-if="approvedServicemen.length">
          <thead>
            <tr>
              <th scope="col" @click="sortTable('user_id')">User ID <span :class="getSortClass('user_id')"></span></th>
              <th scope="col" @click="sortTable('full_name')">Full Name <span :class="getSortClass('full_name')"></span></th>
              <th scope="col" @click="sortTable('average_rating')">Average Rating <span :class="getSortClass('average_rating')"></span></th>
              <th scope="col" @click="sortTable('experience')">Experience <span :class="getSortClass('experience')"></span></th>
              <th scope="col" @click="sortTable('pin_code')">Pin Code <span :class="getSortClass('pin_code')"></span></th>
              <th scope="col">Request</th>
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
                <button @click="requestServiceman(person.user_id, person.full_name)" class="btn btn-secondary">
                  Request
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else aria-live="polite">No approved servicemen available for this subservice.</div>
      </div>
    </div>
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
          serviceman.service === this.selectedSubservice.subservice_name && serviceman.approval == "1"
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
          "http://127.0.0.1:5000/users/getServicemen",
          {
            headers: {
              "Content-Type": "application/json",
              'Authorization': `${token}`,
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
                  Authorization: `${token}`
                },
              }
            );
            if (response.data && response.data.average_rating !== undefined) {
              serviceman.average_rating = response.data.average_rating;
            } else {
              serviceman.average_rating = "No ratings available";
            }
          } catch (error) {
            console.error(`Error fetching rating for serviceman ${serviceman.user_id}:`, error);
            serviceman.average_rating = "Error";
          }
        });

        await Promise.all(ratingPromises);
      } catch (error) {
        console.error("Error fetching average ratings:", error);
      }
    },
    toggleSubservices(serviceId) {
      if (this.selectedService && this.selectedService.service_id === serviceId) {
        this.selectedService = null;
      } else {
        this.selectedService = this.rawServices.find(service => service.service_id === serviceId);
        this.searchQuery = '';
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

        if (response.status === 201) {
          alert("Service request submitted successfully!");
        } else {
          alert("Failed to submit service request. Please try again.");
        }
      } catch (error) {
        console.error("Error submitting service request:", error);
        alert("An Error occurred while submitting the request!");
      }
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
  },
  created() {
    this.fetchServices();
    this.fetchServicemen();
    this.customerApproved = localStorage.getItem("cust_approval") == 1;
  },
};
</script>

<style scoped>
.services-container {
  font-family: Arial, sans-serif;
  background-color: #1e2a3a;
  color: white;
  padding: 20px;
  min-height: 100vh;
}

.header {
  background-color: #2c3e50;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 5px 5px 0 0;
}

.logo-section h1 {
  margin: 0;
  font-size: 24px;
}

.logo-section p {
  margin: 5px 0 0;
  font-size: 14px;
}

.content-container {
  background-color: #34495e;
  color: white;
  padding: 20px;
  border-radius: 0 0 5px 5px;
  display: flex;
  flex-direction: column;
}

.services-grid-container {
  overflow-x: auto;
  max-width: 100%;
}

.services-grid {
  display: flex;
  gap: 20px;
  padding: 10px;
  overflow-x: scroll;
}

.service-card {
  background-color: #2c3e50;
  border: 1px solid #4a6278;
  border-radius: 5px;
  overflow: hidden;
  transition: box-shadow 0.3s;
  text-align: center;
  min-width: 400px;
  max-width: 500px;
}

.service-card:hover,
.service-card:focus {
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.4);
  outline: none;
}

.service-content {
  padding: 15px;
}

.service-content h2 {
  margin-top: 0;
  font-size: 18px;
}

.service-content p {
  margin: 5px 0;
  font-size: 14px;
}

.table-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.servicemen-table,
.subservices-table {
  width: 100%;
  background-color: #34495e;
  border-radius: 5px;
  border-collapse: collapse;
  color: white;
}

.servicemen-table th,
.servicemen-table td,
.subservices-table th,
.subservices-table td {
  border: 1px solid #4a6278;
  padding: 10px;
  text-align: left;
}

.servicemen-table th,
.subservices-table th {
  background-color: #2c3e50;
  cursor: pointer;
}

.servicemen-table td,
.subservices-table td {
  background-color: #34495e;
}

/* Custom scrollbar */
.services-grid::-webkit-scrollbar {
  height: 8px;
}

.services-grid::-webkit-scrollbar-track {
  background: #34495e;
}

.services-grid::-webkit-scrollbar-thumb {
  background: #2c3e50;
  border-radius: 5px;
}

.services-grid::-webkit-scrollbar-thumb:hover {
  background: #4a6278;
}

.asc::after {
  content: ' ▲';
}

.desc::after {
  content: ' ▼';
}

.subservices-container,
.servicemen-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #2ecc71;
  color: white;
}

.btn-secondary:hover {
  background-color: #27ae60;
}

.search-input {
  min-width: 200px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #34495e;
  color: white;
}

.search-input::placeholder {
  color: #95a5a6;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>