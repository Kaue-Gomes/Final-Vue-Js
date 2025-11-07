<template>
  <Transition name="sidebar">
    <div v-if="aberto" class="sidebar-overlay" @click="fecharSidebar">
      <aside class="sidebar" @click.stop>
        <div class="sidebar-header">
          <h3>Menu</h3>
          <button class="sidebar-close" @click="fecharSidebar">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        
        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.to"
            :to="item.to"
            class="sidebar-item"
            @click="fecharSidebar"
          >
            <i :class="item.icon"></i>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
      </aside>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'

const authStore = useAuthStore()
const uiStore = useUIStore()

const aberto = computed(() => uiStore.sidebarAberto)

const menuItems = computed(() => {
  if (!authStore.isAuthenticated) return []
  
  return [
    { to: '/produtos', label: 'Gestão de Produtos', icon: 'bi bi-box-seam' },
    { to: '/dashboard', label: 'Dashboard', icon: 'bi bi-speedometer2' },
    { to: '/perfil', label: 'Perfil', icon: 'bi bi-person' },
    { to: '/sobre', label: 'Sobre', icon: 'bi bi-info-circle' }
  ]
})

const fecharSidebar = () => {
  uiStore.fecharSidebar()
}
</script>

<style scoped>
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  display: none;
}

@media (max-width: 768px) {
  .sidebar-overlay {
    display: block;
  }
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  z-index: 201;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

@media (min-width: 769px) {
  .sidebar {
    transform: translateX(0);
  }
}

.sidebar-enter-active .sidebar,
.sidebar-leave-active .sidebar {
  transition: transform 0.3s ease;
}

.sidebar-enter-from .sidebar,
.sidebar-leave-to .sidebar {
  transform: translateX(-100%);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.sidebar-close {
  background: none;
  border: none;
  color: var(--text-tertiary);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: none;
}

@media (max-width: 768px) {
  .sidebar-close {
    display: block;
  }
}

.sidebar-close:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.sidebar-item i {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.sidebar-item:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.sidebar-item.router-link-active {
  background: var(--bg-secondary);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
  font-weight: 500;
}
</style>

