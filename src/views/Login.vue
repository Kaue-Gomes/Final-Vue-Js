<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <i class="bi bi-box-seam"></i>
        <h1>Sistema de Produtos</h1>
        <p>Gerencie seus produtos de forma eficiente</p>
      </div>

      <div class="login-card">
        <div class="login-tabs">
          <button
            class="tab-button"
            :class="{ active: modo === 'login' }"
            @click="modo = 'login'"
          >
            Entrar
          </button>
          <button
            class="tab-button"
            :class="{ active: modo === 'register' }"
            @click="modo = 'register'"
          >
            Registrar
          </button>
        </div>

        <div class="login-content">
          <LoginForm
            v-if="modo === 'login'"
            @success="handleSuccess"
            @toggle-mode="modo = 'register'"
          />
          <RegisterForm
            v-else
            @success="handleSuccess"
            @toggle-mode="modo = 'login'"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LoginForm from '@/components/auth/LoginForm.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'

const router = useRouter()
const modo = ref('login')

const handleSuccess = () => {
  router.push('/produtos')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 500px;
}

.login-header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.login-header i {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.login-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
}

.login-header p {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

.login-card {
  background: var(--bg-primary);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
}

.tab-button {
  flex: 1;
  padding: 1rem;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 2px solid transparent;
}

.tab-button:hover {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.tab-button.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.login-content {
  padding: 2rem;
}
</style>

