<script setup>
import { ref } from 'vue'

const isExporting = ref(false)

const downloadExport = async () => {
  isExporting.value = true
  const projectId = localStorage.getItem('project_id')
  try {
    const response = await fetch(`http://localhost:8000/api/export/${projectId}`)
    if (!response.ok) throw new Error('Export failed')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'submission_export.zip'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  } catch (err) {
    alert("Error downloading file: " + err.message)
  } finally {
    isExporting.value = false
  }
}

const startNewProject = () => {
  localStorage.removeItem('project_id')
  window.location.href = '/'
}
</script>

<template>
  <div class="max-w-4xl mx-auto py-12 px-6 text-center">
    
    <div class="mb-10">
      <div class="inline-flex items-center justify-center w-20 h-20 bg-green-500/20 text-green-400 rounded-full mb-6">
        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
      </div>
      <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
        Adaptation Complete
      </h1>
      <p class="text-gray-400 text-lg">The story has been culturally adapted and visually realized with strict continuity.</p>
    </div>

    <div class="bg-gray-800/50 rounded-2xl border border-gray-700 p-8 mb-10 text-left">
      <h2 class="text-xl font-bold text-gray-200 mb-6 flex items-center gap-2">
        <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
        Export Package Contents
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
        <div>
          <h3 class="font-bold text-gray-400 uppercase tracking-wider mb-3">Documents</h3>
          <ul class="space-y-2 text-gray-300 font-mono">
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-purple-500"></div>adapted_screenplay.pdf</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-purple-500"></div>scene_breakdown.json</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-purple-500"></div>continuity_report.pdf</li>
          </ul>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-400 uppercase tracking-wider mb-3">Audit Trail</h3>
          <ul class="space-y-2 text-gray-300 font-mono">
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div>adaptation_plan.json</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div>cultural_evidence.json</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div>generation_manifest.json</li>
          </ul>
        </div>
        
        <div class="md:col-span-2 mt-4 pt-4 border-t border-gray-700">
          <h3 class="font-bold text-gray-400 uppercase tracking-wider mb-3">Visual Assets</h3>
          <ul class="space-y-2 text-gray-300 font-mono flex flex-wrap gap-x-8 gap-y-2">
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-pink-500"></div>character_bible/</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-pink-500"></div>costume_bible/</li>
            <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-pink-500"></div>scene_keyframes/</li>
          </ul>
        </div>
      </div>
    </div>

    <button 
      @click="downloadExport" 
      :disabled="isExporting"
      class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-lg font-bold py-4 px-12 rounded-xl transition-all shadow-lg hover:shadow-purple-500/30 flex items-center justify-center mx-auto min-w-[300px]"
    >
      <span v-if="isExporting" class="flex items-center gap-3">
        <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        Generating Package...
      </span>
      <span v-else class="flex items-center gap-2">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        Download submission_export.zip
      </span>
    </button>
    
    <div class="mt-6">
      <button 
        @click="startNewProject" 
        class="text-gray-400 hover:text-white transition-colors underline decoration-gray-600 underline-offset-4"
      >
        Start a New Project (Back to Home)
      </button>
    </div>
  </div>
</template>
