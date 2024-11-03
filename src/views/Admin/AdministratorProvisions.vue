<template>
  <div class="service-dashboard">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="text-3xl font-bold">Provisions Dashboard</h1>
          <p class="text-sm opacity-75">Manage Provisions</p>
        </div>
        <div class="header-actions">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input
              type="text" 
              v-model="searchQuery"
              placeholder="Search provisions..." 
              class="search-input text-bg-light"
            />
          </div>
          <button @click="showCreateServiceModal = true" class="create-btn">
            <i class="fas fa-plus"></i>
            New Provision
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="dashboard-content">
      <!-- Kanban Board -->
      <div class="kanban-container" v-if="!loading">
  <div class="kanban-wrapper">
    <div 
      v-for="service in processedServices" 
      :key="service.service_id" 
      class="kanban-column"
    >
      <div class="kanban-card" :class="{ 'active': selectedService?.service_id === service.service_id }">
        <div class="card-header">
          <h3>{{ service.service_info.service_name }}</h3>
        </div>
        
        <!-- Move the action buttons outside of card-header to position them below the card name -->
        <div class="card-actions">
          <button @click="showEditServiceModal(service)" class="action-btn edit">
            <i class="fas fa-pencil-alt">Edit</i>
          </button>
          <button @click="confirmDeleteService(service)" class="action-btn delete">
            <i class="fas fa-trash">Delete</i>
          </button>
          <button @click="showDeleteSubserviceModal(service)" class="delete-subservice">
            <i class="fas fa-trash">Delete SubProvision</i>
          </button>
        </div>
        <br>
        <p class="service-description">{{ service.service_info.service_desc }}</p>
        
        <div class="service-meta">
          <span class="date">Created: {{ service.service_info.date_created }}</span>
          <span class="subservice-count">
            {{ service.subservices.length }} SubProvisions
          </span>
        </div>
        
        <div class="card-actions">
          <button @click="showAddSubserviceModal(service)" class="action-btn primary">
            Add Subprovision
          </button>
          <button 
            @click="toggleSubservices(service)"
            class="action-btn secondary"
            :class="{ 'active': selectedService?.service_id === service.service_id }"
          >
            {{ selectedService?.service_id === service.service_id ? 'Hide Details' : 'View Details' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</div>


      <!-- Loading State -->
      <div v-else class="loading-state">
        <div class="loader"></div>
        <p>Loading provisions...</p>
      </div>

      <!-- Slide-out Subservices Panel -->
      <div 
        class="subservices-panel"
        :class="{ 'panel-open': selectedService }"
      >
        <div v-if="selectedService" class="panel-content">
          <div class="panel-header">
            <h2>{{ selectedService.service_info.service_name }} - SubProvisions</h2>
            <button @click="selectedService = null" class="close-panel">
              <i class="fas fa-times">X</i>
            </button>
          </div>
          
          <div class="subservices-list">
            <div
              v-for="subservice in filteredSubservices" 
              :key="subservice.subservice_id"
              class="subservice-item">
              <div class="subservice-info">
                <h4>{{ subservice.subservice_name }}</h4>
                <p class="base-rate">Base Rate: ${{ subservice.base_rate }}</p>
              </div>
              <div class="subservice-actions">
                <button @click="showEditSubserviceModal(subservice)" class="edit-subservice">
                  <i class="fas fa-pencil-alt">Edit</i>
                </button>

              </div>
            </div>
          </div>
        </div>
      </div>
    </main>


    <!-- Create Service Modal -->
    <div v-if="showCreateServiceModal" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Provision</h5>
            <button type="button" class="close" @click="closeCreateServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitCreateServiceForm">
              <div class="form-group">
                <label for="serviceName">Provision Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="serviceName"
                  v-model="createServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="serviceDescription">Provision Description</label>
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
            <h5 class="modal-title">Add Subprovision</h5>
            <button type="button" class="close" @click="closeAddSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitAddSubserviceForm">
              <div class="form-group">
                <label for="subserviceName">Subprovision Name</label>
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
            <h5 class="modal-title">Delete Subprovision</h5>
            <button type="button" class="close" @click="closeDeleteSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitDeleteSubserviceForm">
              <div class="form-group">
                <label for="subserviceSelect">Select Subprovision to Delete</label>
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
            <h5 class="modal-title">Confirm Delete Provision</h5>
            <button type="button" class="close" @click="closeDeleteServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete "{{ selectedService.service_info.service_name }}"?</p>
            <p>This will also delete all associated subprovisions.</p>
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
            <h5 class="modal-title">Edit Provision</h5>
            <button type="button" class="close" @click="closeEditServiceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditServiceForm">
              <div class="form-group">
                <label for="editServiceName">Provision Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="editServiceName"
                  v-model="editServiceForm.service_name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="editServiceDescription">Provision Description</label>
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
            <h5 class="modal-title">Edit Subprovision</h5>
            <button type="button" class="close" @click="closeEditSubserviceModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitEditSubserviceForm">
              <div class="form-group">
                <label for="editSubserviceName">Subprovision Name</label>
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

export default {
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
      console.log(service);
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

.search-box {
  position: relative;
  margin-right: 1rem;
}

.search-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border-radius: 0.5rem;
  color: white;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.7;
}

.create-btn {
  background-color: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.create-btn:hover {
  background-color: #1d4ed8;
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
}

.kanban-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.kanban-card.active {
  border-color: #2563eb;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
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
  color: #64748b;
  margin-bottom: 1rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.action-btn.primary {
  background-color: #2563eb;
  color: white;
}

.action-btn.secondary {
  background-color: #e2e8f0;
  color: #1e293b;
}

.action-btn.edit {
  color: #2563eb;
}

.action-btn.delete {
  color: #dc2626;
}

.subservices-panel {
  position: fixed;
  right: -400px;
  top: 0;
  width: 400px;
  height: 100vh;
  background: white;
  box-shadow: -4px 0 6px -1px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease-in-out;
  z-index: 1000;
}

.panel-open {
  right: 0;
}

.panel-content {
  padding: 1.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 1rem;
}

.subservices-list {
  flex: 1;
  overflow-y: auto;
}

.subservice-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.subservice-info h4 {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.base-rate {
  font-size: 0.875rem;
  color: #64748b;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loader {
  border: 3px solid #f3f3f3;
  border-radius: 50%;
  border-top: 3px solid #2563eb;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.header-actions
{
  display: flex;
  align-items: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-input {
    width: 100%;
  }
  
  .subservices-panel {
    width: 100%;
    right: -100%;
  }
}
</style>