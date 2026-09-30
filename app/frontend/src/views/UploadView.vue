<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isDragging = ref(false)
const selectedFile = ref(null)
const selectedCulture = ref('malwai')
const region = ref('punjab')
const setting = ref('rural')
const isUploading = ref(false)

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) selectedFile.value = file
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) selectedFile.value = file
}

const startExtraction = async () => {
  if (!selectedFile.value) return
  isUploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('culture_id', selectedCulture.value.toLowerCase().replace(' ', ''))
    
    const res = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData
    })
    
    if (!res.ok) throw new Error('Upload failed')
    const data = await res.json()
    
    // Save project_id to localStorage so subsequent pages can fetch state
    localStorage.setItem('project_id', data.project_id)
    
    // Navigate to extraction review (Gate 1)
    router.push('/extraction')
  } catch(err) {
    alert("Error uploading: " + err.message)
  } finally {
    isUploading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto py-12 px-6">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
        Screenplay Adaptation Studio
      </h1>
      <p class="text-gray-400 text-lg">Upload your 3-5 page screenplay to begin the cultural adaptation process.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Upload Section -->
      <div 
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="handleDrop"
        :class="[
          'border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center transition-all duration-300',
          isDragging ? 'border-purple-500 bg-purple-500/10' : 'border-gray-700 bg-gray-800/50 hover:border-gray-500 hover:bg-gray-800'
        ]"
      >
        <div v-if="!selectedFile" class="text-center">
          <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
          <p class="text-gray-300 font-medium mb-2">Drag and drop your screenplay here</p>
          <p class="text-gray-500 text-sm mb-6">Supports .pdf, .docx, .txt</p>
          
          <label class="cursor-pointer bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-full font-medium transition-colors">
            Browse Files
            <input type="file" class="hidden" accept=".pdf,.docx,.txt" @change="handleFileUpload">
          </label>
        </div>
        <div v-else class="text-center">
          <div class="bg-green-500/20 text-green-400 p-4 rounded-full mb-4 inline-block">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          </div>
          <p class="text-gray-200 font-medium text-lg">{{ selectedFile.name }}</p>
          <button @click="selectedFile = null" class="text-red-400 text-sm mt-2 hover:text-red-300">Remove</button>
        </div>
      </div>

      <!-- Settings Section -->
      <div class="bg-gray-800/50 rounded-2xl p-8 border border-gray-700">
        <h2 class="text-2xl font-bold text-gray-100 mb-6">Adaptation Settings</h2>
        
        <div class="space-y-5">
          <div>
            <label class="block text-gray-400 text-sm font-medium mb-2">Target Culture & Dialect</label>
            <select v-model="selectedCulture" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors">
              <option value="malwai">Malwai (Punjab)</option>
              <option value="marwari">Marwari (Rajasthan)</option>
              <option value="majhi">Majhi</option>
              <option value="bangru">Bangru</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-gray-400 text-sm font-medium mb-2">Setting</label>
              <select v-model="setting" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors">
                <option value="rural">Rural / Village</option>
                <option value="urban">Urban / City</option>
              </select>
            </div>
            <div>
              <label class="block text-gray-400 text-sm font-medium mb-2">Script Output</label>
              <select class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-gray-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors">
                <option value="english">English (Transliterated)</option>
                <option value="native">Native Script</option>
              </select>
            </div>
          </div>
        </div>

        <button 
          @click="startExtraction" 
          :disabled="!selectedFile || isUploading"
          :class="[
            'w-full mt-8 py-3 rounded-lg font-bold text-lg transition-all',
            (!selectedFile || isUploading) ? 'bg-gray-700 text-gray-500 cursor-not-allowed' : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:shadow-lg hover:shadow-purple-500/30'
          ]"
        >
          <span v-if="isUploading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Extracting Narrative...
          </span>
          <span v-else>Start Extraction (Gate 1)</span>
        </button>
      </div>
    </div>
  </div>
</template>
