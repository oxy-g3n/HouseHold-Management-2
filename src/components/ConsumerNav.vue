<!-- src/components/Navbar.vue -->
<template>
  <nav class="customer-navigation">
    <div class="nav-container">
      <!-- Brand Section -->
      <div class="brand-section">
        <div class="customer-profile">
          <div class="profile-avatar">
            {{ getInitials() }}
          </div>
          <div class="customer-info">
            <h2 class="customer-name">{{ customerName }}</h2>
            <span class="customer-id">ID: {{ customerId }}</span>
            <span v-if="approvalStatus !== '1'" class="approval-status">
              Not Approved by Admin!
            </span>
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
  name: 'CustNav',
  
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isMenuOpen = ref(false);
    const customerName = ref('');
    const customerId = ref('');
    const approvalStatus = ref('');

    const navItems = [
      { 
        label: 'Search',
        path: '/Custdash/SearchServices',
        icon: 'fas fa-search'
      },
      { 
        label: 'My Services',
        path: '/Custdash/MyServices',
        icon: 'fas fa-briefcase'
      },
      { 
        label: 'Summary',
        path: '/Custdash/Summary',
        icon: 'fas fa-chart-bar'
      },
      { 
        label: 'Edit Profile',
        path: '/Custdash/editProf',
        icon: 'fas fa-user-edit'
      }
    ];

    const currentRoute = computed(() => route.path);

    const getInitials = () => {
      return customerName.value
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase();
    };

    const handleLogout = () => {
      ['cust_Token', 'cust_name', 'cust_id', 'cust_Fullname', 'cust_approval']
        .forEach(key => localStorage.removeItem(key));
      router.push('/');
    };

    onMounted(() => {
      customerName.value = localStorage.getItem('cust_Fullname') || 'Customer';
      customerId.value = localStorage.getItem('cust_id') || 'N/A';
      approvalStatus.value = localStorage.getItem('cust_approval') || '0';
    });

    return {
      isMenuOpen,
      navItems,
      currentRoute,
      customerName,
      customerId,
      approvalStatus,
      getInitials,
      handleLogout
    };
  }
};
</script>

<style scoped>
.customer-navigation {
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

.customer-profile {
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

.customer-info {
  color: white;
}

.customer-name {
  font-size: 1rem;
  margin: 0;
  font-weight: 600;
}

.customer-id {
  font-size: 0.8rem;
  opacity: 0.8;
  display: block;
}

.approval-status {
  font-size: 0.8rem;
  color: #ff9800;
  display: block;
  margin-top: 0.2rem;
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