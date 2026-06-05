<script setup>
import { ref } from 'vue'
import * as Strings from '../utilities/strings.js'
import { useRouter } from 'vue-router'


const WelcomeMessage = ref(Strings.WELCOME_MESSAGE)
const InstructionMessage = ref(Strings.INSTRUCTION_MESSAGE)
const router = useRouter()

</script>

<template>
  <div class="galaxy-card">
    <h2 class="welcome-message"><strong>{{ WelcomeMessage }}</strong></h2>
    <p><strong>{{ InstructionMessage }}</strong></p>
    
    <button @click="">
      Click to proceed to Profile Page
    </button>
    <button @click="">
      Click to proceed to Galaxy Classification
    </button>
  </div>
</template>

<style scoped>
welcome-message {
    color: black !important;
    }
</style>

<style scoped>
.galaxy-card {
  border: 2px solid #333;
  color: rgb(0, 0, 0);
  padding: 15px;
  border-radius: 8px;
  background: #f5f5f5;
}

button {
  background: #007bff;
  color: rgb(255, 255, 255);
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

