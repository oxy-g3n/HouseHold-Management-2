<template>
  <main class="dashboard-wrapper py-4">
    <header class="dashboard-header mb-4 text-center rounded-3 p-3">
      <h1 class="header-title">Service Management Portal</h1>
      <p class="header-subtitle" v-if="pendingTasks.length">
        Currently Processing {{ pendingTasks.length }} Service Tasks
      </p>
    </header>

    <div v-if="isDataLoading" class="loading-indicator">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Retrieving service tasks...</span>
      </div>
    </div>

    <div v-else-if="pendingTasks.length === 0" class="empty-dashboard">
      <div class="text-center p-5 bg-white rounded-3 shadow-sm">
        <i class="bi bi-clipboard-x display-1 text-muted"></i>
        <h2 class="mt-3">Queue Empty</h2>
        <p class="text-muted">Your service queue is currently empty.</p>
      </div>
    </div>

    <div v-else class="task-grid">
      <article v-for="task in pendingTasks" 
               :key="task.serviceRequest_id" 
               class="task-card">
        <header class="task-header">
          <span class="task-identifier">Task #{{ task.serviceRequest_id }}</span>
          <span class="task-status">{{ task.status }}</span>
        </header>

        <div class="task-details">
          <div class="info-row">
            <i class="bi bi-person"></i>
            <div>
              <small class="text-muted">Client</small>
              <p class="mb-0 text-black">{{ task.customer_name }}</p>
            </div>
          </div>

          <div class="info-row">
            <i class="bi bi-gear"></i>
            <div>
              <small class="text-muted">Service Type</small>
              <p class="mb-0 text-black">{{ task.service }}</p>
            </div>
          </div>

          <div class="info-row">
            <i class="bi bi-geo-alt"></i>
            <div>
              <small class="text-muted">Location</small>
              <p class="mb-0 text-black">{{ task.customer_address }}</p>
            </div>
          </div>

          <div class="info-row">
            <i class="bi bi-calendar3"></i>
            <div>
              <small class="text-muted">Requested</small>
              <p class="mb-0 text-black">{{ task.request_begin_date }}</p>
            </div>
          </div>
        </div>

        <footer class="task-actions">
          <button @click="processTask(task.serviceRequest_id, 'active')"
                  class="btn accept-btn">
            <i class="bi bi-check-circle me-2"></i>Accept
          </button>
          <button @click="processTask(task.serviceRequest_id, 'rejected')"
                  class="btn decline-btn">
            <i class="bi bi-x-circle me-2"></i>Decline
          </button>
        </footer>
      </article>
    </div>
  </main>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ServiceTaskDashboard',
  
  data() {
    return {
      pendingTasks: [],
      isDataLoading: true,
    };
  },

  methods: {
    formatRequestDate(dateString) {
      if (!dateString) return 'Not specified';
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      };
      return new Date(dateString).toLocaleDateString('en-US', options);
    },

    async retrieveTasks() {
      this.isDataLoading = true;
      try {
        const technician = localStorage.getItem("service_id");
        const authKey = localStorage.getItem("service_Token");
        
        const response = await axios.get(
          `http://127.0.0.1:5000/requests/listServices/${technician}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: authKey,
            },
          }
        );
        
        this.pendingTasks = response.data.filter(task => 
          task.status === "requested"
        );
      } catch (err) {
        console.error("Failed to fetch tasks:", err);
      } finally {
        this.isDataLoading = false;
      }
    },

    async processTask(taskId, newStatus) {
      try {
        const authKey = localStorage.getItem("service_Token");
        const result = await axios({
          method: 'PUT',
          url: "http://127.0.0.1:5000/requests/editRequest",
          data: {
            serviceRequest_id: taskId,
            status: newStatus,
          },
          headers: {
            "Content-Type": "application/json",
            Authorization: authKey,
          },
        });
        
        await this.showNotification(result.data);
        await this.retrieveTasks();
      } catch (err) {
        console.error("Task processing failed:", err);
        this.showNotification("Operation failed. Please try again.");
      }
    },

    showNotification(message) {
      return new Promise(resolve => {
        alert(message);
        resolve();
      });
    }
  },

  mounted() {
    this.retrieveTasks();
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 0 1.5rem;
}

.dashboard-header {
  background-color: #1e40af;
  padding: 2rem 1rem;
}

.header-title {
  color: white;
  font-size: 2.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.header-subtitle {
  color: #e2e8f0;
  font-size: 1.1rem;
  margin-bottom: 0;
}

.loading-indicator {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.task-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.2s ease;
}

.task-card:hover {
  transform: translateY(-4px);
}

.task-header {
  padding: 1rem;
  background: linear-gradient(45deg, #f8f9fa, #e9ecef);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-identifier {
  font-weight: 600;
  color: #1e40af;
}

.task-status {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.task-details {
  padding: 1.25rem;
}

.info-row {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-row i {
  color: #1e40af;
  font-size: 1.25rem;
  margin-top: 0.25rem;
}

.task-actions {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  border-top: 1px solid #e9ecef;
}

.accept-btn {
  flex: 1;
  background: #e8f5e9;
  color: #2e7d32;
  border: none;
  transition: background-color 0.2s;
}

.accept-btn:hover {
  background: #c8e6c9;
}

.decline-btn {
  flex: 1;
  background: #ffebee;
  color: #c62828;
  border: none;
  transition: background-color 0.2s;
}

.decline-btn:hover {
  background: #ffcdd2;
}

@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 0 1rem;
  }

  .header-title {
    font-size: 1.75rem;
  }

  .task-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .task-actions {
    flex-direction: column;
  }
}

@media (prefers-reduced-motion: reduce) {
  .task-card {
    transition: none;
  }
}
</style>