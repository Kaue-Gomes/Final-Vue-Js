<template>
  <div class="produto-form-page">
    <div class="page-header">
      <router-link to="/produtos" class="btn btn-secondary">
        <i class="bi bi-arrow-left"></i>
        Voltar
      </router-link>
      <h1>Editar Produto</h1>
    </div>

    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner size="large" />
    </div>

    <div v-else-if="produto" class="produto-form-container">
      <ProdutoForm :produto="produto" @submit="handleSubmit" @cancel="cancelar" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProdutosStore } from '@/store/produtos'
import { useUIStore } from '@/store/ui'
import ProdutoForm from '@/components/produtos/ProdutoForm.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const produtosStore = useProdutosStore()
const uiStore = useUIStore()

const produto = ref(null)
const isLoading = ref(true)

onMounted(async () => {
  const id = parseInt(route.params.id)
  await produtosStore.buscarProduto(id)
  produto.value = produtosStore.produtoAtual
  isLoading.value = false
})

const handleSubmit = async (produtoData) => {
  const result = await produtosStore.atualizarProduto(produtoData.id, produtoData)
  
  if (result.success) {
    uiStore.adicionarToast({
      tipo: 'success',
      mensagem: 'Produto atualizado com sucesso!'
    })
    router.push('/produtos')
  } else {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: result.error || 'Erro ao atualizar produto'
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

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
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

