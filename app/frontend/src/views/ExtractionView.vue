<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const projectId = localStorage.getItem('project_id')

const characters = ref([])
const continuityWarnings = ref([])
const isLoading = ref(true)
const editingChar = ref(null)

onMounted(async () => {
  if (!projectId) return router.push('/')
  try {
    const res = await fetch(`http://localhost:8000/api/state/${projectId}`)
    if (!res.ok) throw new Error("Failed to fetch state")
    const data = await res.json()
    // Map backend LLM extraction to UI model
    characters.value = data.characters || []
    continuityWarnings.value = data.continuity_results || []
  } catch(e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const approveAll = () => {
  characters.value.forEach(c => c.status = 'approved')
}

const openEditModal = (char) => {
  editingChar.value = { 
    ...char, 
    canonical_name: char.canonical_name || char.name || '',
    aliases_str: char.aliases ? char.aliases.join(', ') : '' 
  }
}

const saveEdit = () => {
  if (!editingChar.value) return
  const target = characters.value.find(c => 
    (c.character_id || c.id) === (editingChar.value.character_id || editingChar.value.id)
  )
  if (target) {
    target.canonical_name = editingChar.value.canonical_name
    target.name = editingChar.value.canonical_name
    target.aliases = editingChar.value.aliases_str.split(',').map(s => s.trim()).filter(Boolean)
    target.role = editingChar.value.role
    target.status = 'approved'
  }
  editingChar.value = null
}

const cancelEdit = () => {
  editingChar.value = null
}

const proceedToAdaptation = async () => {
  try {
    await fetch(`http://localhost:8000/api/approve/${projectId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gate_name: 'extract', approved: true })
    })
    router.push('/adaptation')
  } catch(e) {
    alert("Error approving gate")
  }
}
</script>

<template>
  <div class="max-w-6xl mx-auto py-8 px-6">
    <div class="mb-8 flex justify-between items-end">
      <div>
        <h1 class="text-3xl font-bold text-gray-100 mb-2">Extraction Review (Gate 1)</h1>
        <p class="text-gray-400">Review canonical entities, merge duplicates, and resolve continuity warnings before cultural adaptation.</p>
      </div>
      <button 
        @click="proceedToAdaptation"
        class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
      >
        Approve & Proceed
      </button>
    </div>

    <!-- Continuity Warnings Alert -->
    <div v-if="continuityWarnings.length > 0" class="bg-red-500/10 border border-red-500/50 rounded-lg p-4 mb-8">
      <div class="flex items-center gap-2 text-red-400 mb-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <h3 class="font-bold">Continuity Contradictions Detected</h3>
      </div>
      <ul class="list-disc list-inside text-sm text-red-300/80">
        <li v-for="warning in continuityWarnings" :key="warning.id">
          <span class="font-mono text-red-400">{{ warning.scene }}</span>: {{ warning.message }}
        </li>
      </ul>
    </div>

    <!-- Canonical Characters Table -->
    <div class="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
      <div class="p-4 border-b border-gray-700 flex justify-between items-center bg-gray-800/80">
        <h2 class="text-lg font-bold text-gray-200">Extracted Characters</h2>
        <button @click="approveAll" class="text-sm text-purple-400 hover:text-purple-300 font-medium">Approve All</button>
      </div>
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-900/50 text-gray-400 text-sm">
            <th class="p-4 font-medium">Canonical ID</th>
            <th class="p-4 font-medium">Name</th>
            <th class="p-4 font-medium">Aliases to Merge</th>
            <th class="p-4 font-medium">Role</th>
            <th class="p-4 font-medium">Status</th>
            <th class="p-4 font-medium text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="text-sm divide-y divide-gray-700/50">
          <tr v-for="char in characters" :key="char.id" class="hover:bg-gray-800/30 transition-colors">
            <td class="p-4 font-mono text-xs text-purple-400">{{ char.character_id || char.id }}</td>
            <td class="p-4 text-gray-200 font-medium">{{ char.canonical_name || char.name }}</td>
            <td class="p-4 text-gray-400">{{ char.aliases ? char.aliases.join(', ') : 'None' }}</td>
            <td class="p-4 text-gray-400">{{ char.role }}</td>
            <td class="p-4">
              <span :class="[
                'px-2 py-1 rounded text-xs font-medium',
                char.status === 'approved' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
              ]">
                {{ char.status || 'pending' }}
              </span>
            </td>
            <td class="p-4 text-right">
              <button @click="openEditModal(char)" class="text-gray-400 hover:text-white transition-colors">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Character Modal -->
    <div v-if="editingChar" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-gray-800 border border-gray-700 rounded-xl w-full max-w-md p-6 shadow-2xl">
        <h2 class="text-xl font-bold text-gray-100 mb-4">Edit Character</h2>
        
        <div class="space-y-4 mb-6">
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Canonical Name</label>
            <input v-model="editingChar.canonical_name" type="text" class="w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-gray-200 focus:outline-none focus:border-purple-500" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Aliases (comma separated)</label>
            <input v-model="editingChar.aliases_str" type="text" class="w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-gray-200 focus:outline-none focus:border-purple-500" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Role</label>
            <input v-model="editingChar.role" type="text" class="w-full bg-gray-900 border border-gray-700 rounded px-3 py-2 text-gray-200 focus:outline-none focus:border-purple-500" />
          </div>
        </div>
        
        <div class="flex justify-end gap-3">
          <button @click="cancelEdit" class="px-4 py-2 text-gray-400 hover:text-gray-200 font-medium">Cancel</button>
          <button @click="saveEdit" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded font-medium transition-colors">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>
