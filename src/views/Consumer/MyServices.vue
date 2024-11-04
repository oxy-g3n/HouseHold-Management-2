<template>
  <section class="service-dashboard p-4">
    <div class="dashboard-header mb-4 rounded-3">
      <h1 class="dashboard-title text-gradient pt-2">Service Request Dashboard</h1>
      <p class="dashboard-subtitle pb-2" v-if="requests.length > 0">
        Managing {{ requests.length }} Active Requests
      </p>
    </div>

    <div v-if="loading" class="loader-container">
      <div class="spinner-grow text-primary" role="status">
        <span class="visually-hidden">Loading requests...</span>
      </div>
    </div>

    <div v-else-if="requests.length === 0" class="empty-state">
      <div class="empty-state-content">
        <i class="bi bi-clipboard-check display-1"></i>
        <h2>No Active Requests</h2>
        <p>You currently don't have any pending service requests.</p>
      </div>
    </div>

    <div v-else class="request-grid">
      <div v-for="request in requests" 
           :key="request.serviceRequest_id" 
           class="request-tile">
        <div class="request-card">
          <div class="request-header">
            <span class="request-id">Request #{{ request.serviceRequest_id }}</span>
            <span :class="['status-badge', `status-${request.status}`]">
              {{ request.status }}
            </span>
          </div>

          <div class="request-body">
            <div class="info-group">
              <i class="bi bi-person-circle"></i>
              <div class="info-content">
                <label>Serviceman</label>
                <span>{{ request.serviceman_name }}</span>
              </div>
            </div>

            <div class="info-group">
              <i class="bi bi-tools"></i>
              <div class="info-content">
                <label>Service Type</label>
                <span>{{ request.service }}</span>
              </div>
            </div>

            <div class="info-group">
              <i class="bi bi-calendar3"></i>
              <div class="info-content">
                <label>Requested On</label>
                <span>{{ request.request_begin_date }}</span>
              </div>
            </div>
          </div>

          <div class="request-actions">
            <button 
              @click="withdrawRequest(request.serviceRequest_id)"
              class="action-btn withdraw-btn"
              :disabled="request.status === 'active'"
              :aria-label="'Withdraw request ' + request.serviceRequest_id"
            >
              <i class="bi bi-x-circle"></i>
              Withdraw
            </button>
            <button 
              @click="openCompletionModal(request.serviceRequest_id)"
              class="action-btn complete-btn"
              :disabled="request.status === 'requested'"
              :aria-label="'Mark completed request ' + request.serviceRequest_id"
            >
              <i class="bi bi-check-circle"></i>
              Complete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Rating Modal -->
    <div v-if="showCompletionModal" 
         class="modal-overlay"
         @click="closeCompletionModal">
      <div class="rating-modal" @click.stop>
        <div class="modal-header">
          <h3>Rate Your Service Experience</h3>
          <button class="close-btn" @click="closeCompletionModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="rating-scale">
            <label for="rating-input">Your Rating (1-10)</label>
            <div class="rating-input-group">
              <input 
                v-model.number="rating"
                type="range"
                min="1"
                max="10"
                class="rating-slider"
                id="rating-input"
              >
              <span class="rating-value">{{ rating }}</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button 
            @click="closeCompletionModal" 
            class="cancel-btn"
          >
            Cancel
          </button>
          <button 
            @click="submitCompletion"
            class="submit-btn"
          >
            Submit Rating
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ServiceRequestsDashboard',
  
  data() {
    return {
      requests: [],
      loading: true,
      showCompletionModal: false,
      selectedRequestId: null,
      rating: 5,
    };
  },

  methods: {
    async fetchRequests() {
      this.loading = true;
      try {
        const customerId = localStorage.getItem("cust_id");
        const token = localStorage.getItem("cust_Token");
        
        const response = await axios.get(
          `http://127.0.0.1:5000/provision_requests/get_consumer_requests/${customerId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );

        this.requests = response.data.filter(request => 
          ["open", "requested", "active"].includes(request.status)
        );
      } catch (error) {
        console.error("Failed to fetch requests:", error);
      } finally {
        this.loading = false;
      }
    },

    async updateRequest(serviceRequestId, status, rating = null) {
      try {
        const token = localStorage.getItem("cust_Token");
        const payload = { serviceRequest_id: serviceRequestId, status };
        
        if (rating !== null) {
          payload.rating = rating;
        }

        const response = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/provision_requests/edit_request",
          data: payload,
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token}`,
          },
        });

        this.showNotification(response.data);
        await this.fetchRequests();
      } catch (error) {
        console.error("Update failed:", error);
        this.showNotification("Failed to update request. Please try again.", "error");
      }
    },

    withdrawRequest(serviceRequestId) {
      if (confirm("Are you sure you want to withdraw this service request?")) {
        this.updateRequest(serviceRequestId, "withdrawn");
      }
    },

    openCompletionModal(serviceRequestId) {
      this.selectedRequestId = serviceRequestId;
      this.showCompletionModal = true;
      document.body.style.overflow = 'hidden';
    },

    closeCompletionModal() {
      this.showCompletionModal = false;
      this.selectedRequestId = null;
      this.rating = 5;
      document.body.style.overflow = 'auto';
    },

    submitCompletion() {
      if (this.rating < 1 || this.rating > 10) {
        this.showNotification("Please enter a valid rating between 1 and 10.", "error");
        return;
      }
      
      this.updateRequest(this.selectedRequestId, "completed", this.rating);
      this.closeCompletionModal();
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },

    showNotification(message, type = 'success') {
      // Implement your notification system here
      alert(message);
    }
  },

  created() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.service-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.dashboard-header {
  text-align: center;
  background-color: #1e40af;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 300;
  background: #ffffff;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
  font-weight: 600;
  
}

