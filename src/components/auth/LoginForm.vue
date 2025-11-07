<template>
  <form class="login-form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        type="email"
        class="form-control"
        :class="{ 'is-invalid': errors.email }"
        placeholder="seu@email.com"
        required
      />
      <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
    </div>

    <div class="form-group">
      <label for="senha">Senha</label>
      <input
        id="senha"
        v-model="senha"
        type="password"
        class="form-control"
        :class="{ 'is-invalid': errors.senha }"
        placeholder="••••••••"
        required
      />
      <div v-if="errors.senha" class="invalid-feedback">{{ errors.senha }}</div>
    </div>

    <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
      <span v-if="isLoading">Entrando...</span>
      <span v-else>Entrar</span>
    </button>

    <div class="form-footer">
      <p>
        Não tem uma conta?
        <a href="#" @click.prevent="$emit('toggle-mode')">Registrar-se</a>
      </p>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'
import { validarEmail } from '@/utils/validators'

const emit = defineEmits(['toggle-mode', 'success'])

const authStore = useAuthStore()
const uiStore = useUIStore()

const email = ref('')
const senha = ref('')
const errors = ref({})
const isLoading = ref(false)

const handleSubmit = async () => {
  errors.value = {}
  
  if (!validarEmail(email.value)) {
    errors.value.email = 'Email inválido'
    return
  }
  
  if (!senha.value || senha.value.length < 6) {
    errors.value.senha = 'Senha deve ter no mínimo 6 caracteres'
    return
  }
  
  isLoading.value = true
  
  const result = await authStore.login(email.value, senha.value)
  
  isLoading.value = false
  
  if (result.success) {
    uiStore.adicionarToast({
      tipo: 'success',
      mensagem: 'Login realizado com sucesso!'
    })
    emit('success')
  } else {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: result.error || 'Erro ao fazer login'
    })
  }
}
</script>

<style scoped>
.login-form {
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
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

.form-control.is-invalid {
  border-color: var(--color-danger);
}

.invalid-feedback {
  display: block;
  margin-top: 0.5rem;
  color: var(--color-danger);
  font-size: 0.875rem;
}

.btn-block {
  width: 100%;
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.form-footer p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.form-footer a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>

