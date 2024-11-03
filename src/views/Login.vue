<template>
  <section class="auth-wrapper position-relative">
    <div class="portal-container mx-auto p-4">
      <div class="entry-card bg-white shadow-lg rounded-3">
        <header class="portal-header text-center p-4 bg-gradient">
          <span class="portal-icon display-4">🔐</span>
          <h1 class="welcome-text mt-3 text-black">Welcome Back!</h1>
        </header>

        <main class="credential-form p-4">
          <form @submit.prevent="authenticateUser">
            <div class="field-wrapper mb-4">
              <div class="floating-input position-relative">
                <input 
                  type="text"
                  id="identityField"
                  v-model="credentials.identifier"
                  class="credential-input form-control"
                  required
                  autocomplete="username"
                >
                <label for="identityField" class="floating-label">Username</label>
              </div>
            </div>

            <div class="field-wrapper mb-4">
              <div class="floating-input position-relative">
                <input 
                  type="password"
                  id="secretField"
                  v-model="credentials.secret"
                  class="credential-input form-control"
                  required
                  autocomplete="current-password"
                >
                <label for="secretField" class="floating-label">Password</label>
              </div>
            </div>

            <div class="action-buttons">
              <button type="submit" class="portal-btn enter-btn w-100 mb-3">
                Login
              </button>
              
              <div class="row g-2">
                <div class="col-6">
                  <button 
                    type="button" 
                    class="portal-btn register-btn w-100 h-100"
                    @click="navigateToRegistration('individual')"
                  >
                    New Customer
                  </button>
                </div>
                <div class="col-6">
                  <button 
                    type="button" 
                    class="portal-btn register-btn w-100"
                    @click="navigateToRegistration('provider')"
                  >
                    New Service Provider
                  </button>
                </div>
              </div>
            </div>
          </form>
        </main>
      </div>
    </div>

    <div 
      v-if="notification.message" 
      class="notification-overlay"
      @click="dismissNotification"
    >
      <div 
        class="notification-box"
        :class="notification.type"
        @click.stop
      >
        <p class="notification-text mb-0">{{ notification.message }}</p>
        <button 
          class="notification-dismiss btn-close"
          @click="dismissNotification"
          aria-label="Close notification"
        ></button>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'AuthPortal',
  
  setup() {
    const router = useRouter()
    const credentials = reactive({
      identifier: '',
      secret: ''
    })
    
    const notification = reactive({
      message: '',
      type: ''
    })

    const showNotification = (message, type) => {
      notification.message = message
      notification.type = `notification-${type}`
    }

    const dismissNotification = () => {
      notification.message = ''
      notification.type = ''
    }

    const authenticateUser = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/users/auth', {
          username: credentials.identifier,
          password: credentials.secret,
          action: "login"
        })

        if (response.data.Success) {
          showNotification('Authentication successful', 'success')
          const userInfo = response.data
          
          const roleMap = {
            customer: {
              route: '/Custdash',
              storage: {
                token: ['cust_Token', userInfo.token],
                name: ['cust_name', credentials.identifier],
                id: ['cust_id', userInfo.user_id],
                fullName: ['cust_Fullname', userInfo.full_name],
                pinCode: ['cust_pin', userInfo.pin_code],
                approval: ['cust_approval', userInfo.approval]
              }
            },
            serviceman: {
              route: '/Servicedash',
              storage: {
                token: ['service_Token', userInfo.token],
                name: ['service_name', credentials.identifier],
                id: ['service_id', userInfo.user_id],
                fullName: ['service_Fullname', userInfo.full_name]
              }
            },
            admin: {
              route: '/adminDash',
              storage: {
                token: ['admin_Token', userInfo.token],
                name: ['admin_name', credentials.identifier],
                id: ['admin_id', userInfo.user_id],
                fullName: ['admin_Fullname', userInfo.full_name]
              }
            }
          }

          const roleConfig = roleMap[userInfo.role]
          
          setTimeout(() => {
            Object.values(roleConfig.storage).forEach(([key, value]) => {
              localStorage.setItem(key, value)
            })
            router.push(roleConfig.route)
          }, 1000)
        } else {
          showNotification('Invalid credentials provided', 'warning')
        }
      } catch (error) {
        console.error('Authentication failed:', error)
        showNotification('Authentication process failed', 'error')
      }
    }

    const navigateToRegistration = (type) => {
      const routes = {
        individual: '/CustomerRegistration',
        provider: '/ServiceRegistration'
      }
      router.push(routes[type])
    }

    return {
      credentials,
      notification,
      authenticateUser,
      navigateToRegistration,
      dismissNotification
    }
  }
}
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  display: grid;
  place-items: center;
}

.portal-container {
  width: 100%;
  max-width: 480px;
}

.entry-card {
  overflow: hidden;
}

.portal-header {
  background: linear-gradient(45deg, #303f9f, #1976d2);
}

.welcome-text {
  color: #ffffff;
  font-size: 1.75rem;
  font-weight: 300;
}

.floating-input {
  margin-bottom: 1rem;
}

.credential-input {
  height: 3.5rem;
  padding: 1rem 0.75rem;
  font-size: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 0.5rem;
  transition: border-color 0.2s;
}

.credential-input:focus {
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
}

.credential-input:focus ~ .floating-label,
.credential-input:not(:placeholder-shown) ~ .floating-label {
  top: 0;
  font-size: 0.875rem;
  color: #1976d2;
  background: white;
  padding: 0 0.25rem;
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

.enter-btn {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  color: white;
}

.register-btn {
  background: #f5f5f5;
  color: #303f9f;
}

.notification-overlay {
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

.notification-box {
  position: relative;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 90%;
  width: 400px;
}

.notification-dismiss {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.notification-success { border-left: 4px solid #2e7d32; }
.notification-warning { border-left: 4px solid #f57c00; }
.notification-error { border-left: 4px solid #c62828; }

@media (max-width: 576px) {
  .portal-container {
    padding: 1rem;
  }
  
  .welcome-text {
    font-size: 1.5rem;
  }
}
</style>