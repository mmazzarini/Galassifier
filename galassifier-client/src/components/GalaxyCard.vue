<script setup>
import { ref } from 'vue'

const galaxyName = ref('Andromeda')
const classification = ref('Spiral')

const updateClassification = (newClass) => {
  classification.value = newClass
}
</script>

<template>
  <div class="galaxy-card">
    <h2><strong>{{ galaxyName }}</strong></h2>
    <p>Classification: <strong>{{ classification }}</strong></p>
    
    <button @click="updateClassification('Elliptical')">
      Mark as Elliptical
    </button>
  </div>
</template>

<style scoped>
.galaxy-card {
  border: 2px solid #333;
  padding: 15px;
  border-radius: 8px;
  background: #f5f5f5;
}

button {
  background: #007bff;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>