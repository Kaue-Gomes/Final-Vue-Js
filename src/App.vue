<template>
  <div id="app">
    <NavBar />
    
    <div class="app-container">
      <Sidebar v-if="isAuthenticated" />
      
      <main class="app-main">
        <div class="app-content">
          <RouterView v-slot="{ Component }">
            <Transition name="fade" mode="out-in">
              <component :is="Component" />
            </Transition>
          </RouterView>
        </div>
        <Footer v-if="isAuthenticated" />
      </main>
    </div>

    <ToastContainer />
    <ConfirmDialog />
    <LoadingOverlay :show="uiStore.loading" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'
import NavBar from '@/components/ui/NavBar.vue'
import Sidebar from '@/components/ui/Sidebar.vue'
import Footer from '@/components/ui/Footer.vue'
import ToastContainer from '@/components/ui/ToastContainer.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import LoadingOverlay from '@/components/ui/LoadingOverlay.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  uiStore.inicializarTema()
  authStore.verificarAutenticacao()
})
</script>

<style>
@import './styles/main.css';
</style>

