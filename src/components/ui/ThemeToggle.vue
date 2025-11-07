<template>
  <button class="theme-toggle" @click="alternarTema" :aria-label="`Alternar para tema ${isDark ? 'claro' : 'escuro'}`">
    <i :class="iconClass"></i>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useUIStore } from '@/store/ui'

const uiStore = useUIStore()

const isDark = computed(() => uiStore.isDarkMode)

const iconClass = computed(() => 
  isDark.value ? 'bi bi-sun-fill' : 'bi bi-moon-fill'
)

const alternarTema = () => {
  uiStore.alternarTema()
}
</script>

<style scoped>
.theme-toggle {
  background: var(--bg-secondary);
  border: none;
  color: var(--text-primary);
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.1rem;
}

.theme-toggle:hover {
  background: var(--bg-tertiary);
  transform: scale(1.05);
}

.theme-toggle:active {
  transform: scale(0.95);
}
</style>

