<template>
  <div class="services-container">
    <div class="header">
      <div class="logo-section">
        <h1>Services</h1>
        <p>All Available Services</p>
      </div>
      <div class="search-create-container">
        <input
          type="text"
          class="form-control search-input"
          placeholder="Search"
          v-model="searchQuery"
        />
      </div>
    </div>

    <div class="content-container">
      <div class="services-grid-container">
        <div v-if="processedServices.length" class="services-grid">
          <div
            v-for="service in processedServices"
            :key="service.id"
            class="service-card"
          >
            <div class="service-content">
              <h1>{{ service.service_name }}</h1>
              <p>{{ service.service_desc }}</p>
              <p>Max Price: ${{ service.max_price }}</p>
              <p>Created: {{ service.date_created }}</p>
            </div>
            <button @click="viewServicemen(service)" class="btn btn-primary m-2">
              View Servicemen
            </button>
          </div>
        </div>
        <div v-else-if="loading" class="loading">Loading services...</div>
        <div v-else class="no-services">No services available.</div>
      </div>

      <!-- Updated Dynamic Table Container -->
      <div class="table-container" v-if="selectedServiceName !== 'None'">
        <h3>Servicemen for {{ selectedServiceName }}</h3>
        <table class="servicemen-table" v-if="filteredServicemen.length">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Full Name</th>
              <th>Service</th>
              <th>Rating</th>
              <th>Commission</th>
              <th>Experience</th>
              <th>Pin Code</th>
              <th>Request</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="person in filteredServicemen" :key="person.user_id">
              <td>{{ person.user_id }}</td>
              <td>{{ person.full_name }}</td>
              <td>{{ person.service }}</td>
              <td>{{ person.Rating !== null ? person.Rating : 'N/A' }}</td>
              <td>{{ person.commission !== null ? person.commission : 'N/A' }}</td>
              <td>{{ person.experience }} years</td>
              <td>{{ person.pin_code }}</td>
              <td>
                <button @click="requestServiceman(person.user_id)" class="btn btn-secondary">
                  Request
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else>No servicemen available for this service.</div>
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
      selectedServiceName: "None",
      loading: true,
      searchQuery: '',
    };
  },
  computed: {
    processedServices() {
      return this.rawServices
        .map((service, index) => ({
          ...service,
          id: index,
        }))
        .filter((service) => {
          const searchLower = this.searchQuery.toLowerCase();
          return (
            service.service_name.toLowerCase().includes(searchLower) ||
            service.service_desc.toLowerCase().includes(searchLower)
          );
        });
    },
    filteredServicemen() {
      return this.allServicemen.filter(serviceman => 
        serviceman.service === this.selectedServiceName
      );
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
        } else {
          console.error("Unexpected data format:", response.data);
          this.allServicemen = [];
        }
      } catch (error) {
        console.error("Error fetching servicemen:", error);
        this.allServicemen = [];
      }
    },
    viewServicemen(service) {
      console.log(`Viewing servicemen for: ${service.service_name}`);
      this.selectedServiceName = service.service_name;
    },
    
 async requestServiceman(userId) {
      try {
        const token = localStorage.getItem("cust_Token");
        const customerId = localStorage.getItem("cust_id");
        const customerName = localStorage.getItem("cust_Fullname");
        const customerAddress = localStorage.getItem("cust_pin");

        const requestData = {
          customer_id: customerId,
          serviceman_id: userId,
          status: "requested",
          service: this.selectedServiceName,
          cust_Fullname: customerName,
          pin_code: customerAddress
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
        alert("An error occurred while submitting the service request. Please try again later.");
      }
    },
  },
  created() {
    this.fetchServices();
    this.fetchServicemen();
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

.service-card:hover {
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.4);
}

.service-content {
  padding: 15px;
}

.service-content h1 {
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

.servicemen-table {
  width: 100%;
  background-color: #34495e;
  border-radius: 5px;
  border-collapse: collapse;
  color: white;
}

.servicemen-table th,
.servicemen-table td {
  border: 1px solid #4a6278;
  padding: 10px;
  text-align: left;
}

.servicemen-table th {
  background-color: #2c3e50;
}

.servicemen-table td {
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
</style>