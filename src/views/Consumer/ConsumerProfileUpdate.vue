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
          <h2 class="profile-title mt-2 text-white mb-0">Personal Information</h2>
        </header>

        <main class="profile-content p-4">
          <form @submit.prevent="submitProfileUpdate" class="profile-form">
            <div class="row g-4">
              <!-- Security Section -->
              <div class="col-md-6">
                <div class="profile-section">
                  <h3 class="section-title h5 mb-4">Security Details</h3>
                  
                  <div class="form-floating mb-3">
                    <input
                      type="password"
                      class="form-control"
                      id="securityPassword"
                      v-model="formData.password"
                      placeholder="Leave blank to keep current"
                    >
                    <label for="securityPassword">New Password</label>
                  </div>

                  <div class="form-floating mb-3">
                    <input
                      type="email"
                      class="form-control"
                      id="securityEmail"
                      v-model="formData.mail"
                      placeholder="Email address"
                      required
                    >
                    <label for="securityEmail">Email Address</label>
                  </div>

                  <div class="form-floating">
                    <input
                      type="tel"
                      class="form-control"
                      id="securityMobile"
                      v-model="formData.mobile"
                      placeholder="Mobile number"
                      maxlength="10"
                      pattern="[0-9]*"
                      required
                    >
                    <label for="securityMobile">Mobile Number</label>
                  </div>
                </div>
              </div>

              <!-- Personal Section -->
              <div class="col-md-6">
                <div class="profile-section">
                  <h3 class="section-title h5 mb-4">Personal Details</h3>

                  <div class="form-floating mb-3">
                    <input
                      type="text"
                      class="form-control text-uppercase"
                      id="personalName"
                      v-model="formData.full_name"
                      placeholder="Full name"
                      required
                    >
                    <label for="personalName">Full Name</label>
                  </div>

                  <div class="form-floating mb-3">
                    <input
                      type="text"
                      class="form-control"
                      id="personalAddress"
                      v-model="formData.address"
                      placeholder="Address"
                      required
                    >
                    <label for="personalAddress">Address</label>
                  </div>

                  <div class="form-floating">
                    <input
                      type="text"
                      class="form-control"
                      id="personalPincode"
                      v-model="formData.pin_code"
                      placeholder="PIN code"
                      required
                    >
                    <label for="personalPincode">PIN Code</label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons mt-4">
              <div class="row g-3">
                <div class="col-md-6">
                  <button type="submit" class="btn submit-btn w-100">
                    Save Changes
                  </button>
                </div>
                <div class="col-md-6">
                  <button type="button" class="btn cancel-btn w-100" @click="handleCancel">
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
        @click="closeNotification"
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
            @click="closeNotification"
            aria-label="Close alert"
          ></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'ProfileManager',

  setup() {
    const router = useRouter()
    const isLoading = ref(true)
    
    const formData = reactive({
      password: '',
      mail: '',
      mobile: '',
      full_name: '',
      address: '',
      pin_code: ''
    })

    const notification = reactive({
      message: '',
      type: ''
    })

    const displayNotification = (message, type = 'success') => {
      notification.message = message
      notification.type = `notification-${type}`
      setTimeout(() => {
        closeNotification()
      }, 5000)
    }

    const closeNotification = () => {
      notification.message = ''
      notification.type = ''
    }

    const retrieveProfileData = async () => {
      try {
        const customerId = localStorage.getItem('cust_id')
        const token = localStorage.getItem('cust_Token')
        
        const response = await axios.get(
          `http://127.0.0.1:5000/end_users/getConsumer/${customerId}`,
          {
            headers: { Authorization: token }
          }
        )

        const [userData] = response.data
        
        Object.assign(formData, {
          mail: userData.mail,
          mobile: userData.mobile,
          full_name: userData.full_name,
          address: userData.address,
          pin_code: userData.pin_code
        })
      } catch (error) {
        console.error('Profile fetch failed:', error)
        displayNotification('Unable to load profile data', 'error')
      } finally {
        isLoading.value = false
      }
    }

    const submitProfileUpdate = async () => {
      const submitData = new FormData()
      
      Object.entries(formData).forEach(([key, value]) => {
        if (key === 'password' && !value) return
        submitData.append(key === 'fullName' ? 'full_name' : key, value.toUpperCase())
      })

      try {
        const response = await axios.put(
          'http://127.0.0.1:5000/end_users/update_user',
          submitData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: localStorage.getItem('cust_Token')
            }
          }
        )
        displayNotification(response.data.message)
      } catch (error) {
        console.error('Profile update failed:', error)
        displayNotification('Profile update failed', 'error')
      }
    }

    const handleCancel = () => {
      router.push('/Custdash/SearchServices')
    }

    return {
      isLoading,
      formData,
      notification,
      submitProfileUpdate,
      handleCancel,
      closeNotification,
      retrieveProfileData
    }
  },

  mounted() {
    this.retrieveProfileData()
  }
}
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
  color: #ffffff; /* Keeping this white for contrast on the header */
}

.profile-icon {
  color: #ffffff; /* Keeping this white for contrast on the header */
}

.section-title {
  color: #000000;
  font-weight: 500;
}

.form-floating > label {
  color: #00000000;
}

.form-floating > .form-control {
  color: #000000;
}

.form-floating > .form-control:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 0.25rem rgba(25, 118, 210, 0.25);
  color: #000000;
}

.form-floating > .form-control::placeholder {
  color: #666666;
}

.submit-btn {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  color: white; /* Keeping this white for contrast on the button */
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  transition: transform 0.2s;
}

.submit-btn:hover {
  color: white; /* Keeping this white for contrast on the button */
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
  z-index: 1050;
}

.notification-panel {
  position: relative;
  background: white;
  padding: 1rem 3rem 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  width: 400px;
  color: #000000;
}

.notification-close {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  color: #000000;
}

.notification-success { 
  border-left: 4px solid #2e7d32; 
  color: #000000;
}

.notification-error { 
  border-left: 4px solid #c62828; 
  color: #000000;
}

/* Input specific styles */
input.form-control {
  color: #000000 !important;
}

input.form-control:focus {
  color: #000000;
}

/* Loading spinner color override */
.spinner-border.text-light {
  color: #ffffff !important; /* Keeping this white for visibility on the dark background */
}

@media (max-width: 768px) {
  .profile-container {
    padding: 0.5rem;
  }

  .profile-title {
    font-size: 1.5rem;
  }
}
</style>