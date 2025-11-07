<template>
  <form class="register-form" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="nome">Nome</label>
      <input
        id="nome"
        v-model="nome"
        type="text"
        class="form-control"
        :class="{ 'is-invalid': errors.nome }"
        placeholder="Seu nome completo"
        required
      />
      <div v-if="errors.nome" class="invalid-feedback">{{ errors.nome }}</div>
    </div>

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
      <small class="form-text">Mínimo de 6 caracteres</small>
    </div>

    <div class="form-group">
      <label for="confirmarSenha">Confirmar Senha</label>
      <input
        id="confirmarSenha"
        v-model="confirmarSenha"
        type="password"
        class="form-control"
        :class="{ 'is-invalid': errors.confirmarSenha }"
        placeholder="••••••••"
        required
      />
      <div v-if="errors.confirmarSenha" class="invalid-feedback">{{ errors.confirmarSenha }}</div>
    </div>

    <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
      <span v-if="isLoading">Registrando...</span>
      <span v-else>Registrar</span>
    </button>

    <div class="form-footer">
      <p>
        Já tem uma conta?
        <a href="#" @click.prevent="$emit('toggle-mode')">Entrar</a>
      </p>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useUIStore } from '@/store/ui'
import { validarEmail, validarNome } from '@/utils/validators'

const emit = defineEmits(['toggle-mode', 'success'])

const authStore = useAuthStore()
const uiStore = useUIStore()

const nome = ref('')
const email = ref('')
const senha = ref('')
const confirmarSenha = ref('')
const errors = ref({})
const isLoading = ref(false)

const handleSubmit = async () => {
  errors.value = {}
  
  if (!validarNome(nome.value)) {
    errors.value.nome = 'Nome deve ter no mínimo 2 caracteres'
    return
  }
  
  if (!validarEmail(email.value)) {
    errors.value.email = 'Email inválido'
    return
  }
  
  if (!senha.value || senha.value.length < 6) {
    errors.value.senha = 'Senha deve ter no mínimo 6 caracteres'
    return
  }
  
  if (senha.value !== confirmarSenha.value) {
    errors.value.confirmarSenha = 'As senhas não coincidem'
    return
  }
  
  isLoading.value = true
  
  const result = await authStore.register({
    nome: nome.value,
    email: email.value,
    senha: senha.value
  })
  
  isLoading.value = false
  
  if (result.success) {
    uiStore.adicionarToast({
      tipo: 'success',
      mensagem: 'Registro realizado com sucesso!'
    })
    emit('success')
  } else {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: result.error || 'Erro ao registrar'
    })
  }
}
</script>

<style scoped>
.register-form {
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

.form-text {
  display: block;
  margin-top: 0.5rem;
  color: var(--text-tertiary);
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

