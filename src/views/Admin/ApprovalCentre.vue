<template>
  <div class="management-portal">
    <!-- Header Section -->
    <div class="portal-header p-4 rounded-3 mb-4">
      <h2 class="text-white mb-3">User Management Portal</h2>
      <div class="control-panel d-flex gap-3 align-items-center flex-wrap">
        <div class="segment-control d-flex rounded-pill overflow-hidden">
          <button 
            @click="activeSection = 'servicemen'"
            :class="['segment-btn', activeSection === 'servicemen' ? 'active' : '']"
          >
            Service Providers
          </button>
          <button 
            @click="activeSection = 'customers'"
            :class="['segment-btn', activeSection === 'customers' ? 'active' : '']"
          >
            Customers
          </button>
        </div>
        
        <div class="search-container flex-grow-1">
          <input 
            type="text" 
            v-model="searchQuery"
            class="search-input form-control"
            :placeholder="`Search ${activeSection}...`"
          >
        </div>
      </div>
    </div>

    <!-- Timeline Section -->
    <div class="timeline-container">
      <TransitionGroup 
        name="timeline-list" 
        tag="div" 
        class="timeline-wrapper"
      >
        <div 
          v-for="user in filteredUsers" 
          :key="user.user_id"
          class="timeline-item"
        >
          <!-- Timeline Marker -->
          <div class="timeline-marker"></div>
          
          <!-- User Card -->
          <div class="user-card">
            <div class="user-card-header d-flex justify-content-between align-items-center">
              <h3 class="user-name mb-0">
                <template v-if="activeSection === 'servicemen'">
                  <button 
                    class="pdf-button"
                    @click="showPdfPreview(user)"
                    @mouseover="previewUser = user"
                    @mouseleave="previewUser = null"
                  >
                    {{ user.full_name }}
                    <i class="fas fa-file-pdf ms-2"></i>
                  </button>
                </template>
                <template v-else>
                  <div class = "pdf-button">
                    {{ user.full_name }}
                  </div>
                  </template>
              </h3>
              <div class="approval-toggle flex-column">
                <label class="switch">
                  Toggle Approval
                  <input 
                    type="checkbox"
                    :checked="user.approval"
                    @change="updateApproval(user)"
                  >
                  <span class="slider"></span>
                </label>
              </div>
            </div>

            <div class="user-card-body">
              <div class="user-details">
                <div class="detail-row">
                  <span class="detail-label">User ID:</span>
                  <span class="detail-value">{{ user.user_id }}</span>
                </div>
                
                <template v-if="activeSection === 'servicemen'">
                  <div class="detail-row">
                    <span class="detail-label">Service:</span>
                    <span class="detail-value">{{ user.service }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Rating:</span>
                    <span class="detail-value">
                      {{ user.Rating !== null ? `${user.Rating} ⭐` : 'N/A' }}
                    </span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Experience:</span>
                    <span class="detail-value">{{ user.experience }} years</span>
                  </div>
                </template>
                
                <template v-else>
                  <div class="detail-row">
                    <span class="detail-label">Email:</span>
                    <span class="detail-value">{{ user.mail }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Mobile:</span>
                    <span class="detail-value">{{ user.mobile }}</span>
                  </div>
                </template>
                
                <div class="detail-row">
                  <span class="detail-label">Pin Code:</span>
                  <span class="detail-value">{{ user.pin_code }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- PDF Preview Modal -->
    <div 
      v-if="previewUser"
      class="preview-card"
      :style="previewPosition"
    >
      <div class="preview-header">
        <h4>{{ previewUser.full_name }}</h4>
        <p>Service Provider Details</p>
      </div>
      <div class="preview-body">
        <p>Click to view complete profile and certificates</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed } from 'vue';

export default {
  name: 'UserManagementTimeline',
  
  setup() {
    const activeSection = ref('servicemen');
    const servicemen = ref([]);
    const customers = ref([]);
    const searchQuery = ref('');
    const previewUser = ref(null);
    const mousePosition = ref({ x: 0, y: 0 });

    const filteredUsers = computed(() => {
      const users = activeSection.value === 'servicemen' ? servicemen.value : customers.value;
      if (!searchQuery.value) return users;
      
      const query = searchQuery.value.toLowerCase();
      return users.filter(user => {
        return Object.values(user).some(value => 
          String(value).toLowerCase().includes(query)
        );
      });
    });

    const previewPosition = computed(() => {
      if (!previewUser.value) return {};
      return {
        top: `${mousePosition.value.y + 20}px`,
        left: `${mousePosition.value.x + 20}px`
      };
    });

    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("admin_Token");
        const headers = {
          "Content-Type": "application/json",
          Authorization: token,
        };

        const [servicemanResponse, customerResponse] = await Promise.all([
          axios.get("http://127.0.0.1:5000/users/getServicemen", { headers }),
          axios.get("http://127.0.0.1:5000/users/getCustomers", { headers })
        ]);

        servicemen.value = servicemanResponse.data;
        customers.value = customerResponse.data;
      } catch (error) {
        console.error("Error fetching users:", error);
        // Using native browser alert for simplicity
        alert("Failed to fetch user data. Please try again.");
      }
    };

    const updateApproval = async (user) => {
      try {
        const token = localStorage.getItem("admin_Token");
        await axios.put(
          `http://127.0.0.1:5000/users/update_approval/${user.user_id}`,
          { approval: (!user.approval).toString() },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: token
            },
          }
        );
        await fetchUsers();
      } catch (error) {
        console.error("Error updating approval status:", error);
        alert("Failed to update approval status. Please try again.");
      }
    };

    const showPdfPreview = (user) => {
      window.open(`http://127.0.0.1:5000/users/getpdf/${user.user_id}`, '_blank');
    };

    // Initialize data on component creation
    fetchUsers();

    return {
      activeSection,
      searchQuery,
      filteredUsers,
      previewUser,
      previewPosition,
      updateApproval,
      showPdfPreview
    };
  }
};
</script>

