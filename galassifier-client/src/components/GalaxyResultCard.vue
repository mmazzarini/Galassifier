<script setup>
import { ref } from 'vue'
import * as Strings from '../utilities/strings.js'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

console.log('GalaxyResultCard setup started')
const rawResult = sessionStorage.getItem('galaxyResult')
const result = rawResult ? JSON.parse(rawResult) : {}

//DEBUG ATTEMPT
const galaxytype = computed(() => {
  return result.galaxyType ?? result.classification ?? 'Unknown'
})

console.log('Galaxy result:', result)
</script>


<template>
  <div class="galaxy-card">
    <p>
      Classification:
      <strong>{{ galaxytype }}</strong>
    </p>

    <button>
      Classify more!!
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