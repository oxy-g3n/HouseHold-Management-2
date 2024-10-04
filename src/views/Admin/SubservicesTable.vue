<template>
    <div class="subservices-table-container">
      <h3>Subservices for {{ serviceName }}</h3>
      <table class="requests-table">
        <thead>
          <tr>
            <th>Subservice Name</th>
            <th>Base Rate</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subservice in subservices" :key="subservice.subservice_id">
            <td>{{ subservice.subservice_name }}</td>
            <td>${{ subservice.base_rate }}</td>
          </tr>
        </tbody>
      </table>
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
  
  </style>