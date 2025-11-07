<template>
  <div class="produto-form-page">
    <div class="page-header">
      <router-link to="/produtos" class="btn btn-secondary">
        <i class="bi bi-arrow-left"></i>
        Voltar
      </router-link>
      <h1>Criar Novo Produto</h1>
    </div>

    <div class="produto-form-container">
      <ProdutoForm @submit="handleSubmit" @cancel="cancelar" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useProdutosStore } from '@/store/produtos'
import { useUIStore } from '@/store/ui'
import ProdutoForm from '@/components/produtos/ProdutoForm.vue'

const router = useRouter()
const produtosStore = useProdutosStore()
const uiStore = useUIStore()

const handleSubmit = async (produto) => {
  const result = await produtosStore.criarProduto(produto)
  
  if (result.success) {
    uiStore.adicionarToast({
      tipo: 'success',
      mensagem: 'Produto criado com sucesso!'
    })
    router.push('/produtos')
  } else {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: result.error || 'Erro ao criar produto'
    })
  }
}

const cancelar = () => {
  router.push('/produtos')
}
</script>

<style scoped>
.produto-form-page {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.produto-form-container {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
}

@media (max-width: 768px) {
  .produto-form-page {
    padding: 1rem;
  }

  .produto-form-container {
    padding: 1.5rem;
  }
}
</style>

