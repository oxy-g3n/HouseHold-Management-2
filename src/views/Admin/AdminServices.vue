<template>
  <div class="services-container">
    <div class="header">
      <div class="logo-section">
        <h1>Services</h1>
        <p>Service Management</p>
      </div>
      <div class="search-create-container">
        <input type="text" class="form-control search-input" placeholder="Search Services or Subservices" v-model="searchQuery">
        <button type="button" class="btn btn-primary create-service-btn" @click="showCreateServiceModal = true">
          Create Service
        </button>
      </div>
    </div>

    <div class="content-container">
      <div v-if="processedServices.length" class="services-grid">
        <div v-for="service in processedServices" :key="service.service_id" class="service-card">
          <div class="service-content">
            <h3>{{ service.service_info.service_name }}</h3>
            <p>{{ service.service_info.service_desc }}</p>
            <p>Created: {{ service.service_info.date_created }}</p>
            <div class="button-group">
              <button @click="showAddSubserviceModal(service)" class="btn btn-success">Add Subservice</button>
              <button @click="showDeleteSubserviceModal(service)" class="btn btn-warning">Delete Subservice</button>
              <button @click="showEditServiceModal(service)" class="btn btn-primary">Edit Service</button>
            </div>
            <button @click="toggleSubservices(service)" class="btn btn-info mt-2">
              Show Subservices
            </button>
          </div>
          <button @click="confirmDeleteService(service)" class="btn btn-danger mt-2">Delete Service</button>
        </div>
      </div>
      <div v-else-if="loading" class="loading">
        Loading services...
      </div>
      <div v-else class="no-services">
        No services available.
      </div>
    </div>

    <div class="subservices-section">
      <h2 v-if="!selectedService">No service selected</h2>
      <SubservicesTable
        v-else
        :subservices="filteredSubservices"
        :serviceName="selectedService.service_info.service_name"
        :searchQuery="searchQuery"
        @edit-subservice="showEditSubserviceModal"
      />
    </div>

    <!-- Create Service Modal -->
    <div v-if="showCreateServiceModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Service</h5>
            <button type="button" class="close" @click="closeCreateServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitCreateServiceForm">
              <div class="form-group">
                <label for="serviceName">Service Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="serviceName"
                  v-model="createServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="serviceDescription">Service Description</label>
                <textarea
                  class="form-control"
                  id="serviceDescription"
                  v-model="createServiceForm.service_description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeCreateServiceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Subservice Modal -->
    <div v-if="showAddSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Subservice</h5>
            <button type="button" class="close" @click="closeAddSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitAddSubserviceForm">
              <div class="form-group">
                <label for="subserviceName">Subservice Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="subserviceName"
                  v-model="addSubserviceForm.subservice_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="baseRate">Base Rate</label>
                <input
                  type="number"
                  class="form-control"
                  id="baseRate"
                  v-model.number="addSubserviceForm.base_rate"
                  required
                  min="0"
                  step="1"
                />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeAddSubserviceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Subservice Modal -->
    <div v-if="showDeleteSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Delete Subservice</h5>
            <button type="button" class="close" @click="closeDeleteSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitDeleteSubserviceForm">
              <div class="form-group">
                <label for="subserviceSelect">Select Subservice to Delete</label>
                <select
                  class="form-control"
                  id="subserviceSelect"
                  v-model="deleteSubserviceForm.subservice_name"
                  required
                >
                  <option v-for="subservice in selectedService.subservices" :key="subservice.subservice_id" :value="subservice.subservice_name">
                    {{ subservice.subservice_name }}
                  </option>
                </select>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeDeleteSubserviceModal">Cancel</button>
                <button type="submit" class="btn btn-danger">Delete</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Service Confirmation Modal -->
    <div v-if="showDeleteServiceModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete Service</h5>
            <button type="button" class="close" @click="closeDeleteServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete "{{ selectedService.service_info.service_name }}"?</p>
            <p>This will also delete all associated subservices.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteServiceModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteService">Delete</button>
          </div>
        </div>
      </div>
    </div>

        <!-- Edit Service Modal -->
        <div v-if="showEditServiceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Service</h5>
            <button type="button" class="close" @click="closeEditServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditServiceForm">
              <div class="form-group">
                <label for="editServiceName">Service Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editServiceName"
                  v-model="editServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="editServiceDescription">Service Description</label>
                <textarea
                  class="form-control"
                  id="editServiceDescription"
                  v-model="editServiceForm.service_description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditServiceModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Subservice Modal -->
    <div v-if="showEditSubserviceModalbool" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Subservice</h5>
            <button type="button" class="close" @click="closeEditSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditSubserviceForm">
              <div class="form-group">
                <label for="editSubserviceName">Subservice Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editSubserviceName"
                  v-model="editSubserviceForm.subservice_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="editBaseRate">Base Rate</label>
                <input
                  type="number"
                  class="form-control"
                  id="editBaseRate"
                  v-model.number="editSubserviceForm.base_rate"
                  required
                  min="0"
                  step="1"
                />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditSubserviceModal">Cancel</button>
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
import SubservicesTable from './SubservicesTable.vue';

