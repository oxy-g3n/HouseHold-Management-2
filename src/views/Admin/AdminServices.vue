<template>
  <div class="services-container">
    <div class="header">
      <div class="logo-section">
        <h1>Services</h1>
        <p>Service Management</p>
      </div>
      <div class="search-create-container">
      <input type="text" class="form-control search-input" placeholder="Search" v-model="searchQuery">
      <button type="button" class="btn btn-primary create-service-btn" @click="showModal = true">
        Create Service
      </button>
      </div>
    </div>

    <div class="content-container">
      <div v-if="processedServices.length" class="services-grid">
        <div v-for="service in processedServices" :key="service.id" class="service-card">
          <div class="service-content">
            <h3>{{ service.service_name }}</h3>
            <p>{{ service.service_desc }}</p>
            <p>Max Price: ${{ service.max_price }}</p>
            <p>Created: {{ service.date_created }}</p>
          </div>
          <button @click="confirmDelete(service)" class="btn btn-danger m-2">Delete Service</button>
        </div>
      </div>
      <div v-else-if="loading" class="loading">
        Loading services...
      </div>
      <div v-else class="no-services">
        No services available.
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-wrapper">
        <div class="modal-content">
          <p class=" m-2">Are you sure you want to delete "{{ selectedService.service_name }}"?</p>
          <button @click="deleteService" class="btn btn-danger mb-1">Yes, Delete</button>
          <button @click="cancelDelete" class="btn btn-secondary mb-1">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Create Service Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Service</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label for="serviceName">Service Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="serviceName"
                  v-model="formData.service_name"
                  required
                />
              </div>

              <div class="form-group">
                <label for="serviceDescription">Service Description</label>
                <textarea
                  class="form-control"
                  id="serviceDescription"
                  v-model="formData.service_description"
                  rows="3"
                  required
                ></textarea>
              </div>

              <div class="form-group">
                <label for="maxPrice">Max Price</label>
                <input
                  type="number"
                  class="form-control"
                  id="maxPrice"
                  v-model="formData.max_price"
                  required
                />
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
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
      loading: true,
      showModal: false,
      showDeleteModal: false,
      selectedService: null,
      searchQuery: '', // Add this line
      formData: {
        service_name: "",
        service_description: "",
        max_price: ""
      }
    };
  },
  computed: {
    processedServices() {
      return this.rawServices
        .map((service, index) => ({
          ...service,
          id: index
        }))
        .filter(service => {
          const searchLower = this.searchQuery.toLowerCase();
          return service.service_name.toLowerCase().includes(searchLower) ||
                 service.service_desc.toLowerCase().includes(searchLower);
        });
    }
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.get('http://127.0.0.1:5000/services/listServices', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `${token}`
          },
        });
        if (Array.isArray(response.data)) {
          this.rawServices = response.data;
        } else {
          console.error('Unexpected data format:', response.data);
          this.rawServices = [];
        }
      } catch (error) {
        console.error('Error fetching services:', error);
        this.rawServices = [];
      } finally {
        this.loading = false;
      }
    },
    confirmDelete(service) {
      this.selectedService = service;
      this.showDeleteModal = true;
    },
    deleteService() {
      if (this.selectedService) {
        console.log(`Service Deleted: ${this.selectedService.service_name}`);
        this.rawServices = this.rawServices.filter(s => s !== this.selectedService);
      }
      this.showDeleteModal = false;
      this.selectedService = null;
    },
    cancelDelete() {
      this.showDeleteModal = false;
      this.selectedService = null;
    },
    closeModal() {
      this.showModal = false;
    },
    async submitForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/createService",
          {
            'action': "createService",
            'service_name': this.formData.service_name,
            'service_description': this.formData.service_description,
            'max_price': this.formData.max_price
          },
          {
            headers: {
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    }
  },
  created() {
    this.fetchServices();
  }
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

.create-service-btn {
  background-color: #3498db;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.create-service-btn:hover {
  background-color: #2980b9;
}

.content-container {
  background-color: #34495e;
  color: white;
  padding: 20px;
  border-radius: 0 0 5px 5px;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.service-card {
  background-color: #2c3e50;
  border: 1px solid #4a6278;
  border-radius: 5px;
  overflow: hidden;
  transition: box-shadow 0.3s;
  text-align: center; /* Add this line */

}

.service-card:hover {
  box-shadow: 0 8px 8px rgba(0,0,0,0.4);
  

}

.service-content {
  padding: 15px;
}

.service-content h3 {
  margin-top: 0;
  font-size: 18px;
}

.service-content p {
  margin: 5px 0;
  font-size: 14px;
}

.btn {
  padding: 8px 12px;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.btn-secondary {
  background-color: #7f8c8d;
  color: white;
}

.btn-secondary:hover {
  background-color: #6c7a7d;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  
}

.modal-wrapper {
  background-color: #34495e;
  padding: 20px;
  border-radius: 5px;
}

.modal-content {
  color: black;
}

.modal-content p {
  margin-bottom: 15px;
}

.modal-content .btn {
  margin-right: 10px;
}

.loading, .no-services {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .create-service-btn {
    margin-top: 10px;
  }
  
}

.search-create-container {
  display: flex;
  align-items: center;
}


.search-input {
    margin-right: 1em;
  }

</style>