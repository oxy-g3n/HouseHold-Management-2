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
            <router-link class="nav-link navbar-text" to="/Custdash/SearchServices">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/Custdash/MyServices">My services</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text" to="/Custdash/Summary">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link navbar-text">Edit Profile</router-link>
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
  name: 'CustNav',
  data() {
    return {
      welcomeMessage: 'Welcome user!'
    };
  },
  methods:
  {
    deletelocal()
  {
    localStorage.removeItem('cust_Token');
    localStorage.removeItem('cust_name');
    localStorage.removeItem('cust_id');
    localStorage.removeItem('cust_Fullname');
  }
  },  
  mounted() {
      const uname = localStorage.getItem('cust_Fullname');
      const uid = localStorage.getItem('cust_id');
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