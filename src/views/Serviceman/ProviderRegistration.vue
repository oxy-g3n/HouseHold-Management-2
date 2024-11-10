<template>
  <div class="professional-portal d-flex align-items-center justify-content-center min-vh-100">
    <div class="registration-wrapper mx-auto p-4">
      <div class="content-card bg-white rounded-4 shadow">
        <header class="registration-header text-center p-4 rounded-top-4">
          <span class="header-icon fs-1">🛠️</span>
          <h1 class="welcome-text mt-3 text-white fw-light">Professional Registration</h1>
        </header>

        <div class="registration-body p-4">
          <form @submit.prevent="processRegistration" class="needs-validation">
            <div class="row g-4">
              <!-- Personal Information Section -->
              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="text"
                    id="professionalId"
                    v-model="registrationDetails.professionalId"
                    class="custom-input form-control"
                    required
                    maxlength="30"
                  >
                  <label for="professionalId">Professional Username</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="text"
                    id="professionalName"
                    v-model="registrationDetails.professionalName"
                    class="custom-input form-control"
                    required
                    maxlength="60"
                  >
                  <label for="professionalName">Full Name</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="password"
                    id="securityKey"
                    v-model="registrationDetails.securityKey"
                    class="custom-input form-control"
                    required
                    minlength="8"
                  >
                  <label for="securityKey">Security Password</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="email"
                    id="emailContact"
                    v-model="registrationDetails.emailContact"
                    class="custom-input form-control"
                    required
                  >
                  <label for="emailContact">Email Address</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="tel"
                    id="phoneContact"
                    v-model="registrationDetails.phoneContact"
                    class="custom-input form-control"
                    maxlength="10"
                    pattern="[0-9]*"
                    required
                  >
                  <label for="phoneContact">Contact Number</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="text"
                    id="areaCode"
                    v-model="registrationDetails.areaCode"
                    class="custom-input form-control"
                    required
                    pattern="[0-9]*"
                    maxlength="6"
                  >
                  <label for="areaCode">Area Code</label>
                </div>
              </div>

              <div class="col-12">
                <div class="input-wrapper">
                  <textarea 
                    id="locationDetails"
                    v-model="registrationDetails.locationDetails"
                    class="custom-input form-control"
                    required
                    maxlength="500"
                    rows="3"
                  ></textarea>
                  <label for="locationDetails">Complete Address</label>
                </div>
              </div>

              <!-- Professional Details Section -->
              <div class="col-md-6">
                <div class="input-wrapper">
                  <select 
                    id="expertiseArea"
                    v-model="registrationDetails.selectedExpertise"
                    class="custom-input form-control"
                    @change="updateSpecializations"
                    required
                  >
                    <option value="">Choose Expertise Area</option>
                    <option 
                      v-for="expertise in expertiseAreas" 
                      :key="expertise.service_id"
                      :value="expertise"
                    >
                      {{ expertise.service_info.service_name }}
                    </option>
                  </select>
                  <label for="expertiseArea">Expertise Area</label>
                </div>
              </div>

              <div class="col-md-6" v-if="specializations.length">
                <div class="input-wrapper">
                  <select 
                    id="specialization"
                    v-model="registrationDetails.selectedSpecialization"
                    class="custom-input form-control"
                    required
                  >
                    <option value="">Select Specialization</option>
                    <option 
                      v-for="specialization in specializations"
                      :key="specialization.subservice_id"
                      :value="specialization"
                    >
                      {{ specialization.subservice_name }}
                    </option>
                  </select>
                  <label for="specialization">Specialization</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="number"
                    id="expertiseYears"
                    v-model="registrationDetails.expertiseYears"
                    class="custom-input form-control"
                    required
                    min="0"
                  >
                  <label for="expertiseYears">Years of Expertise</label>
                </div>
              </div>

              <div class="col-md-6">
                <div class="input-wrapper">
                  <input 
                    type="file"
                    id="workPortfolio"
                    @change="handlePortfolioUpload"
                    class="custom-input form-control"
                    required
                  >
                  <label for="workPortfolio">Work Portfolio</label>
                </div>
              </div>
            </div>

            <div class="action-section mt-4">
              <div class="row g-3">
                <div class="col-md-6">
                  <button 
                    type="submit" 
                    class="action-button submit-button w-100"
                    :disabled="!isFormComplete"
                  >
                    Complete Registration
                  </button>
                </div>
                <div class="col-md-6">
                  <button 
                    type="button" 
                    class="action-button cancel-button w-100"
                    @click="navigateHome"
                  >
                    Return to Home
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div 
      v-if="notificationDetails.message" 
      class="notification-overlay"
      @click="clearNotification"
    >
      <div 
        class="notification-content"
        :class="notificationDetails.type"
        @click.stop
      >
        {{ notificationDetails.message }}
        <button 
          class="notification-close btn-close"
          @click="clearNotification"
        ></button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'ProfessionalRegistration',
  
  setup() {
    const router = useRouter()
    
    const registrationDetails = reactive({
      professionalId: '',
      securityKey: '',
      emailContact: '',
      phoneContact: '',
      professionalName: '',
      locationDetails: '',
      areaCode: '',
      selectedExpertise: null,
      selectedSpecialization: null,
      expertiseYears: '',
      portfolioDocument: null
    })

    const notificationDetails = reactive({
      message: '',
      type: ''
    })

    const expertiseAreas = reactive([])
    const specializations = reactive([])

    const showNotification = (message, category) => {
      notificationDetails.message = message
      notificationDetails.type = `notification-${category}`
      setTimeout(clearNotification, 5000)
    }

    const clearNotification = () => {
      notificationDetails.message = ''
      notificationDetails.type = ''
    }

    const handlePortfolioUpload = (event) => {
      registrationDetails.portfolioDocument = event.target.files[0]
    }

    const isFormComplete = computed(() => {
      return registrationDetails.professionalId && registrationDetails.securityKey && 
             registrationDetails.emailContact && registrationDetails.phoneContact && 
             registrationDetails.professionalName && registrationDetails.locationDetails && 
             registrationDetails.areaCode && registrationDetails.selectedExpertise && 
             registrationDetails.selectedSpecialization && registrationDetails.expertiseYears && 
             registrationDetails.portfolioDocument
    })

    const processRegistration = async () => {
      if (!isFormComplete.value) {
        showNotification('Please complete all required fields', 'error')
        return
      }

      const formPayload = new FormData()
      formPayload.append('action', 'provider')
      formPayload.append('username', registrationDetails.professionalId)
      formPayload.append('password', registrationDetails.securityKey)
      formPayload.append('mail', registrationDetails.emailContact)
      formPayload.append('mobile', registrationDetails.phoneContact)
      formPayload.append('full_name', registrationDetails.professionalName.toUpperCase())
      formPayload.append('address', registrationDetails.locationDetails)
      formPayload.append('pin_code', registrationDetails.areaCode)
      formPayload.append('service', registrationDetails.selectedExpertise.service_info.service_name)
      formPayload.append('subservice', registrationDetails.selectedSpecialization.subservice_name)
      formPayload.append('experience', registrationDetails.expertiseYears)
      formPayload.append('portfolio', registrationDetails.portfolioDocument)

      try {
        const response = await axios.post('http://127.0.0.1:5000/end_users/register', formPayload, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        showNotification(response.data, 'success')
        setTimeout(() => router.push('/'), 2000)
      } catch (error) {
        console.error('Registration failed:', error)
        showNotification('Registration process encountered an error', 'error')
      }
    }

    const fetchExpertiseAreas = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/provisions/getProvisions')
        expertiseAreas.push(...response.data)
      } catch (error) {
        console.error('Error fetching expertise areas:', error)
        showNotification('Failed to load expertise areas', 'error')
      }
    }

    const updateSpecializations = () => {
      if (registrationDetails.selectedExpertise) {
        specializations.splice(0, specializations.length, 
          ...registrationDetails.selectedExpertise.subservices)
      } else {
        specializations.splice(0, specializations.length)
      }
      registrationDetails.selectedSpecialization = null
    }

    const navigateHome = () => {
      router.push('/')
    }

    fetchExpertiseAreas()

    return {
      registrationDetails,
      notificationDetails,
      expertiseAreas,
      specializations,
      isFormComplete,
      processRegistration,
      updateSpecializations,
      handlePortfolioUpload,
      navigateHome,
      clearNotification
    }
  }
}
</script>

