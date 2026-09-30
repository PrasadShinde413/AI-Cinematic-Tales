<script setup>
import { computed } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const currentStep = computed(() => {
  if (route.path.includes('/extraction')) return 2
  if (route.path.includes('/adaptation')) return 3
  if (route.path.includes('/screenplay')) return 4
  if (route.path.includes('/visuals') || route.path.includes('/export')) return 5
  return 1
})

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-gray-100 font-sans selection:bg-purple-500/30">
    <!-- Navbar -->
    <nav class="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-3">
            <div @click="goHome" class="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center cursor-pointer hover:shadow-lg hover:shadow-purple-500/30 transition-all">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"></path></svg>
            </div>
            <span @click="goHome" class="font-bold text-xl tracking-tight cursor-pointer hover:text-purple-400 transition-colors">Adaptation Studio</span>
            
            <!-- Navigation Buttons -->
            <div class="flex items-center gap-4 ml-4 pl-4 border-l border-gray-700">
              <button @click="goBack" class="flex items-center gap-1.5 text-sm font-medium text-gray-400 hover:text-white transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                Back
              </button>
              <button @click="goHome" class="flex items-center gap-1.5 text-sm font-medium text-gray-400 hover:text-white transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
                Home
              </button>
            </div>
          </div>
          
          <!-- Dynamic Progress Stepper -->
          <div class="hidden md:flex items-center space-x-2 text-sm font-medium transition-all duration-300">
            <span :class="currentStep === 1 ? 'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.9)]' : currentStep > 1 ? 'text-purple-400/70' : 'text-gray-600'">1. Upload</span>
            <span class="text-gray-700">→</span>
            
            <span :class="currentStep === 2 ? 'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.9)] transition-all' : currentStep > 2 ? 'text-purple-400/70' : 'text-gray-600'">2. Extract</span>
            <span class="text-gray-700">→</span>
            
            <span :class="currentStep === 3 ? 'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.9)] transition-all' : currentStep > 3 ? 'text-purple-400/70' : 'text-gray-600'">3. Adapt</span>
            <span class="text-gray-700">→</span>
            
            <span :class="currentStep === 4 ? 'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.9)] transition-all' : currentStep > 4 ? 'text-purple-400/70' : 'text-gray-600'">4. Script</span>
            <span class="text-gray-700">→</span>
            
            <span :class="currentStep >= 5 ? 'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.9)] transition-all' : 'text-gray-600'">5. Visuals</span>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="relative">
      <!-- Decorative background blur -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-purple-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      
      <div class="relative z-10">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