<style scoped>
.management-portal {
  min-height: 100vh;
  background: #3c35f0;
  padding: 2rem;
  position: relative;
}

.portal-header {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.segment-control {
  background: rgba(255, 255, 255, 0.1);
}

.segment-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: white;
  transition: all 0.3s ease;
}

.segment-btn.active {
  background: white;
  color: #1976d2;
}

.search-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.75rem 1rem;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.timeline-container {
  position: relative;
  padding: 2rem 0;
}

.timeline-wrapper {
  position: relative;
}

.timeline-wrapper::before {
  content: '';
  position: absolute;
  left: 2rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: rgba(255, 255, 255, 0.2);
}

.timeline-item {
  position: relative;
  padding-left: 4rem;
  margin-bottom: 2rem;
}

.timeline-marker {
  position: absolute;
  left: 1.5rem;
  top: 2rem;
  width: 1rem;
  height: 1rem;
  background: #1976d2;
  border: 2px solid white;
  border-radius: 50%;
  transform: translateX(-50%);
}

.user-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.user-card-header {
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.pdf-button {
  background: none;
  border: none;
  color: #1976d2;
  font-weight: 500;
  padding: 0;
  transition: color 0.3s ease;
  text-decoration: underline;
}

.pdf-button:hover {
  color: #0d47a1;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 0.5rem;
}

.detail-label {
  color: #757575;
  font-weight: 500;
}

.detail-value {
  color: #303f9f;
}

/* Switch Toggle Styles */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #1976d2;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* Preview Card Styles */
.preview-card {
  position: fixed;
  width: 300px;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  pointer-events: none;
}

.preview-header {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  color: white;
  padding: 1rem;
  border-radius: 1rem 1rem 0 0;
}

.preview-header h4 {
  margin: 0;
  font-size: 1.1rem;
}

.preview-header p {
  margin: 0.5rem 0 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.preview-body {
  padding: 1rem;
  color: #666;
}

/* Transitions */
.timeline-list-enter-active,
.timeline-list-leave-active {
  transition: all 0.5s ease;
}

.timeline-list-enter-from,
.timeline-list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

@media (max-width: 768px) {
  .management-portal {
    padding: 1rem;
  }
  
  .timeline-item {
    padding-left: 3rem;
  }
  
  .timeline-wrapper::before {
    left: 1.5rem;
  }
  
  .timeline-marker {
    left: 1rem;
  }
}
</style>