export default {
  components: {
    SubservicesTable
  },
  data() {
    return {
      rawServices: [],
      loading: true,
      showCreateServiceModal: false,
      showAddSubserviceModalbool: false,
      showDeleteSubserviceModalbool: false,
      showDeleteServiceModal: false,
      selectedService: null,
      searchQuery: '',
      selectedService: null,
      showEditServiceModalbool: false,
      showEditSubserviceModalbool: false,

      createServiceForm: {
        service_name: "",
        service_description: "",
      },
      addSubserviceForm: {
        subservice_name: "",
        base_rate: null,
      },
      deleteSubserviceForm: {
        subservice_name: "",
      },
      editServiceForm: {
        service_actual_id: null,
        service_name: "",
        service_description: "",
      },
      editSubserviceForm: {
        subservice_id: null,
        subservice_name: "",
        subservice_previous_name: "",
        base_rate: null,
      },
    };
  },
  computed: {
    processedServices() {
      return this.rawServices.map(service => ({
        ...service,
        showSubservices: false
      })).filter(service => {
        const searchLower = this.searchQuery.toLowerCase();
        return service.service_info.service_name.toLowerCase().includes(searchLower) ||
               service.service_info.service_desc.toLowerCase().includes(searchLower) ||
               service.subservices.some(subservice => 
                 subservice.subservice_name.toLowerCase().includes(searchLower)
               );
      });
    },
    filteredSubservices() {
      if (!this.selectedService) return [];
      const searchLower = this.searchQuery.toLowerCase();
      return this.selectedService.subservices.filter(subservice =>
        subservice.subservice_name.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    toggleSubservices(service) {
      service.showSubservices = !service.showSubservices;
      this.selectedService = service.showSubservices ? service : null;
    },
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
    showAddSubserviceModal(service) {
      this.selectedService = service;
      this.showAddSubserviceModalbool = true;
    },
    showDeleteSubserviceModal(service) {
      this.selectedService = service;
      this.showDeleteSubserviceModalbool = true;
    },
    confirmDeleteService(service) {
      this.selectedService = service;
      this.showDeleteServiceModal = true;
    },
    closeCreateServiceModal() {
      this.showCreateServiceModal = false;
      this.createServiceForm = { service_name: "", service_description: "" };
    },
    closeAddSubserviceModal() {
      this.showAddSubserviceModalbool = false;
      this.addSubserviceForm = { subservice_name: "", base_rate: null };
    },
    closeDeleteSubserviceModal() {
      this.showDeleteSubserviceModalbool = false;
      this.deleteSubserviceForm = { subservice_name: "" };
    },
    closeDeleteServiceModal() {
      this.showDeleteServiceModal = false;
      this.selectedService = null;
    },
    async submitCreateServiceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/createService",
          {
            action: "createService",
            service_name: this.createServiceForm.service_name,
            service_description: this.createServiceForm.service_description,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeCreateServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitAddSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post( "http://127.0.0.1:5000/services/SubService",
          {
            action: "createService",
            sub_name: this.addSubserviceForm.subservice_name,
            service_actual_id: this.selectedService.service_id,
            base_rate: this.addSubserviceForm.base_rate,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeAddSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitDeleteSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/SubService",
          {
            action: "deleteService",
            sub_name: this.deleteSubserviceForm.subservice_name,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeDeleteSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async deleteService() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.post(
          "http://127.0.0.1:5000/services/createService",
          {
            action: "deleteService",
            service_name: this.selectedService.service_info.service_name
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeDeleteServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },

    showEditServiceModal(service) {
      this.editServiceForm.service_actual_id = service.service_id;
      this.editServiceForm.service_name = service.service_info.service_name;
      this.editServiceForm.service_description = service.service_info.service_desc;
      this.showEditServiceModalbool = true;
    },
    closeEditServiceModal() {
      this.showEditServiceModalbool = false;
      this.editServiceForm = { service_actual_id: null, service_name: "", service_description: "" };
    },
    showEditSubserviceModal(subservice) {
      this.editSubserviceForm.subservice_id = subservice.subservice_id;
      this.editSubserviceForm.subservice_name = subservice.subservice_name;
      this.editSubserviceForm.subservice_previous_name = subservice.subservice_name;
      this.editSubserviceForm.base_rate = subservice.base_rate;
      this.showEditSubserviceModalbool = true;
    },
    closeEditSubserviceModal() {
      this.showEditSubserviceModalbool = false;
      this.editSubserviceForm = { subservice_id: null, subservice_name: "", subservice_previous_name: "", base_rate: null };
    },
    async submitEditServiceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.put("http://127.0.0.1:5000/services/EditService",
          {
            action: "service",
            service_actual_id: this.editServiceForm.service_actual_id,
            service_name: this.editServiceForm.service_name,
            service_description: this.editServiceForm.service_description,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeEditServiceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
    async submitEditSubserviceForm() {
      try {
        const token = localStorage.getItem('admin_Token');
        const response = await axios.put("http://127.0.0.1:5000/services/EditService",
          {
            action: "subservice",
            subservice_id: this.editSubserviceForm.subservice_id,
            subservice_name: this.editSubserviceForm.subservice_name,
            subservice_previous_name: this.editSubserviceForm.subservice_previous_name,
            base_rate: this.editSubserviceForm.base_rate,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `${token}`
            }
          }
        );
        alert(response.data);
        this.closeEditSubserviceModal();
        this.fetchServices();
      } catch (error) {
        console.error(error);
        alert(error.response.data);
      }
    },
  

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
  transition: box-shadow 0.3s;
  text-align: center;
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

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.button-group .btn {
  flex: 1;
  margin: 0 5px;
}

.subservices-section {
  margin-top: 30px;
}

.subservices-section h2 {
  color: white;
  text-align: center;
}

.services-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-container {
  overflow-x: auto; /* Enable horizontal scrolling */
  display: flex;
  padding: 10px;
  gap: 10px;
  white-space: nowrap; /* Prevents cards from wrapping */
}

.services-grid {
  display: flex;
  gap: 20px; /* Add spacing between cards */
}


button-group {
  display: flex;
  gap: 5px;
}

.no-services, .loading {
  text-align: center;
}

/* Custom scrollbar */
.content-container::-webkit-scrollbar {
  height: 8px;
}

.content-container::-webkit-scrollbar-track {
  background: #34495e;
}

.content-container::-webkit-scrollbar-thumb {
  background: #2c3e50;
  border-radius: 5px;
}

.content-container::-webkit-scrollbar-thumb:hover {
  background: #4a6278;
}

</style>















