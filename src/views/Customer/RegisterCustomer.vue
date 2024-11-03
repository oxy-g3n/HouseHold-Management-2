<template>
  <div class="enrollment-portal position-relative">
    <div class="enrollment-container mx-auto p-4">
      <div class="profile-card bg-white shadow-lg rounded-3">
        <header class="profile-header text-center p-4 bg-gradient">
          <span class="profile-icon display-4">📝</span>
          <h1 class="enrollment-title mt-3 text-white">Create Your Account</h1>
        </header>

        <main class="profile-form p-4">
          <form @submit.prevent="initiateRegistration">
            <div class="row g-4">
              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="text"
                    id="userIdentifier"
                    v-model="profileData.userIdentifier"
                    class="profile-input form-control"
                    required
                    autocomplete="username"
                  >
                  <label for="userIdentifier" class="floating-label">Choose Username</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="text"
                    id="displayName"
                    v-model="profileData.displayName"
                    class="profile-input form-control"
                    required
                  >
                  <label for="displayName" class="floating-label">Full Name</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="password"
                    id="accessKey"
                    v-model="profileData.accessKey"
                    class="profile-input form-control"
                    required
                    autocomplete="new-password"
                  >
                  <label for="accessKey" class="floating-label">Create Password</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="email"
                    id="contactEmail"
                    v-model="profileData.contactEmail"
                    class="profile-input form-control"
                    required
                  >
                  <label for="contactEmail" class="floating-label">Email Address</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="tel"
                    id="contactPhone"
                    v-model="profileData.contactPhone"
                    class="profile-input form-control"
                    required
                  >
                  <label for="contactPhone" class="floating-label">Mobile Number</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="floating-group position-relative">
                  <input
                    type="text"
                    id="postalCode"
                    v-model="profileData.postalCode"
                    class="profile-input form-control"
                    required
                  >
                  <label for="postalCode" class="floating-label">Postal Code</label>
                </div>
              </div>

              <div class="col-12">
                <div class="floating-group position-relative">
                  <input
                    type="text"
                    id="residentialAddress"
                    v-model="profileData.residentialAddress"
                    class="profile-input form-control"
                    required
                  >
                  <label for="residentialAddress" class="floating-label">Residential Address</label>
                </div>
              </div>
            </div>

            <div class="action-panel mt-4">
              <div class="row g-3">
                <div class="col-md-6">
                  <button type="submit" class="portal-btn submit-btn w-100">
                    Complete Registration
                  </button>
                </div>
                <div class="col-md-6">
                  <button type="button" class="portal-btn cancel-btn w-100" @click="returnToPortal">
                    Return to Login
                  </button>
                </div>
              </div>
            </div>
          </form>
        </main>
      </div>
    </div>

    <div 
      v-if="statusMessage.content" 
      class="status-overlay"
      @click="dismissStatus"
    >
      <div 
        class="status-container"
        :class="statusMessage.category"
        @click.stop
      >
        <p class="status-text mb-0">{{ statusMessage.content }}</p>
        <button 
          class="status-close btn-close"
          @click="dismissStatus"
          aria-label="Close status message"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'EnrollmentPortal',
  
  setup() {
    const router = useRouter()
    const profileData = reactive({
      userIdentifier: '',
      accessKey: '',
      contactEmail: '',
      contactPhone: '',
      displayName: '',
      residentialAddress: '',
      postalCode: ''
    })
    
    const statusMessage = reactive({
      content: '',
      category: ''
    })

    const displayStatus = (content, type) => {
      statusMessage.content = content
      statusMessage.category = `status-${type}`
      setTimeout(() => dismissStatus(), 5000)
    }

    const dismissStatus = () => {
      statusMessage.content = ''
      statusMessage.category = ''
    }

    const initiateRegistration = async () => {
      const enrollmentData = new FormData()
      enrollmentData.append('action', 'cust_reg')
      enrollmentData.append('username', profileData.userIdentifier)
      enrollmentData.append('password', profileData.accessKey)
      enrollmentData.append('mail', profileData.contactEmail)
      enrollmentData.append('mobile', profileData.contactPhone)
      enrollmentData.append('full_name', profileData.displayName)
      enrollmentData.append('address', profileData.residentialAddress)
      enrollmentData.append('pin_code', profileData.postalCode)

      try {
        const response = await axios.post('http://127.0.0.1:5000/users/register', enrollmentData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        displayStatus(response.data, 'success')
        setTimeout(() => router.push('/'), 2000)
      } catch (error) {
        console.error('Enrollment failed:', error)
        displayStatus('Registration process encountered an error', 'error')
      }
    }

    const returnToPortal = () => {
      router.push('/')
    }

    return {
      profileData,
      statusMessage,
      initiateRegistration,
      returnToPortal,
      dismissStatus
    }
  }
}
</script>

<style scoped>
.enrollment-portal {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  display: grid;
  place-items: center;
}

.enrollment-container {
  width: 100%;
  max-width: 900px;
}

.profile-card {
  overflow: hidden;
}

.profile-header {
  background: linear-gradient(45deg, #303f9f, #1976d2);
}

.enrollment-title {
  font-size: 1.75rem;
  font-weight: 300;
}

.floating-group {
  margin-bottom: 0.5rem;
}

.profile-input {
  height: 3.5rem;
  padding: 1rem 0.75rem;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 0.5rem;
  transition: border-color 0.2s;
}

.profile-input:focus {
  border-color: #1976d2;
  box-shadow: none;
}

.floating-label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  transition: 0.2s ease all;
  color: #757575;
  pointer-events: none;
  padding: 0 0.25rem;
}

.profile-input:focus ~ .floating-label,
.profile-input:not(:placeholder-shown) ~ .floating-label {
  top: 0;
  font-size: 0.875rem;
  color: #1976d2;
  background: white;
}

.portal-btn {
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: transform 0.2s;
}

.portal-btn:active {
  transform: scale(0.98);
}

.submit-btn {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  color: white;
}

.cancel-btn {
  background: #f5f5f5;
  color: #303f9f;
}

.status-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
  z-index: 1000;
}

.status-container {
  position: relative;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  width: 400px;
}

.status-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.status-success { border-left: 4px solid #2e7d32; }
.status-error { border-left: 4px solid #c62828; }

@media (max-width: 768px) {
  .enrollment-container {
    padding: 1rem;
  }
  
  .enrollment-title {
    font-size: 1.5rem;
  }
}
</style>