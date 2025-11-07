<template>
  <div class="produto-detalhes-page">
    <div class="page-header">
      <router-link to="/produtos" class="btn btn-secondary">
        <i class="bi bi-arrow-left"></i>
        Voltar para Produtos
      </router-link>
    </div>

    <ProdutoDetalhes
      :produto="produto"
      :is-loading="isLoading"
      @deletar="confirmarDeletar"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProdutosStore } from '@/store/produtos'
import { useUIStore } from '@/store/ui'
import ProdutoDetalhes from '@/components/produtos/ProdutoDetalhes.vue'

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

  if (!produto.value) {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: 'Produto não encontrado'
    })
  }
})

const confirmarDeletar = (id) => {
  uiStore.abrirConfirmDialog({
    titulo: 'Confirmar Exclusão',
    mensagem: 'Tem certeza que deseja excluir este produto? Esta ação não pode ser desfeita.',
    onConfirm: async () => {
      const result = await produtosStore.deletarProduto(id)
      if (result.success) {
        uiStore.adicionarToast({
          tipo: 'success',
          mensagem: 'Produto excluído com sucesso!'
        })
        router.push('/produtos')
      } else {
        uiStore.adicionarToast({
          tipo: 'error',
          mensagem: result.error || 'Erro ao excluir produto'
        })
      }
    }
  })
}
</script>

<style scoped>
.produto-detalhes-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

@media (max-width: 768px) {
  .produto-detalhes-page {
    padding: 1rem;
  }
}
</style>

