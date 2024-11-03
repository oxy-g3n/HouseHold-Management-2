<!-- src/components/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <span class="navbar-text" id="welcome-message">{{ welcomeMessage }}</span>
      <button
      data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/adminDash/Services">Services</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/adminDash/allRequests">Stats</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/adminDash/ApprovalCentre">Approvals</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/" @click="deletelocal()">Logout</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNav',
  data() {
    return {
      welcomeMessage: 'Welcome user!'
    };
  },
  methods:
  {
    deletelocal()
  {
    localStorage.removeItem('admin_Token');
    localStorage.removeItem('admin_name');
    localStorage.removeItem('admin_id');
    localStorage.removeItem('admin_Fullname');
  }
  },  
  mounted() {
      const uname = localStorage.getItem('admin_Fullname');
      const uid = localStorage.getItem('admin_id');
      if (uname) {
        this.welcomeMessage = `Welcome ${uname}!      ID: ${uid}`;
      }
  }
};
</script>

<style scoped>
.navbar {
  background-color: white;
}
.navbar-text{
  color:white;
}
</style>
<!-- 
if (response.data.role === 'admin') {
  setTimeout(() => {
    localStorage.setItem('admin_Token', token);
    localStorage.setItem('admin_name', username);
    localStorage.setItem('admin_id', user_id);
    localStorage.setItem('admin_Fullname', full_name);
    this.$router.push('/Admindash');
  }, 1000);
} -->