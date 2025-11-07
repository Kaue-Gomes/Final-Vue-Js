<template>
  <div class="toast-container">
    <ToastNotification
      v-for="toast in toasts"
      :key="toast.id"
      :tipo="toast.tipo"
      :titulo="toast.titulo"
      :mensagem="toast.mensagem"
      :show="true"
      @close="removerToast(toast.id)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUIStore } from '@/store/ui'
import ToastNotification from './ToastNotification.vue'

const uiStore = useUIStore()

const toasts = computed(() => uiStore.toasts)

const removerToast = (id) => {
  uiStore.removerToast(id)
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
}

@media (max-width: 768px) {
  .toast-container {
    top: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
  }
  
  .toast-container > * {
    max-width: 100%;
  }
}
</style>

