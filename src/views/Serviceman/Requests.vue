<template>
  <div class="serviceman-requests-container">
    <h2>Service Requests</h2>
    <div v-if="loading" class="loading" aria-live="polite">Loading requests...</div>
    <div v-else-if="requests.length === 0" class="no-requests" aria-live="polite">No pending requests available.</div>
    <div v-else class="table-container">
      <table class="requests-table">
        <thead>
          <tr>
            <th scope="col">Request ID</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Service</th>
            <th scope="col">Address</th>
            <th scope="col">Status</th>
            <th scope="col">Request Date</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.serviceRequest_id">
            <td>{{ request.serviceRequest_id }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ request.service }}</td>
            <td>{{ request.customer_address }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.request_begin_date }}</td>
            <td>
              <button @click="updateRequest(request.serviceRequest_id, 'active')" class="btn btn-primary mr-2">
                Accept
              </button>
              <button @click="updateRequest(request.serviceRequest_id, 'rejected')" class="btn btn-danger">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
    };
  },
  methods: {
    async fetchRequests() {
      this.loading = true;
      try {
        const servicemanId = localStorage.getItem("service_id");
        const token = localStorage.getItem("service_Token");
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/listServices/${servicemanId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.requests = response.data.filter(request => request.status === "requested");
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },
    async updateRequest(serviceRequestId, status) {
      try {
        const token = localStorage.getItem("service_Token");
        const response = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/requests/editRequest",
          data: {
            serviceRequest_id: serviceRequestId,
            status: status,
          },
          headers: {
            "Content-Type": "application/json",
            "Authorization": `${token}`,
          },
          withCredentials: false,
        });
        alert(response.data);
        await this.fetchRequests();
      } catch (error) {
        console.error("Error updating service request:", error);
        if (error.response) {
          console.error("Response data:", error.response.data);
          console.error("Response status:", error.response.status);
          console.error("Response headers:", error.response.headers);
        } else if (error.request) {
          console.error("No response received:", error.request);
        } else {
          console.error("Error setting up request:", error.message);
        }
        alert("Failed to update service request. Please check the console for more details.");
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },
  },
  created() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
.serviceman-requests-container {
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

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.mr-2 {
  margin-right: 8px;
}
</style>