<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const projectId = localStorage.getItem('project_id')
const visualPrompts = ref([])
const isLoading = ref(true)

onMounted(async () => {
  if (!projectId) return router.push('/')
  try {
    const res = await fetch(`http://localhost:8000/api/state/${projectId}`)
    const data = await res.json()
    const prompts = data.visual_prompts || []
    
    visualPrompts.value = prompts
  } catch(e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const generateImage = async (promptObj) => {
  promptObj.status = 'generating'
  // Simulate image generation latency before showing the result
  await new Promise(r => setTimeout(r, 2000))
  promptObj.status = 'completed'
  // Use Pollinations AI for dynamic, keyless, on-the-fly image generation based on the actual prompt text
  const encodedPrompt = encodeURIComponent(promptObj.prompt || 'Cinematic movie scene')
  promptObj.generatedImage = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=1024&height=576&nologo=true`
}
</script>

<template>
  <div class="max-w-6xl mx-auto py-8 px-6">
    <div class="mb-8 flex justify-between items-end">
      <div>
        <h1 class="text-3xl font-bold text-gray-100 mb-2">Visual Prompt Builder (Gate 3)</h1>
        <p class="text-gray-400">Review canonical references and the LLM-generated prompt before spending compute on image generation. You can regenerate individual failed assets here.</p>
      </div>
      <button 
        @click="router.push('/export')"
        class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-medium transition-colors whitespace-nowrap"
      >
        Proceed to Export
      </button>
    </div>

    <div class="space-y-8">
      <div v-for="item in visualPrompts" :key="item.id" class="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
        
        <!-- Header -->
        <div class="p-4 border-b border-gray-700 bg-gray-900/50 flex justify-between items-center">
          <div class="flex items-center gap-3">
            <h2 class="font-bold text-lg text-gray-200">Scene {{ item.scene }} Keyframe</h2>
            <span class="px-2 py-1 bg-gray-800 rounded text-xs font-mono text-purple-400">{{ item.id }}</span>
          </div>
          <span :class="[
            'px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider',
            item.status === 'completed' ? 'bg-green-500/20 text-green-400' : 
            item.status === 'generating' ? 'bg-yellow-500/20 text-yellow-400 animate-pulse' : 
            'bg-gray-700 text-gray-300'
          ]">
            {{ item.status }}
          </span>
        </div>

        <div class="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <!-- Canonical Inputs & Prompt -->
          <div>
            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-3">Canonical References</h3>
            <div class="flex flex-wrap gap-2 mb-6">
              <div v-for="ref in item.canonicalReferences" :key="ref.id" class="bg-gray-900 border border-gray-700 rounded p-2 text-xs">
                <span class="font-bold text-gray-300 block mb-1">{{ ref.type }}</span>
                <span class="text-purple-400 font-mono">{{ ref.id }}</span>
              </div>
            </div>

            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-3">Generated Prompt</h3>
            <textarea 
              v-model="item.prompt" 
              rows="4" 
              class="w-full bg-gray-900 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 mb-4"
            ></textarea>
            
            <div class="flex gap-3">
              <button 
                v-if="item.status !== 'completed'"
                @click="generateImage(item)" 
                class="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg font-medium transition-colors"
              >
                Approve & Generate Image
              </button>
              <button 
                v-else
                @click="generateImage(item)" 
                class="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg font-medium transition-colors"
              >
                Retry / Regenerate Asset
              </button>
            </div>
          </div>

          <!-- Output Preview -->
          <div class="bg-gray-900/50 rounded-lg border border-gray-700 flex items-center justify-center min-h-[300px] overflow-hidden">
            <img v-if="item.generatedImage" :src="item.generatedImage" alt="Generated Scene" class="w-full h-full object-cover">
            <div v-else class="text-center text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              <p>Image will appear here after generation</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
