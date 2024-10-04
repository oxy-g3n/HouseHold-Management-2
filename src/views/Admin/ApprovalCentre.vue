<template>
  <div class="user-table-container">
    <h3>User Management Table</h3>
    <div class="button-group">
      <button @click="activeTable = 'servicemen'" :class="{ active: activeTable === 'servicemen' }">Servicemen</button>
      <button @click="activeTable = 'customers'" :class="{ active: activeTable === 'customers' }">Customers</button>
    </div>
    <table class="user-table">
      <thead>
        <tr v-if="activeTable === 'servicemen'">
          <th @click="sortTable('user_id')">User ID <span :class="getSortClass('user_id')"></span></th>
          <th @click="sortTable('full_name')">Full Name <span :class="getSortClass('full_name')"></span></th>
          <!-- <th @click="sortTable('mail')">Email <span :class="getSortClass('mail')"></span></th>
          <th @click="sortTable('mobile')">Mobile <span :class="getSortClass('mobile')"></span></th> -->
          <th @click="sortTable('service')">Service <span :class="getSortClass('service')"></span></th>
          <th @click="sortTable('Rating')">Rating <span :class="getSortClass('Rating')"></span></th>
          <th @click="sortTable('experience')">Experience <span :class="getSortClass('experience')"></span></th>
          <th @click="sortTable('pin_code')">Pin Code <span :class="getSortClass('pin_code')"></span></th>
          <th @click="sortTable('approval')">Approval Status <span :class="getSortClass('approval')"></span></th>
        </tr>
        <tr v-else>
          <th @click="sortTable('user_id')">User ID <span :class="getSortClass('user_id')"></span></th>
          <th @click="sortTable('full_name')">Full Name <span :class="getSortClass('full_name')"></span></th>
          <th @click="sortTable('mail')">Email <span :class="getSortClass('mail')"></span></th>
          <th @click="sortTable('mobile')">Mobile <span :class="getSortClass('mobile')"></span></th>
          <th @click="sortTable('pin_code')">Pin Code <span :class="getSortClass('pin_code')"></span></th>
          <th @click="sortTable('approval')">Approval Status <span :class="getSortClass('approval')"></span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in sortedUsers" :key="user.user_id">
          <td>{{ user.user_id }}</td>
          <td>
            <a v-if="activeTable === 'servicemen'" :href="getPdfUrl(user.user_id)" target="_blank">{{ user.full_name }}</a>
            <span v-else>{{ user.full_name }}</span>
          </td>
          <td v-if="activeTable != 'servicemen'">{{ user.mail }}</td>
          <td v-if="activeTable != 'servicemen'">{{ user.mobile }}</td>
          <td v-if="activeTable === 'servicemen'">{{ user.service }}</td>
          <td v-if="activeTable === 'servicemen'">{{ user.Rating !== null ? user.Rating : 'N/A' }}</td>
          <td v-if="activeTable === 'servicemen'">{{ user.experience }} years</td>
          <td>{{ user.pin_code }}</td>
          <td>
            {{ user.approval ? 'Approved' : 'Not Approved' }}
            <button @click="updateApproval(user)" class="btn btn-secondary btn-sm ml-2">
              {{ user.approval ? 'Revoke' : 'Approve' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      servicemen: [],
      customers: [],
      activeTable: 'servicemen',
      sortKey: '',
      sortAsc: true
    };
  },
  computed: {
    sortedUsers() {
      const users = this.activeTable === 'servicemen' ? this.servicemen : this.customers;
      return users.slice().sort((a, b) => {
        const modifier = this.sortAsc ? 1 : -1;
        if (a[this.sortKey] < b[this.sortKey]) return -1 * modifier;
        if (a[this.sortKey] > b[this.sortKey]) return 1 * modifier;
        return 0;
      });
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("admin_Token");
        const servicemanResponse = await axios.get(
          "http://127.0.0.1:5000/users/getServicemen",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.servicemen = servicemanResponse.data;

        const customerResponse = await axios.get(
          "http://127.0.0.1:5000/users/getCustomers",
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`,
            },
          }
        );
        this.customers = customerResponse.data;
      } catch (error) {
        console.error("Error fetching users:", error);
        alert("Failed to fetch user data. Please try again.");
      }
    },
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },
    getSortClass(key) {
      if (this.sortKey === key) {
        return this.sortAsc ? 'asc' : 'desc';
      }
      return '';
    },
    getPdfUrl(servicemanId) {
      return `http://127.0.0.1:5000/users/getpdf/${servicemanId}`;
    },
    async updateApproval(user) {
      try {
        const token = localStorage.getItem("admin_Token");
        const response = await axios.put(
          `http://127.0.0.1:5000/users/update_approval/${user.user_id}`,
          { approval: (!user.approval).toString() },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `${token}`
            },
          }
        );
        if (response.status === 200) {
          await this.fetchUsers();  // Reload the table
          alert("Approval status updated successfully");
        }
      } catch (error) {
        console.error("Error updating approval status:", error);
        alert("Failed to update approval status. Please try again.");
      }
    }
  },
  created() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.user-table-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #2c3e50;
  border-radius: 5px;
}

.button-group {
  margin-bottom: 10px;
}

.button-group button {
  padding: 10px 20px;
  margin-right: 10px;
  background-color: #34495e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.button-group button.active {
  background-color: #3498db;
}

.user-table {
  width: 100%;
  background-color: #34495e;
  border-radius: 5px;
  border-collapse: collapse;
  color: white;
}

.user-table th,
.user-table td {
  border: 1px solid #4a6278;
  padding: 10px;
  text-align: left;
}

.user-table th {
  background-color: #2c3e50;
  cursor: pointer;
}

.user-table td {
  background-color: #34495e;
}

.asc::after {
  content: ' ▲';
}

.desc::after {
  content: ' ▼';
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.btn-secondary {
  background-color: #7f8c8d;
  border-color: #7f8c8d;
}

.btn-secondary:hover {
  background-color: #95a5a6;
  border-color: #95a5a6;
}
</style>