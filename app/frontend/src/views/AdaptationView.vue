<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const projectId = localStorage.getItem('project_id')
const culturalDecisions = ref([])
const isLoading = ref(true)

onMounted(async () => {
  if (!projectId) return router.push('/')
  try {
    const res = await fetch(`http://localhost:8000/api/state/${projectId}`)
    const data = await res.json()
    const rawRules = data.adaptation_plan?.adaptations || []
    const rules = rawRules.map((r, i) => ({
      id: `RULE_${i+1}`,
      category: r.category || 'GENERAL',
      sourceText: r.source || 'N/A',
      adaptedText: r.adapted || '',
      reason: r.reason || '',
      evidence: 'RAG Context',
      confidence: 'LOW'
    }))
    
    culturalDecisions.value = rules
  } catch(e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const acceptDecision = (decision) => {
  decision.confidence = 'HIGH'
}

const rejectDecision = (decision) => {
  culturalDecisions.value = culturalDecisions.value.filter(d => d.id !== decision.id)
}

const editDecision = (decision) => {
  const newText = prompt("Edit the adapted text:", decision.adaptedText)
  if (newText !== null && newText.trim() !== "") {
    decision.adaptedText = newText.trim()
    decision.confidence = 'HIGH'
  }
}

const proceedToVisuals = async () => {
  try {
    await fetch(`http://localhost:8000/api/approve/${projectId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gate_name: 'adaptation', approved: true })
    })
    router.push('/screenplay')
  } catch(e) {
    alert("Error approving gate")
  }
}
</script>

<template>
  <div class="max-w-6xl mx-auto py-8 px-6">
    <div class="mb-8 flex justify-between items-end">
      <div>
        <h1 class="text-3xl font-bold text-gray-100 mb-2">Cultural Plan Approval (Gate 2)</h1>
        <p class="text-gray-400">Review the LLM's cultural adaptation decisions. Pay special attention to low confidence items.</p>
      </div>
      <button 
        @click="proceedToVisuals"
        class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        Approve Plan & Proceed to Screenplay
      </button>
    </div>

    <!-- Adaptation Decisions Table -->
    <div class="space-y-6">
      <div v-for="decision in culturalDecisions" :key="decision.id" 
        :class="[
          'rounded-xl border p-6 transition-all',
          decision.confidence === 'LOW' ? 'bg-yellow-500/10 border-yellow-500/50' : 'bg-gray-800/50 border-gray-700'
        ]">
        
        <div class="flex justify-between items-start mb-4">
          <div class="flex items-center gap-3">
            <span class="px-2 py-1 bg-gray-900 rounded text-xs font-mono text-purple-400">{{ decision.id }}</span>
            <span class="px-2 py-1 bg-gray-700 rounded text-xs font-bold text-gray-200">{{ decision.category }}</span>
            
            <span v-if="decision.confidence === 'LOW'" class="flex items-center gap-1 text-xs font-bold text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              CULTURAL UNCERTAINTY
            </span>
          </div>
          
          <div v-if="decision.confidence === 'LOW'" class="flex gap-2">
            <button @click="acceptDecision(decision)" class="px-3 py-1 bg-green-600 hover:bg-green-500 text-white text-sm rounded transition-colors">Accept</button>
            <button @click="editDecision(decision)" class="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded transition-colors">Edit</button>
            <button @click="rejectDecision(decision)" class="px-3 py-1 bg-red-600 hover:bg-red-500 text-white text-sm rounded transition-colors">Reject</button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-6 mb-4">
          <div class="bg-gray-900/50 p-4 rounded-lg border border-gray-700/50">
            <p class="text-xs text-gray-500 mb-1 font-bold uppercase">Source Concept</p>
            <p class="text-gray-300 font-medium">"{{ decision.sourceText }}"</p>
          </div>
          <div class="bg-purple-900/20 p-4 rounded-lg border border-purple-500/30">
            <p class="text-xs text-purple-400 mb-1 font-bold uppercase">Adapted Implementation</p>
            <p class="text-gray-100 font-bold">"{{ decision.adaptedText }}"</p>
          </div>
        </div>
        
        <div class="text-sm text-gray-400 bg-gray-900/30 p-3 rounded flex flex-col gap-2">
          <p><strong class="text-gray-300">Reasoning:</strong> {{ decision.reason }}</p>
          <p><strong class="text-gray-300">Evidence Citation:</strong> <span class="font-mono text-xs">{{ decision.evidence }}</span></p>
        </div>
      </div>
    </div>
  </div>
</template>
