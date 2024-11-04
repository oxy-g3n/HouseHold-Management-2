<template>
    <div class="profile-portal min-vh-100 d-flex align-items-center justify-content-center py-5">
      <div class="profile-container">
        <!-- Loading State -->
        <div v-if="isLoading" class="text-center">
          <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
  
        <!-- Profile Form -->
        <div v-else class="profile-card bg-white rounded-4 shadow-lg overflow-hidden">
          <header class="profile-header text-center p-4">
            <span class="profile-icon display-4">👤</span>
            <h2 class="profile-title mt-2 text-white mb-0">Update Profile</h2>
          </header>
  
          <main class="profile-content p-4">
            <form @submit.prevent="submitProfileUpdate" class="profile-form">
              <div class="row g-4">
                <!-- Security and Contact Section -->
                <div class="col-md-6">
                  <div class="profile-section">
                    <h3 class="section-title h5 mb-4">Contact Information</h3>
                    
                    <div class="form-floating mb-3">
                      <input 
                        type="email" 
                        class="form-control" 
                        id="floatingEmail" 
                        v-model="profileData.email" 
                        placeholder="Email Address"
                        required
                      >
                      <label for="floatingEmail">Email Address</label>
                    </div>
  
                    <div class="form-floating mb-3">
                      <input 
                        type="tel" 
                        class="form-control" 
                        id="floatingMobile" 
                        v-model="profileData.mobile" 
                        placeholder="Mobile Number"
                        required
                      >
                      <label for="floatingMobile">Mobile Number</label>
                    </div>
  
                    <div class="form-floating">
                      <input 
                        type="password" 
                        class="form-control" 
                        id="floatingPassword" 
                        v-model="profileData.password" 
                        placeholder="New Password (Optional)"
                      >
                      <label for="floatingPassword">New Password (Optional)</label>
                    </div>
                  </div>
                </div>
  
                <!-- Personal and Professional Section -->
                <div class="col-md-6">
                  <div class="profile-section">
                    <h3 class="section-title h5 mb-4">Personal Details</h3>
  
                    <div class="form-floating mb-3">
                      <input 
                        type="text" 
                        class="form-control" 
                        id="floatingFullName" 
                        v-model="profileData.fullName" 
                        placeholder="Full Name"
                        required
                      >
                      <label for="floatingFullName">Full Name</label>
                    </div>
  
                    <div class="form-floating mb-3">
                      <input 
                        type="text" 
                        class="form-control" 
                        id="floatingAddress" 
                        v-model="profileData.address" 
                        placeholder="Address"
                        required
                      >
                      <label for="floatingAddress">Address</label>
                    </div>
  
                    <div class="form-floating">
                      <input 
                        type="text" 
                        class="form-control" 
                        id="floatingPinCode" 
                        v-model="profileData.pinCode" 
                        placeholder="Pin Code"
                        required
                      >
                      <label for="floatingPinCode">Pin Code</label>
                    </div>
                  </div>
                </div>
  
                <!-- Professional Section -->
                <div class="col-12">
                  <div class="profile-section">
                    <h3 class="section-title h5 mb-4">Professional Details</h3>
                    
                    <div class="row g-3">
                      <div class="col-md-6">
                        <div class="form-floating mb-3">
                          <select 
                            class="form-select" 
                            id="floatingService" 
                            v-model="profileData.selectedService"
                            @change="updateSubservices"
                            required
                          >
                            <option value="">Select Service</option>
                            <option 
                              v-for="service in availableServices" 
                              :key="service.service_id" 
                              :value="service"
                            >
                              {{ service.service_info.service_name }}
                            </option>
                          </select>
                          <label for="floatingService">Service</label>
                        </div>
                      </div>
  
                      <div class="col-md-6" v-if="subservices.length">
                        <div class="form-floating mb-3">
                          <select 
                            class="form-select" 
                            id="floatingSubservice" 
                            v-model="profileData.selectedSubservice"
                            required
                          >
                            <option value="">Select Subservice</option>
                            <option 
                              v-for="subservice in subservices" 
                              :key="subservice.subservice_id" 
                              :value="subservice"
                            >
                              {{ subservice.subservice_name }}
                            </option>
                          </select>
                          <label for="floatingSubservice">Subservice</label>
                        </div>
                      </div>
  
                      <div class="col-md-6">
                        <div class="form-floating">
                          <input 
                            type="text" 
                            class="form-control" 
                            id="floatingExperience" 
                            v-model="profileData.experience" 
                            placeholder="Experience"
                            required
                          >
                          <label for="floatingExperience">Experience</label>
                        </div>
                      </div>
  
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="portfolioUpload" class="form-label">Portfolio</label>
                          <input 
                            type="file" 
                            class="form-control" 
                            id="portfolioUpload"
                            @change="handleFileUpload"
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- Action Buttons -->
              <div class="action-buttons mt-4">
                <div class="row g-3">
                  <div class="col-md-6">
                    <button type="submit" class="btn submit-btn w-100">
                      Update Profile
                    </button>
                  </div>
                  <div class="col-md-6">
                    <button type="button" class="btn cancel-btn w-100" @click="cancelUpdate">
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </main>
        </div>
  
        <!-- Notification -->
        <div 
          v-if="notification.message" 
          class="notification-overlay"
          @click="dismissNotification"
        >
          <div 
            class="notification-panel"
            :class="notification.type"
            @click.stop
          >
            {{ notification.message }}
            <button 
              type="button" 
              class="btn-close notification-close" 
              @click="dismissNotification"
              aria-label="Close alert"
            ></button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, reactive, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'ServicemanProfileUpdate',
    setup() {
      const router = useRouter();
      const availableServices = ref([]);
      const subservices = ref([]);
      const isLoading = ref(true);
  
      const profileData = reactive({
        fullName: '',
        email: '',
        mobile: '',
        address: '',
        pinCode: '',
        selectedService: null,
        selectedSubservice: null,
        experience: '',
        password: '',
        portfolioFile: null
      });
  
      const notification = reactive({
        message: '',
        type: ''
      });
  
      const displayNotification = (message, type = 'success') => {
        notification.message = message;
        notification.type = `notification-${type}`;
        setTimeout(() => {
          dismissNotification();
        }, 5000);
      };
  
      const dismissNotification = () => {
        notification.message = '';
        notification.type = '';
      };
  
      const handleFileUpload = (event) => {
        profileData.portfolioFile = event.target.files[0];
      };
  
      const updateSubservices = () => {
        if (profileData.selectedService) {
          subservices.value = profileData.selectedService.subservices;
        } else {
          subservices.value = [];
        }
        profileData.selectedSubservice = null;
      };
  
      const fetchAvailableServices = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:5000/provisions/getProvisions');
          availableServices.value = response.data;
        } catch (error) {
          console.error('Error fetching services:', error);
          displayNotification('Failed to load services', 'error');
        }
      };

      const fetchUserData = async () => {
        try {
          const userId = localStorage.getItem('service_id');
          if (!userId) {
            throw new Error('User ID not found');
          }
  
          const response = await axios.get(`http://127.0.0.1:5000/end_users/getProvider/${userId}`, {
            headers: {
              'Authorization': `${localStorage.getItem('service_Token')}`
            }
          });

          if (response.data && response.data.length > 0) {
            const userData = response.data[0];
            profileData.fullName = userData.full_name;
            profileData.email = userData.mail;
            profileData.mobile = userData.mobile;
            profileData.address = userData.address;
            profileData.pinCode = userData.pin_code;
            profileData.experience = userData.experience;
  
            profileData.selectedService = availableServices.value.find(service => 
              service.service_info.service_name === userData.service
            );
  
            if (profileData.selectedService) {
              updateSubservices();
              profileData.selectedSubservice = subservices.value.find(subservice => 
                subservice.subservice_name === userData.subservice
              );
            }
          }
        } catch (error) {
          console.error('Error fetching user data:', error);
          displayNotification('Failed to load profile data', 'error');
        } finally {
          isLoading.value = false;
        }
      };
  
      const submitProfileUpdate = async () => {
        const formData = new FormData();
        
        if (profileData.password) formData.append('password', profileData.password);
        formData.append('mail', profileData.email);
        formData.append('mobile', profileData.mobile);
        formData.append('full_name', profileData.fullName);
        formData.append('address', profileData.address);
        formData.append('pin_code', profileData.pinCode);
        formData.append('service', profileData.selectedService ? profileData.selectedService.service_info.service_name : '');
        formData.append('subservice', profileData.selectedSubservice ? profileData.selectedSubservice.subservice_name : '');
        formData.append('experience', profileData.experience);
        if (profileData.portfolioFile) formData.append('portfolio', profileData.portfolioFile);
  
        try {
          const response = await axios.put('http://127.0.0.1:5000/end_users/update_user', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': `${localStorage.getItem('service_Token')}`
            }
          });
  
          displayNotification(response.data.message);
        } catch (error) {
          console.error('Update error:', error);
          displayNotification('Profile update failed', 'error');
        }
      };
  
      const cancelUpdate = () => {
        router.push('/Servicedash/requests');
      };
  
      onMounted(async () => {
        await fetchAvailableServices();
        await fetchUserData();
      });
  
      return {
        isLoading,
        profileData,
        availableServices,
        subservices,
        notification,
        handleFileUpload,
        updateSubservices,
        submitProfileUpdate,
        displayNotification,
        dismissNotification,
        cancelUpdate
      };
    }
  };
  </script>
  
  <style scoped>
  .profile-portal {
    background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  }
  
  .profile-container {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    padding: 1rem;
  }
  
  .profile-card {
    background-color: #ffffff;
  }
  
  .profile-header {
    background: linear-gradient(45deg, #303f9f, #1976d2);
  }
  
  .profile-title {
    font-weight: 300;
    font-size: 1.75rem;
    color: #ffffff;
  }
  
  .profile-icon {
    color: #ffffff;
  }
  
  .section-title {
    color: #000000;
    font-weight: 500;
  }
  
  .form-floating > label {
    color: #000000;
  }
  
  .form-floating > .form-control,
  .form-select {
    color: #000000;
  }
  
  .form-floating > .form-control:focus,
  .form-select:focus {
    border-color: #1976d2;
    box-shadow: 0 0 0 0.25rem rgba(25, 118, 210, 0.25);
    color: #000000;
  }
  
  .form-floating > .form-control::placeholder,
  .form-select::placeholder {
    color: #666666;
  }
  
  .submit-btn {
    background: linear-gradient(45deg, #303f9f, #1976d2);
    color: white;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    transition: transform 0.2s;
  }
  
  .submit-btn:hover {
    color: white;
    transform: translateY(-1px);
  }
  
  .cancel-btn {
    background: #f5f5f5;
    color: #000000;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    transition: transform 0.2s;
  }
  
  .cancel-btn:hover {
    background: #e0e0e0;
    transform: translateY(-1px);
    color: #000000;
  }
  
  .notification-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    cursor: pointer;
  }

  .notification-panel {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    max-width: 400px;
    width: 90%;
    position: relative;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    cursor: default;
  }

  .notification-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .notification-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .notification-close {
    position: absolute;
    top: 10px;
    right: 10px;
    opacity: 0.7;
    transition: opacity 0.2s ease;
  }

  .notification-close:hover {
    opacity: 1;
  }
</style>