<template>
  <div class="customer-requests-container">
    <h2>My Service Requests</h2>
    <div v-if="loading" class="loading">Loading requests...</div>
    <div v-else-if="requests.length === 0" class="no-requests">No pending requests available.</div>
    <div v-else class="table-container">
      <table class="requests-table">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Serviceman Name</th>
            <th>Serviceman ID</th>
            <th>Service</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.serviceRequest_id">
            <td>{{ request.serviceRequest_id }}</td>
            <td>{{ request.serviceman_name }}</td>
            <td>{{ request.serviceman_id }}</td>
            <td>{{ request.service }}</td>
            <td>{{ request.status }}</td>
            <td>
              <button 
                @click="withdrawRequest(request.serviceRequest_id)" 
                class="btn btn-warning mr-2"
                :disabled="request.status === 'active'"
              >
                Withdraw
              </button>
              <button 
                @click="openCompletionModal(request.serviceRequest_id)" 
                class="btn btn-success"
                :disabled="request.status === 'requested'"
              >
                Mark Completed
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Completion Modal -->
    <div v-if="showCompletionModal" class="modal">
      <div class="modal-content">
        <h3>Rate the Service</h3>
        <p>Please rate the service from 1 to 10:</p>
        <input v-model.number="rating" type="number" min="1" max="10" class="rating-input">
        <button @click="submitCompletion" class="btn btn-primary">Submit</button>
        <button @click="closeCompletionModal" class="btn btn-secondary">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
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
          `http://127.0.0.1:5000/requests/listMyServices/${customerId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.requests = response.data.filter(request => 
          request.status === "open" || request.status === "requested" || request.status === "active"
        );
      } catch (error) {
        console.error("Error fetching service requests:", error);

      } finally {
        this.loading = false;
      }
    },
    async updateRequest(serviceRequestId, status, rating = null) {
      try {
        const token = localStorage.getItem("cust_Token");
        const data = {
          serviceRequest_id: serviceRequestId,
          status: status,
        };
        if (rating !== null) {
          data.rating = rating;
        }
        const response = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/requests/editRequest",
          data: data,
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token}`,
          },
        });
        alert(response.data);
        await this.fetchRequests();
      } catch (error) {
        console.error("Error updating service request:", error);
        alert("Failed to update service request. Please try again.");
      }
    },
    withdrawRequest(serviceRequestId) {
      if (confirm("Are you sure you want to withdraw this request?")) {
        this.updateRequest(serviceRequestId, "withdrawn");
      }
    },
    openCompletionModal(serviceRequestId) {
      this.selectedRequestId = serviceRequestId;
      this.showCompletionModal = true;
    },
    closeCompletionModal() {
      this.showCompletionModal = false;
      this.selectedRequestId = null;
      this.rating = 5;
    },
    submitCompletion() {
      if (this.rating < 1 || this.rating > 10) {
        alert("Please enter a rating between 1 and 10.");
        return;
      }
      this.updateRequest(this.selectedRequestId, "completed", this.rating);
      this.closeCompletionModal();
    },
  },
  created() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.customer-requests-container {
  font-family: Arial, sans-serif;
  background-color: #1e2a3a;
  color: white;
  padding: 20px;
  min-height: 100vh;
}

h2 {
  color: white;
  margin-bottom: 20px;
}

.loading, .no-requests {
  text-align: center;
  padding: 20px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.table-container {
  background-color: #2c3e50;
  border-radius: 5px;
  overflow-x: auto;
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
}

.requests-table tr:nth-child(even) {
  background-color: #3a536b;
}

.requests-table tr:hover {
  background-color: #4a6278;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-warning {
  background-color: #f39c12;
  color: white;
}

.btn-warning:hover:not(:disabled) {
  background-color: #e67e22;
}

.btn-success {
  background-color: #2ecc71;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #27ae60;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.mr-2 {
  margin-right: 8px;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.rating-input {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border: 1px solid #4a6278;
  border-radius: 4px;
  background-color: #34495e;
  color: white;
}
</style>