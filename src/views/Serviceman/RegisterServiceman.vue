<template>
  <div class="vh-100 d-flex justify-content-center align-items-center page-colour">
    <div class="container">
      <div class="row">
        <div class="col-md-10 mx-auto">
          <h2 class="text-center text-white mb-4">Serviceman Registration</h2>
          <form @submit.prevent="registerUser" class="form-container border p-4 border-primary rounded">
            <div class="row">
              <div class="col-md-6">
                <div class="form-group mb-3">
                  <label for="username">Username:</label>
                  <input type="text" id="username" v-model="username" class="form-control" maxlength="30" required>
                </div>
                <div class="form-group mb-3">
                  <label for="password">Password:</label>
                  <input type="password" id="password" v-model="password" class="form-control" minlength="8" required>
                </div>
                <div class="form-group mb-3">
                  <label for="email">Email:</label>
                  <input type="email" id="email" v-model="mail" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                  <label for="mobile">Mobile:</label>
                  <input type="text" id="mobile" v-model="mobile" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                  <label for="fullName">Full Name:</label>
                  <input type="text" id="fullName" v-model="fullName" class="form-control" maxlength="60" required>
                </div>
                <div class="form-group mb-3">
                  <label for="address">Address:</label>
                  <textarea id="address" v-model="address" class="form-control" maxlength="500" required></textarea>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group mb-3">
                  <label for="pinCode">Pin Code:</label>
                  <input type="text" id="pinCode" v-model="pinCode" class="form-control" maxlength="6" pattern="[0-9]*" required>
                </div>
                <div class="form-group mb-3">
                  <label for="service">Service:</label>
                  <select id="service" v-model="selectedService" @change="updateSubservices" class="form-control" required>
                    <option value="">Select a service</option>
                    <option v-for="service in availableServices" :key="service.service_id" :value="service">
                      {{ service.service_info.service_name }}
                    </option>
                  </select>
                </div>
                <div class="form-group mb-3" v-if="subservices.length > 0">
                  <label for="subservice">Subservice:</label>
                  <select id="subservice" v-model="selectedSubservice" class="form-control" required>
                    <option value="">Select a subservice</option>
                    <option v-for="subservice in subservices" :key="subservice.subservice_id" :value="subservice">
                      {{ subservice.subservice_name }}
                    </option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label for="experience">Experience (in years):</label>
                  <input type="number" id="experience" v-model="experience" class="form-control" min="0" required>
                </div>
                <div class="form-group mb-3">
                  <label for="portfolio">Portfolio:</label>
                  <input type="file" id="portfolio" @change="handleFileUpload" class="form-control" required>
                </div>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-md-6 mb-3">
                <button type="submit" class="btn btn-primary btn-block" :disabled="!isFormValid">Register</button>
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
      username: '',
      password: '',
      mail: '',
      mobile: '',
      fullName: '',
      address: '',
      pinCode: '',
      selectedService: null,
      selectedSubservice: null,
      experience: '',
      portfolioFile: null,
      alertMessage: '',
      alertClass: '',
      availableServices: [],
      subservices: [],
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  computed: {
    isFormValid() {
      return this.username && this.password && this.mail && this.mobile && this.fullName && 
             this.address && this.pinCode && this.selectedService && this.selectedSubservice && 
             this.experience && this.portfolioFile;
    }
  },
  methods: {
    handleFileUpload(event) {
      this.portfolioFile = event.target.files[0];
    },
    async registerUser() {
      if (!this.isFormValid) {
        this.showAlert('Please fill in all required fields', 'alert-danger');
        return;
      }

      const formData = new FormData();
      formData.append('action', 'service_reg');
      formData.append('username', this.username);
      formData.append('password', this.password);
      formData.append('mail', this.mail);
      formData.append('mobile', this.mobile);
      formData.append('full_name', this.fullName);
      formData.append('address', this.address);
      formData.append('pin_code', this.pinCode);
      formData.append('service', this.selectedService.service_info.service_name);
      formData.append('subservice', this.selectedSubservice.subservice_name);
      formData.append('experience', this.experience);
      formData.append('portfolio', this.portfolioFile);
      
      try {
        const response = await axios.post('http://127.0.0.1:5000/users/register', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.showAlert(response.data, 'alert-success');
        
        setTimeout(() => {
          this.$router.push('/');
        }, 2000);  // 2000 milliseconds = 2 seconds

      } catch (error) {
        console.error('Registration error:', error);
        this.showAlert('An error occurred during registration', 'alert-danger');
      }
    },
    cancel() {
      this.$router.push('/');
    },
    showAlert(message, alertClass) {
      this.alertMessage = message;
      this.alertClass = `alert ${alertClass} alert-dismissible fade show`;
      setTimeout(() => {
        this.alertMessage = '';
      }, 5000);
    },
    async fetchAvailableServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/services/listServices');
        this.availableServices = response.data;
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    updateSubservices() {
      if (this.selectedService) {
        this.subservices = this.selectedService.subservices;
      } else {
        this.subservices = [];
      }
      this.selectedSubservice = null;
    },
  },
  mounted() {
    this.fetchAvailableServices();
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