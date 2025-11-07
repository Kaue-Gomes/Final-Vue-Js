<template>
  <div class="perfil-page">
    <div class="page-header">
      <h1>Meu Perfil</h1>
      <p>Gerencie suas informações pessoais</p>
    </div>

    <div class="perfil-content">
      <div class="perfil-card">
        <div class="perfil-header">
          <div class="perfil-avatar">
            {{ nomeInicial }}
          </div>
          <div class="perfil-info">
            <h2>{{ nomeUsuario }}</h2>
            <p>{{ emailUsuario }}</p>
          </div>
        </div>

        <form class="perfil-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="nome">Nome</label>
            <input
              id="nome"
              v-model="formData.nome"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-control"
              required
            />
          </div>

          <div class="form-group">
            <label for="senha">Nova Senha (deixe em branco para manter)</label>
            <input
              id="senha"
              v-model="formData.senha"
              type="password"
              class="form-control"
              placeholder="••••••••"
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              <span v-if="isLoading">Salvando...</span>
              <span v-else>Salvar Alterações</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'

const authStore = useAuthStore()
const uiStore = useUIStore()

const formData = ref({
  nome: '',
  email: '',
  senha: ''
})
const isLoading = ref(false)

const nomeUsuario = computed(() => authStore.nomeUsuario)
const emailUsuario = computed(() => authStore.emailUsuario)
const nomeInicial = computed(() => nomeUsuario.value.charAt(0).toUpperCase())

onMounted(() => {
  formData.value = {
    nome: nomeUsuario.value,
    email: emailUsuario.value,
    senha: ''
  }
})

const handleSubmit = async () => {
  isLoading.value = true
  
  const dados = {
    nome: formData.value.nome,
    email: formData.value.email
  }
  
  if (formData.value.senha) {
    dados.senha = formData.value.senha
  }
  
  const result = await authStore.atualizarPerfil(dados)
  
  isLoading.value = false
  
  if (result.success) {
    uiStore.adicionarToast({
      tipo: 'success',
      mensagem: 'Perfil atualizado com sucesso!'
    })
  } else {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: result.error || 'Erro ao atualizar perfil'
    })
  }
}
</script>

<style scoped>
.perfil-page {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.page-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
}

.perfil-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
}

.perfil-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
}

.perfil-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  flex-shrink: 0;
}

.perfil-info h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.perfil-info p {
  margin: 0;
  color: var(--text-secondary);
}

.perfil-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  margin-top: 1rem;
}
</style>

