<script setup>
import { ref } from 'vue'
import * as Strings from '../utilities/strings.js'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

console.log('GalaxyResultCard setup started')
const rawResult = sessionStorage.getItem('galaxyResult')
const result = rawResult ? JSON.parse(rawResult) : {}
const MoreClassificationsString = Strings.MORE_CLASSIFICATION_STRING;
const router = useRouter();

function ClassifyMore()
{
    router.push('/galaxy-search');
}

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

    <button class="more-button" @click="ClassifyMore" >
      {{MoreClassificationsString}}
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

.more-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 160px;
  min-height: 36px;
  font-size: 14px;
  line-height: 1;
  color: white !important;
  background: #007bff;
}
</style>