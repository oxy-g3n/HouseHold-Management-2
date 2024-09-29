<template>
    <div class="services-container">
      <div v-if="processedServices.length" class="services-grid">
        <div v-for="service in processedServices" :key="service.id" class="service-card">
          <div class="service-content">
            <h3 style="color: black;">{{ service.service_name }}</h3>
            <p style="color: black;">{{ service.service_desc }}</p>
            <p style="color: black;"> Max Price: ${{ service.max_price }}</p>
            <p style="color: black;"> Created: {{ service.date_created }}</p>
          </div>
          <button @click="confirmDelete(service)" class="btn btn-danger">Delete Service</button>
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
        <div v-if="showModal" class="modal">
        <div class="modal-wrapper">
        <div class="modal-content">
          <p>Are you sure you want to delete {{ selectedService.service_name }}?</p>
          <button @click="deleteService" class="btn btn-danger">Yes, Delete</button>
          <button @click="cancelDelete" class="btn btn-secondary">Cancel</button>
        </div>
        </div>
        </div>
  </template>
  
  <script>
  // Script remains unchanged
  import axios from 'axios';
  
  export default {
    data() {
      return {
        rawServices: [],
        loading: true,
        showModal: false,
        selectedService: null
      };
    },
    computed: {
      processedServices() {
        return this.rawServices.map((service, index) => ({
          ...service,
          id: index // Add an id for key prop
        }));
      }
    },
    methods: {
      async fetchServices() {
        this.loading = true;
        try {
          const response = await axios.get('http://127.0.0.1:5000/services/listServices');
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
        this.showModal = true;
      },
      deleteService() {
        if (this.selectedService) {
          console.log(`Service Deleted: ${this.selectedService.service_name}`);
          // Here you would typically call an API to delete the service
          // For now, we'll just remove it from the local array
          this.rawServices = this.rawServices.filter(s => s !== this.selectedService);
        }
        this.showModal = false;
        this.selectedService = null;
      },
      cancelDelete() {
        this.showModal = false;
        this.selectedService = null;
      }
    },
    created() {
      this.fetchServices();
    }
  };
  </script>
  
  <style scoped>
  .services-container {
    padding: 20px;
  }
  .services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }
  .service-card {
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f9f9f9;
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .service-content {
    flex-grow: 1;
    padding: 20px;
  }
  .btn {
    margin-top: auto;
    padding: 10px;
    border: none;
    cursor: pointer;
    width: 100%;
    border-radius: 0 0 5px 5px;
  }
  .btn-danger {
    background-color: #d9534f;
    color: white;
  }
  .btn-secondary {
    background-color: #5bc0de;
    color: white;
  }
  .modal-wrapper {
  width: 50%;

}
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  
}
.modal-content .btn {
  margin-right: 10px;
  margin-top: 10px;
}
.modal-content p {
  margin-bottom: 15px;
}
  .modal {
  position: fixed;
  background: rgba(0, 0, 0, 0.5);
  color : black;
  display: flex;
  justify-content: center;
  align-items: center;
}
  .modal-content {
    background-color: white;
    
    padding: 20px;
    border-radius: 5px;
  }
  .loading, .no-services {
    text-align: center;
    padding: 20px;
    font-size: 18px;
  }
  </style>