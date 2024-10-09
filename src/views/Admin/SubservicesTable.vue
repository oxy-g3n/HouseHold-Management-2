<template>
  <div class="subservices-table-container">
    <h3>Subservices for {{ serviceName }}</h3>
    <table class="requests-table" v-if="subservices.length > 0">
      <thead>
        <tr>
          <th>Subservice Name</th>
          <th>Base Rate</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="subservice in subservices" :key="subservice.subservice_id">
          <td>{{ subservice.subservice_name }}</td>
          <td>${{ subservice.base_rate }}</td>
          <td>
            <button @click="editSubservice(subservice)" class="btn btn-primary btn-sm">Edit Subservice</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="searchQuery">No subservices match the search query.</p>
    <p v-else>No subservices available for this service.</p>
  </div>
</template>

<script>
export default {
  name: 'SubservicesTable',
  props: {
    subservices: {
      type: Array,
      required: true
    },
    serviceName: {
      type: String,
      required: true
    },
    searchQuery: {
      type: String,
      default: ''
    }
  },
  methods: {
    editSubservice(subservice) {
      this.$emit('edit-subservice', subservice);
    }
  }
}
</script>
  
  <style scoped>
  .subservices-table-container {
    margin-top: 20px;
    background-color: #2c3e50;
    border-radius: 5px;
    padding: 15px;
  }
  
  h3 {
    color: white;
    margin-bottom: 10px;
  }
  
  .requests-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .requests-table th,
  .requests-table td {
    border: 1px solid #4a6278;
    padding: 12px;
    text-align: left;
    color: white;
  }
  
  .requests-table th {
    background-color: #34495e;
  }
  
  .requests-table tr:nth-child(even) {
    background-color: #3a536b;
  }
  
  .requests-table tr:hover {
    background-color: #4a6278;
  }
  
  .btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  border-radius: 0.2rem;
}

  </style>