<template>
  <form class="produto-form" @submit.prevent="handleSubmit">
    <div class="form-row">
      <div class="form-group">
        <label for="nome">Nome do Produto *</label>
        <input
          id="nome"
          v-model="formData.nome"
          type="text"
          class="form-control"
          :class="{ 'is-invalid': errors.nome }"
          placeholder="Ex: Notebook Dell"
          required
        />
        <div v-if="errors.nome" class="invalid-feedback">{{ errors.nome }}</div>
      </div>

      <div class="form-group">
        <label for="categoria">Categoria</label>
        <select
          id="categoria"
          v-model="formData.categoria"
          class="form-control"
        >
          <option value="">Selecione uma categoria</option>
          <option v-for="cat in categorias" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label for="descricao">Descrição</label>
      <textarea
        id="descricao"
        v-model="formData.descricao"
        class="form-control"
        rows="4"
        placeholder="Descreva o produto..."
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="preco">Preço *</label>
        <input
          id="preco"
          v-model.number="formData.preco"
          type="number"
          step="0.01"
          min="0"
          class="form-control"
          :class="{ 'is-invalid': errors.preco }"
          placeholder="0.00"
          required
        />
        <div v-if="errors.preco" class="invalid-feedback">{{ errors.preco }}</div>
      </div>

      <div class="form-group">
        <label for="estoque">Estoque</label>
        <input
          id="estoque"
          v-model.number="formData.estoque"
          type="number"
          min="0"
          class="form-control"
          :class="{ 'is-invalid': errors.estoque }"
          placeholder="0"
        />
        <div v-if="errors.estoque" class="invalid-feedback">{{ errors.estoque }}</div>
      </div>
    </div>

    <div class="form-group">
      <label for="imagem_url">URL da Imagem</label>
      <input
        id="imagem_url"
        v-model="formData.imagem_url"
        type="url"
        class="form-control"
        placeholder="https://exemplo.com/imagem.jpg"
      />
      <small class="form-text">Cole a URL de uma imagem do produto</small>
    </div>

    <div v-if="formData.imagem_url" class="form-group">
      <label>Preview da Imagem</label>
      <div class="image-preview">
        <img :src="getImageUrl(formData.imagem_url)" alt="Preview" />
      </div>
    </div>

    <div class="form-group">
      <label class="checkbox-label">
        <input
          v-model="formData.ativo"
          type="checkbox"
        />
        <span>Produto ativo</span>
      </label>
    </div>

    <div class="form-actions">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Cancelar
      </button>
      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        <span v-if="isLoading">Salvando...</span>
        <span v-else>{{ produtoId ? 'Atualizar' : 'Criar' }} Produto</span>
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { validarPreco, validarEstoque, validarNome } from '@/utils/validators'
import { CATEGORIAS_PADRAO } from '@/utils/constants'

const getImageUrl = (url) => {
  if (!url) return 'https://via.placeholder.com/300x300?text=Sem+Imagem'
  if (url.startsWith('http')) return url
  return url
}

const props = defineProps({
  produto: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({
  nome: '',
  descricao: '',
  preco: 0,
  estoque: 0,
  categoria: '',
  imagem_url: '',
  ativo: true
})

const errors = ref({})
const isLoading = ref(false)
const categorias = ref(CATEGORIAS_PADRAO)
const produtoId = ref(null)

watch(() => props.produto, (newProduto) => {
  if (newProduto) {
    produtoId.value = newProduto.id
    formData.value = {
      nome: newProduto.nome || '',
      descricao: newProduto.descricao || '',
      preco: newProduto.preco || 0,
      estoque: newProduto.estoque || 0,
      categoria: newProduto.categoria || '',
      imagem_url: newProduto.imagem_url || '',
      ativo: newProduto.ativo !== undefined ? newProduto.ativo : true
    }
  }
}, { immediate: true })

const handleSubmit = () => {
  errors.value = {}
  
  if (!validarNome(formData.value.nome)) {
    errors.value.nome = 'Nome deve ter no mínimo 2 caracteres'
    return
  }
  
  if (!validarPreco(formData.value.preco)) {
    errors.value.preco = 'Preço deve ser um número positivo'
    return
  }
  
  if (!validarEstoque(formData.value.estoque)) {
    errors.value.estoque = 'Estoque deve ser um número inteiro positivo'
    return
  }
  
  emit('submit', {
    ...formData.value,
    id: produtoId.value
  })
}
</script>

<style scoped>
.produto-form {
  max-width: 800px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
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
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-control.is-invalid {
  border-color: var(--color-danger);
}

textarea.form-control {
  resize: vertical;
  min-height: 100px;
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

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.image-preview {
  margin-top: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}
</style>

