<!-- src/components/Navbar.vue -->
<template>
  <nav class="service-navigation">
    <div class="nav-container">
      <!-- Brand Section -->
      <div class="brand-section">
        <div class="service-profile">
          <div class="profile-avatar">
            {{ getInitials() }}
          </div>
          <div class="service-info">
            <h2 class="service-name">{{ serviceName }}</h2>
            <span class="service-id">ID: {{ serviceId }}</span>
          </div>
        </div>
      </div>

      <!-- Mobile Toggle -->
      <button 
        class="mobile-toggle"
        @click="isMenuOpen = !isMenuOpen"
        :aria-expanded="isMenuOpen"
        aria-label="Toggle navigation"
      >
        <span class="toggle-icon"></span>
      </button>

      <!-- Navigation Links -->
      <div 
        class="nav-content"
        :class="{ 'nav-open': isMenuOpen }"
      >
        <ul class="nav-links">
          <li v-for="(item, index) in navItems" :key="index">
            <router-link 
              :to="item.path"
              class="nav-link"
              :class="{ 'active': currentRoute === item.path }"
              @click="isMenuOpen = false"
            >
              <i :class="item.icon"></i>
              <span>{{ item.label }}</span>
            </router-link>
          </li>
        </ul>

        <!-- Action Buttons -->
        <div class="nav-actions">
          <button 
            class="action-button logout"
            @click="handleLogout"
          >
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'ServicemanNav',
  
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isMenuOpen = ref(false);
    const serviceName = ref('');
    const serviceId = ref('');

    const navItems = [
      { 
        label: 'Requests',
        path: '/Servicedash/requests',
        icon: 'fas fa-clipboard-list'
      },
      { 
        label: 'History',
        path: '/Servicedash/history',
        icon: 'fas fa-history'
      },
      { 
        label: 'Edit Profile',
        path: '/Servicedash/editProfile',
        icon: 'fas fa-user-edit'
      }
    ];

    const currentRoute = computed(() => route.path);

    const getInitials = () => {
      return serviceName.value
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase();
    };

    const handleLogout = () => {
      ['service_Token', 'service_id', 'service_name', 'service_Fullname']
        .forEach(key => localStorage.removeItem(key));
      router.push('/');
    };

    onMounted(() => {
      serviceName.value = localStorage.getItem('service_Fullname') || 'Service Provider';
      serviceId.value = localStorage.getItem('service_id') || 'N/A';
    });

    return {
      isMenuOpen,
      navItems,
      currentRoute,
      serviceName,
      serviceId,
      getInitials,
      handleLogout
    };
  }
};
</script>

<style scoped>
.service-navigation {
  background: linear-gradient(45deg, #303f9f, #1976d2);
  padding: 1rem 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-section {
  flex-shrink: 0;
}

.service-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.service-info {
  color: white;
}

.service-name {
  font-size: 1rem;
  margin: 0;
  font-weight: 600;
}

.service-id {
  font-size: 0.8rem;
  opacity: 0.8;
  display: block;
}

.nav-content {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.nav-link i {
  font-size: 1.1rem;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-button {
  background: none;
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  padding: 0.5rem;
  cursor: pointer;
}

.toggle-icon {
  display: block;
  width: 24px;
  height: 2px;
  background: white;
  position: relative;
  transition: all 0.3s ease;
}

.toggle-icon::before,
.toggle-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background: white;
  left: 0;
  transition: all 0.3s ease;
}

.toggle-icon::before {
  top: -6px;
}

.toggle-icon::after {
  bottom: -6px;
}

@media (max-width: 768px) {
  .mobile-toggle {
    display: block;
  }

  .nav-content {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: linear-gradient(45deg, #303f9f, #1976d2);
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  .nav-content.nav-open {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
  }

  .nav-link {
    padding: 1rem;
  }

  .nav-actions {
    width: 100%;
    justify-content: center;
  }
}
</style>