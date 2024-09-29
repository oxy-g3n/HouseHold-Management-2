<!-- src/components/Navbar.vue -->
<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <span class="navbar-text" id="welcome-message">{{ welcomeMessage }}</span>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
      <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/ServiceDash/requests">Requests</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/ServiceDash/history">History</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/ServiceDash/editProfile">Edit Profile</router-link>
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
  name: 'ServiemanNav',
  data() {
    return {
      welcomeMessage: 'Welcome user!'
    };
  },
  methods:
  {
    deletelocal()
  {
    localStorage.removeItem('service_Token');
    localStorage.removeItem('service_id');
    localStorage.removeItem('service_name');
    localStorage.removeItem('service_Fullname');
  }
  },  
  mounted() {
      const uname = localStorage.getItem('service_Fullname');
      const uid = localStorage.getItem('service_id');
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