.dashboard-subtitle {
  color: #ffffff;
  font-size: 1.1rem;
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
}

.empty-state-content {
  color: #6c757d;
}

.request-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.request-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

.request-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
}

.request-header {
  padding: 1rem;
  background: linear-gradient(45deg, #f8f9fa, #e9ecef);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.request-id {
  font-weight: 500;
  color: #495057;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-open { background: #e3f2fd; color: #1976d2; }
.status-requested { background: #fff3e0; color: #f57c00; }
.status-active { background: #e8f5e9; color: #2e7d32; }

.request-body {
  padding: 1rem;
}

.info-group {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 0.75rem;
}

.info-group i {
  color: #1976d2;
  font-size: 1.25rem;
}

.info-content {
  display: flex;
  flex-direction: column;
}

.info-content label {
  font-size: 0.75rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.info-content span {
  color: #212529;
  font-weight: 500;
}

.request-actions {
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  border-top: 1px solid #e9ecef;
}

.action-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: opacity 0.2s;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.withdraw-btn {
  background: #fff3e0;
  color: #f57c00;
}

.complete-btn {
  background: #e8f5e9;
  color: #2e7d32;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.rating-modal {
  background: white;
  border-radius: 1rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 1rem 2rem rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #212529;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  color: #6c757d;
  font-size: 1.25rem;
  padding: 0.25rem;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.rating-scale {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rating-input-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-slider {
  flex: 1;
  height: 2px;
  -webkit-appearance: none;
  background: #e9ecef;
  outline: none;
  transition: background 0.2s;
}

.rating-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #1976d2;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.1s;
}

.rating-slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.rating-value {
  min-width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 50%;
  font-weight: 500;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.modal-footer button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}

.cancel-btn {
  background: #f8f9fa;
  color: #6c757d;
  transition: background-color 0.2s;
}

.cancel-btn:hover {
  background: #e9ecef;
}

.submit-btn {
  background: #1976d2;
  color: white;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background: #1565c0;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .dashboard-title {
    font-size: 2rem;
  }

  .request-grid {
    grid-template-columns: 1fr;
    padding: 0.5rem;
  }

  .rating-modal {
    width: 95%;
    margin: 1rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .modal-footer {
    padding: 1rem;
    flex-direction: column;
  }

  .modal-footer button {
    width: 100%;
  }

  .action-btn {
    padding: 0.5rem;
    font-size: 0.875rem;
  }

  .info-group {
    margin-bottom: 0.75rem;
  }
}

/* Accessibility Improvements */
@media (prefers-reduced-motion: reduce) {
  .request-card,
  .rating-slider::-webkit-slider-thumb,
  .action-btn,
  .submit-btn,
  .cancel-btn {
    transition: none;
  }
}

/* High Contrast Mode Support */
@media (forced-colors: active) {
  .status-badge,
  .action-btn,
  .submit-btn,
  .cancel-btn {
    border: 1px solid currentColor;
  }

  .rating-slider::-webkit-slider-thumb {
    border: 2px solid currentColor;
  }
}
</style>