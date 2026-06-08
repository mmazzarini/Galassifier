<script setup>
import { ref } from 'vue'
import * as Strings from '../utilities/strings.js'
import { useRouter } from 'vue-router'


const WelcomeMessage = ref(Strings.WELCOME_MESSAGE)
const InstructionMessage = ref(Strings.INSTRUCTION_MESSAGE)
const AppInfoMessage = ref(Strings.INFORMATION_APP_MESSAGE)
const ClickToStartMessage = ref(Strings.START_STRING)
const router = useRouter()

function goToGalaxyClassification()
{
    router.push('/galaxy-search')
}

</script>

<template>
  <div class="galaxy-card">
    <h2 class="welcome-message"><strong>{{ WelcomeMessage }}</strong></h2>
    <p><strong>{{ InstructionMessage }}</strong></p>
    
    <button @click="goToGalaxyClassification()">
      <p>{{ ClickToStartMessage }}</p>
    </button>
  </div>
</template>

<style scoped>
welcome-message {
    color: black !important;
    }
</style>

<style scoped>

button {
  background: #007bff;
  color: rgb(255, 255, 255);
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>

