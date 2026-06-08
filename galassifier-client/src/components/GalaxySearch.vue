<script setup>
import { ref } from 'vue'
import * as Strings from '../utilities/strings.js'
import { useRouter } from 'vue-router'

const isDrag = ref(false);
const isFileDropped = ref(false);
const isFileSelected = ref(false);
const file =ref(null)
const router = useRouter()

function handleDragOver() {
  isDrag.value = true;
}
function handleDragLeave() {
  isDrag.value = false;
}

function SetSelectedFile(event)
{
  file.value = event.target.files[0]
  isFileSelected.value = true;
}

function handleDrop(event) {
  isDrag.value = false
  file.value = event.dataTransfer.files[0]
  if (file.value) {
    console.log("File dropped: ", file.value.name);
    isFileDropped.value = true;
  }
  else
  {
    console.log("ERROR: File dropped not found")
  }
}

const SendClassificationRequest = async () => {
  if(file.value)
  {
    try{
      //Send classifcation request to backend
      console.log("Sending classification request for image: ", file.value.name);

      const formData = new FormData()
      formData.append('image', file.value)

      const response = await fetch('/api/process_galaxy_image/', {
        method: 'POST',
        body: formData
      })

      console.log("Response received from server");

      const data = await response.json();

      sessionStorage.setItem('galaxyResult', JSON.stringify(data))
      
      await router.push(
        {
          name: 'GalaxyResultCard',
        }
      )

      console.log("Pushed to result");
    }
    
    catch(error){
      console.error(Strings.CLASSIFICATION_ERROR, error);
    }
  }
  else
  {
    console.log("not sending");
  }
}

</script>

<template>
  <main class="galaxy-search-page">
    <div class="galaxy-card">

    </div>

    <div
      class="drop-zone"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <p class="drop-zone-title">
        Drag and drop an image here, or click to select a file
      </p>

      <input type="file" ref="fileInput" class="hidden" @change="SetSelectedFile" />
    </div>

    <button
      class="send-button"
      :disabled="!isFileDropped && !isFileSelected"
      @click="SendClassificationRequest"
    >
      Send request
    </button>
  </main>
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

.drop-zone {
  border: 2px dashed #3182ce;
  border-radius: 8px;
  padding: 28px 16px;
  margin: 16px 0;
  background: #ebf8ff;
  text-align: center;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.drop-zone.dragover
  {
    background: #bee3f8;
    border-color: #63b3ed;
  }

.drop-zone.hover {
  background: #bee3f8;
  border-color: #63b3ed;
}

.drop-zone-title {
  color: #2c5282;
  font-weight: 700;
  margin: 0;
}

.send-button {
  background: #38a169;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.send-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

</style>