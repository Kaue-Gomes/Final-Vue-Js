<template>
  <Transition name="toast">
    <div v-if="show" class="toast" :class="tipo" @click="$emit('close')">
      <div class="toast-icon">
        <i :class="iconClass"></i>
      </div>
      <div class="toast-content">
        <div v-if="titulo" class="toast-titulo">{{ titulo }}</div>
        <div class="toast-mensagem">{{ mensagem }}</div>
      </div>
      <button class="toast-close" @click.stop="$emit('close')">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tipo: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  titulo: String,
  mensagem: String,
  show: {
    type: Boolean,
    default: true
  }
})

defineEmits(['close'])

const iconClass = computed(() => {
  const icons = {
    success: 'bi bi-check-circle-fill',
    error: 'bi bi-x-circle-fill',
    warning: 'bi bi-exclamation-triangle-fill',
    info: 'bi bi-info-circle-fill'
  }
  return icons[props.tipo] || icons.info
})
</script>

<style scoped>
.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  min-width: 300px;
  max-width: 400px;
  background: var(--bg-primary);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: transform 0.2s ease;
  border-left: 4px solid;
}

.toast:hover {
  transform: translateY(-2px);
}

.toast.success {
  border-left-color: var(--color-success);
}

.toast.error {
  border-left-color: var(--color-danger);
}

.toast.warning {
  border-left-color: var(--color-warning);
}

.toast.info {
  border-left-color: var(--color-info);
}

.toast-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.toast.success .toast-icon {
  color: var(--color-success);
}

.toast.error .toast-icon {
  color: var(--color-danger);
}

.toast.warning .toast-icon {
  color: var(--color-warning);
}

.toast.info .toast-icon {
  color: var(--color-info);
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-titulo {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.toast-mensagem {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.toast-close:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.2s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>