<style scoped>
.professional-portal {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
}

.registration-wrapper {
  width: 100%;
  max-width: 1000px;
}

.content-card {
  overflow: hidden;
}

.registration-header {
  background: linear-gradient(45deg, #303f9f, #1976d2);
}

.welcome-text {
  font-size: 2rem;
}

.input-wrapper {
  position: relative;
  margin-bottom: 0.5rem;
}

.custom-input {
  height: 3.5rem;
  padding: 1rem 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 0.5rem;
  transition: border-color 0.2s;
}

.custom-input:focus {
  border-color: #1976d2;
  box-shadow: none;
}

.input-wrapper label {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background-color: white;
  padding: 0 0.25rem;
  color: #757575;
  transition: all 0.2s ease-out;
  pointer-events: none;
}

.custom-input:focus ~ label,
.custom-input:not(:placeholder-shown) ~ label {
  top: 0;
  transform: translateY(-50%) scale(0.85);
  color: #1976d2;
}

textarea.custom-input {
  height: auto;
  padding-top: 1.5rem;
}

textarea.custom-input ~ label {
  top: 1.5rem;
}

textarea.custom-input:focus ~ label,
textarea.custom-input:not(:placeholder-shown) ~ label {
  top: 0;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: transform 0.2s;
}

.submit-button {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  color: white;
}

.submit-button:disabled {
  background: #9e9e9e;
}

.cancel-button {
  background: #f5f5f5;
  color: #303f9f;
}

.action-button:active {
  transform: scale(0.98);
}

.notification-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
  z-index: 1000;
}

.notification-content {
  position: relative;
  padding: 1rem 2.5rem 1rem 1rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  width: 400px;
}

.notification-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.notification-success {
  border-left: 4px solid #4caf50;
}

.notification-error {
  border-left: 4px solid #f44336;
}

.notification-warning {
  border-left: 4px solid #ff9800;
}

@media (max-width: 768px) {
  .registration-wrapper {
    padding: 1rem;
  }

  .welcome-text {
    font-size: 1.5rem;
  }

  .action-button {
    padding: 0.5rem 1rem;
  }
}
</style>