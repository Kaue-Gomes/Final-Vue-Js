<template>
  <Transition name="fade">
    <div v-if="show" class="loading-overlay">
      <div class="loading-content">
        <LoadingSpinner size="large" />
        <p v-if="mensagem" class="loading-mensagem">{{ mensagem }}</p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import LoadingSpinner from './LoadingSpinner.vue'

defineProps({
  show: {
    type: Boolean,
    default: false
  },
  mensagem: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: var(--bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
}

.loading-mensagem {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

