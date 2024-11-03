<!-- src/views/DashboardLayout.vue -->
<template>
    <div class="dashboard-layout">
      <CustomerNav />
      <div class="container mt-4">
        <router-view></router-view> <!-- Dynamic content will be loaded here -->
      </div>
    </div>
  </template>
  
  <script>
  import CustomerNav from '@/components/ConsumerNav.vue';
  
  
  export default {
    name: 'Custdash',
    components: {
      CustomerNav
    },
    created() {
      this.$router.push('/Custdash/SearchServices');
    }
  }
  </script>
  
  <style scoped>
  .dashboard-layout {
    background-color: #000567; /* Dark blue background */
    color: white; /* Optional: Adjust text color for better contrast */
    min-height: 100vh; /* Ensure it covers the full viewport height */
    display: flex;
    flex-direction: column;
  }
  
  .container {
    padding-top: 20px;
  }
  </style>
  