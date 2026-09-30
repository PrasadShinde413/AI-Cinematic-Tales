<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoading = ref(true)
const originalText = ref('')
const adaptedText = ref('')

onMounted(async () => {
  const projectId = localStorage.getItem('project_id')
  if (!projectId) {
    router.push('/')
    return
  }
  
  try {
    const res = await fetch(`http://localhost:8000/api/state/${projectId}`)
    const data = await res.json()
    
    // Extract screenplays from the rich state
    originalText.value = data.source_document?.text || 'No original text found.'
    adaptedText.value = data.adapted_screenplay?.text || 'No adapted text found. Did the LLM finish?'
  } catch(err) {
    console.error("Failed to load state", err)
  } finally {
    isLoading.value = false
  }
})

const proceedToVisuals = () => {
  router.push('/visuals')
}
</script>

<template>
  <div class="max-w-6xl mx-auto py-12 px-6">
    <div class="text-center mb-10">
      <div class="inline-block bg-purple-500/20 text-purple-400 px-4 py-1 rounded-full text-sm font-semibold tracking-wide mb-3 border border-purple-500/30">
        GATE 2.5: STORY PRESERVATION REVIEW
      </div>
      <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
        Adapted Screenplay Comparison
      </h1>
      <p class="text-gray-400 text-lg">
        Review the AI's rewritten script against the original source document.
      </p>
    </div>

    <div v-if="isLoading" class="flex justify-center items-center py-20">
      <svg class="animate-spin h-10 w-10 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
        
        <!-- Left: Original -->
        <div class="bg-gray-800/50 rounded-2xl border border-gray-700 overflow-hidden flex flex-col">
          <div class="bg-gray-900/80 px-6 py-4 border-b border-gray-700">
            <h2 class="text-xl font-bold text-gray-200 flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Original Source
            </h2>
          </div>
          <div class="p-6 h-[500px] overflow-y-auto font-mono text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
            {{ originalText }}
          </div>
        </div>

        <!-- Right: Adapted -->
        <div class="bg-gray-800/50 rounded-2xl border border-purple-500/50 overflow-hidden flex flex-col shadow-[0_0_15px_rgba(168,85,247,0.1)]">
          <div class="bg-gray-900/80 px-6 py-4 border-b border-purple-500/30 flex justify-between items-center">
            <h2 class="text-xl font-bold text-purple-300 flex items-center gap-2">
              <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
              Adapted Screenplay
            </h2>
            <span class="text-xs font-bold bg-green-500/20 text-green-400 px-2 py-1 rounded">CULTURALLY ALIGNED</span>
          </div>
          <div class="p-6 h-[500px] overflow-y-auto font-mono text-sm text-gray-100 leading-relaxed whitespace-pre-wrap bg-purple-900/10">
            {{ adaptedText }}
          </div>
        </div>

      </div>

      <div class="flex justify-end border-t border-gray-800 pt-8">
        <button 
          @click="proceedToVisuals" 
          class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white px-8 py-3 rounded-xl font-bold text-lg transition-all shadow-lg shadow-purple-500/25 flex items-center gap-2"
        >
          Approve & Proceed to Visuals
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </button>
      </div>
    </div>
  </div>
</template>
