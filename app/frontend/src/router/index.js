import { createRouter, createWebHistory } from 'vue-router'
import UploadView from '../views/UploadView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'upload',
      component: UploadView
    },
    {
      path: '/extraction',
      name: 'extraction',
      // route level code-splitting
      component: () => import('../views/ExtractionView.vue')
    },
    {
      path: '/adaptation',
      name: 'adaptation',
      component: () => import('../views/AdaptationView.vue')
    },
    {
      path: '/screenplay',
      name: 'screenplay',
      component: () => import('../views/ScreenplayView.vue')
    },
    {
      path: '/visuals',
      name: 'visuals',
      component: () => import('../views/VisualsView.vue')
    },
    {
      path: '/export',
      name: 'export',
      component: () => import('../views/ExportView.vue')
    }
  ]
})

export default router
