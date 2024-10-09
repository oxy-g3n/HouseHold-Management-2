<template>
  <div class="vh-100 d-flex justify-content-center align-items-center page-colour">
    <div v-if="isLoading" class="text-white">Loading...</div>

    <div v-else class="container">
      <div class="row">
        <div class="col-md-10 mx-auto">
          <h2 class="text-center text-white mb-4">Update Customer Profile</h2>
          <form @submit.prevent="updateProfile" class="form-container border p-4 border-primary rounded">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group mb-3">
                  <label for="password">New Password (leave blank to keep current):</label>
                  <input type="password" id="password" v-model="password" class="form-control">
                </div>
                <div class="form-group mb-3">
                  <label for="email">Email:</label>
                  <input type="email" id="email" v-model="mail" class="form-control">
                </div>
                <div class="form-group mb-3">
                  <label for="mobile">Mobile:</label>
                  <input type="text" id="mobile" v-model="mobile" class="form-control">
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group mb-3">
                  <label for="fullName">Full Name:</label>
                  <input type="text" id="fullName" v-model="fullName" class="form-control">
                </div>
                <div class="form-group mb-3">
                  <label for="address">Address:</label>
                  <input type="text" id="address" v-model="address" class="form-control">
                </div>
                <div class="form-group mb-3">
                  <label for="pinCode">Pin Code:</label>
                  <input type="text" id="pinCode" v-model="pinCode" class="form-control">
                </div>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-md-6 mb-3">
                <button type="submit" class="btn btn-primary btn-block">Update Profile</button>
              </div>
              <div class="col-md-6">
                <button type="button" class="btn btn-secondary btn-block" @click="cancel">Cancel</button>
              </div>
            </div>
          </form>
          <div v-if="alertMessage" class="alert-overlay d-flex justify-content-center align-items-center">
            <div class="alert" :class="alertClass" role="alert">
              {{ alertMessage }}
              <button type="button" class="btn-close" @click="alertMessage = ''" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      password: '',
      mail: '',
      mobile: '',
      fullName: '',
      address: '',
      pinCode: '',
      alertMessage: '',
      alertClass: '',
      isLoading: true,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async fetchUserData() {
      try {
        const customerId = localStorage.getItem('cust_id');
        const response = await axios.get(`http://127.0.0.1:5000/users/getCustomer/${customerId}`, {
          headers: {
            'Authorization': `${localStorage.getItem('cust_Token')}`,
          },
        });
        const customerData = response.data;
        console.log("bruh");
        console.log(customerData);
        // Populate form fields with fetched data
        this.mail = customerData[0].mail;
        this.mobile = customerData[0].mobile;
        this.fullName = customerData[0].full_name;
        this.address = customerData[0].address;
        this.pinCode = customerData[0].pin_code;

        console.log('Fetched customer data:', customerData); // For debugging
      } catch (error) {
        console.error("Error fetching customer data:", error);
        this.showAlert("Unable to fetch customer data", "alert-danger");
      } finally {
        this.isLoading = false;
      }
    },

    async updateProfile() {
      const formData = new FormData();
      if (this.password) formData.append('password', this.password);
      formData.append('mail', this.mail);
      formData.append('mobile', this.mobile);
      formData.append('full_name', this.fullName);
      formData.append('address', this.address);
      formData.append('pin_code', this.pinCode);

      try {
        const response = await axios.put('http://127.0.0.1:5000/users/update_profile', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `${localStorage.getItem('cust_Token')}`
          },
        });
        this.showAlert(response.data.message, 'alert-success');
      } catch (error) {
        console.error('Update error:', error);
        this.showAlert('An error occurred during profile update', 'alert-danger');
      }
    },
    cancel() {
      this.router.push('/Custdash/SearchServices');
    },
    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = `alert ${alertClass} alert-dismissible fade show`;
      setTimeout(() => {
        this.alertMessage = '';
      }, 5000);
    },
  },
  mounted() {
    this.fetchUserData();
  }
};
</script>

<style scoped>
.vh-100 {
  height: 100vh;
}

.d-flex {
  display: flex;
}

.justify-content-center {
  justify-content: center;
}

.align-items-center {
  align-items: center;
}

.container {
  max-width: auto;
  padding: 20px;
}

.form-container {
  background-color: #2c3e50;
  color: white;
}

.border {
  border: 1px solid #007bff;
}

.p-4 {
  padding: 1.5rem !important;
}

.mb-3 {
  margin-bottom: 1rem !important;
}

.btn-block {
  display: block;
  width: 100%;
}

.mx-auto {
  margin-left: auto !important;
  margin-right: auto !important;
}

.text-center {
  text-align: center !important;
}

.page-colour {  
  background-color:#1e2a3a;
}

.alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}

.btn-close {
  background: none;
  border: none;
}
</style>