<template>
    <div class="vh-100 d-flex justify-content-center align-items-center page-colour">
        <div class="container">
            <div class="row">
                <div class="col-md-10 mx-auto">
                    <h2 class="text-center text-white mb-4">Update Serviceman Profile</h2>
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
                                <div class="form-group mb-3">
                                    <label for="fullName">Full Name:</label>
                                    <input type="text" id="fullName" v-model="fullName" class="form-control">
                                </div>
                                <div class="form-group mb-3">
                                    <label for="address">Address:</label>
                                    <input type="text" id="address" v-model="address" class="form-control">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group mb-3">
                                    <label for="pinCode">Pin Code:</label>
                                    <input type="text" id="pinCode" v-model="pinCode" class="form-control">
                                </div>
                                <div class="form-group mb-3">
                                    <label for="service">Service:</label>
                                    <select id="service" v-model="selectedService" @change="updateSubservices" class="form-control">
                                        <option value="">Select a service</option>
                                        <option v-for="service in availableServices" :key="service.service_id" :value="service">
                                            {{ service.service_info.service_name }}
                                        </option>
                                    </select>
                                </div>
                                <div class="form-group mb-3" v-if="subservices.length > 0">
                                    <label for="subservice">Subservice:</label>
                                    <select id="subservice" v-model="selectedSubservice" class="form-control">
                                        <option value="">Select a subservice</option>
                                        <option v-for="subservice in subservices" :key="subservice.subservice_id" :value="subservice">
                                            {{ subservice.subservice_name }}
                                        </option>
                                    </select>
                                </div>
                                <div class="form-group mb-3">
                                    <label for="experience">Experience:</label>
                                    <input type="text" id="experience" v-model="experience" class="form-control">
                                </div>
                                <div class="form-group mb-3">
                                    <label for="portfolio">Portfolio (upload new file to update):</label>
                                    <input type="file" id="portfolio" @change="handleFileUpload" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6 mb-3">
                                <button type="submit" class="btn btn-primary btn-block">
                                    Update Profile
                                </button>
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
            selectedService: null,
            selectedSubservice: null,
            experience: '',
            portfolioFile: null,
            alertMessage: '',
            alertClass: '',
            availableServices: [],
            subservices: [],
            maxPrice: 0,
        };
    },
    setup() {
        const router = useRouter();
        return { router };
    },
    methods: {
        handleFileUpload(event) {
            this.portfolioFile = event.target.files[0];
        },
        updateSubservices() {
            if (this.selectedService) {
                this.subservices = this.selectedService.subservices;
                this.maxPrice = this.selectedService.service_info.max_price;
            } else {
                this.subservices = [];
                this.maxPrice = 0;
            }
            this.selectedSubservice = null;
        },
        async updateProfile() {
            const formData = new FormData();
            if (this.password) formData.append('password', this.password);
            formData.append('mail', this.mail);
            formData.append('mobile', this.mobile);
            formData.append('full_name', this.fullName);
            formData.append('address', this.address);
            formData.append('pin_code', this.pinCode);
            formData.append('service', this.selectedService.service_info.service_name);
            formData.append('subservice', this.selectedSubservice.subservice_name);
            formData.append('experience', this.experience);
            if (this.portfolioFile) formData.append('portfolio', this.portfolioFile);

            try {
                const response = await axios.put('http://127.0.0.1:5000/users/update_profile', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `${localStorage.getItem('service_Token')}`
                    },
                });
                this.showAlert(response.data.message, 'alert-success');
                setTimeout(() => {
                    this.$router.push('/Servicedash/requests');
                }, 2000);
            } catch (error) {
                console.error('Update error:', error);
                this.showAlert('An error occurred during profile update', 'alert-danger');
            }
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
        async fetchUserData() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/users/profile', {
                    headers: {
                        'Authorization': `${localStorage.getItem('service_Token')}`
                    }
                });
                const userData = response.data;
                this.mail = userData.mail;
                this.mobile = userData.mobile;
                this.fullName = userData.full_name;
                this.address = userData.address;
                this.pinCode = userData.pin_code;
                this.experience = userData.experience;

                // Find and set the selected service and subservice
                this.selectedService = this.availableServices.find(service => 
                    service.service_info.service_name === userData.service
                );
                this.updateSubservices();
                this.selectedSubservice = this.subservices.find(subservice => 
                    subservice.subservice_name === userData.subservice
                );
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        }
    },
    mounted() {
        this.fetchAvailableServices().then(() => {
            this.fetchUserData();
        });
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