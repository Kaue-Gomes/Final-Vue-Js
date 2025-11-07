<template>
  <div class="produtos-page">
    <div class="page-header">
      <div>
        <h1>Produtos</h1>
        <p>Gerencie todos os seus produtos</p>
      </div>
      <div class="page-actions">
        <button
          class="btn btn-secondary"
          type="button"
          :disabled="exportando.csv"
          @click="exportarCSV"
        >
          <i v-if="!exportando.csv" class="bi bi-filetype-csv"></i>
          <i v-else class="bi bi-arrow-repeat spin"></i>
          Exportar CSV
        </button>
        <button
          class="btn btn-secondary"
          type="button"
          :disabled="exportando.pdf"
          @click="exportarPDF"
        >
          <i v-if="!exportando.pdf" class="bi bi-file-earmark-pdf"></i>
          <i v-else class="bi bi-arrow-repeat spin"></i>
          Exportar PDF
        </button>
        <router-link to="/produtos/novo" class="btn btn-primary">
          <i class="bi bi-plus-circle"></i>
          Novo Produto
        </router-link>
      </div>
    </div>

    <div class="produtos-layout">
      <aside class="produtos-sidebar">
        <FiltrosProdutos />
      </aside>

      <main class="produtos-main">
        <div v-if="isLoading" class="loading-container">
          <LoadingSpinner size="large" />
        </div>

        <div v-else-if="produtos.length === 0" class="empty-state">
          <i class="bi bi-box"></i>
          <h3>Nenhum produto encontrado</h3>
          <p>Crie seu primeiro produto para começar</p>
          <router-link to="/produtos/novo" class="btn btn-primary">
            Criar Produto
          </router-link>
        </div>

        <div v-else class="produtos-grid">
          <ProdutoCard
            v-for="produto in produtos"
            :key="produto.id"
            :produto="produto"
            @visualizar="visualizarProduto"
            @editar="editarProduto"
            @deletar="confirmarDeletar"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProdutosStore } from '@/store/produtos'
import { useUIStore } from '@/store/ui'
import ProdutoCard from '@/components/produtos/ProdutoCard.vue'
import FiltrosProdutos from '@/components/produtos/FiltrosProdutos.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const router = useRouter()
const produtosStore = useProdutosStore()
const uiStore = useUIStore()

const produtos = computed(() => produtosStore.produtos)
const isLoading = computed(() => produtosStore.isLoading)
const exportando = reactive({
  csv: false,
  pdf: false
})

onMounted(async () => {
  await carregarProdutos()
})

const carregarProdutos = async () => {
  await produtosStore.listarProdutos()
}

const gerarNomeArquivo = (extensao) => {
  const timestamp = new Date().toISOString().replace(/[:T]/g, '-').split('.')[0]
  return `produtos_${timestamp}.${extensao}`
}

const salvarArquivo = (blob, nomeArquivo) => {
  if (!blob) return
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', nomeArquivo)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

const exportarCSV = async () => {
  if (exportando.csv) return
  exportando.csv = true
  try {
    const arquivo = await produtosStore.exportarCSV()
    if (arquivo) {
      salvarArquivo(arquivo, gerarNomeArquivo('csv'))
      uiStore.adicionarToast({
        tipo: 'success',
        mensagem: 'Exportação CSV iniciada com sucesso!'
      })
    } else {
      uiStore.adicionarToast({
        tipo: 'error',
        mensagem: produtosStore.error || 'Não foi possível exportar o CSV.'
      })
    }
  } catch (error) {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: 'Ocorreu um erro ao exportar o CSV.'
    })
  } finally {
    exportando.csv = false
  }
}

const exportarPDF = async () => {
  if (exportando.pdf) return
  exportando.pdf = true
  try {
    const arquivo = await produtosStore.exportarPDF()
    if (arquivo) {
      salvarArquivo(arquivo, gerarNomeArquivo('pdf'))
      uiStore.adicionarToast({
        tipo: 'success',
        mensagem: 'Exportação PDF iniciada com sucesso!'
      })
    } else {
      uiStore.adicionarToast({
        tipo: 'error',
        mensagem: produtosStore.error || 'Não foi possível exportar o PDF.'
      })
    }
  } catch (error) {
    uiStore.adicionarToast({
      tipo: 'error',
      mensagem: 'Ocorreu um erro ao exportar o PDF.'
    })
  } finally {
    exportando.pdf = false
  }
}

const visualizarProduto = (id) => {
  router.push(`/produtos/${id}`)
}

const editarProduto = (id) => {
  router.push(`/produtos/${id}/editar`)
}

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
        await carregarProdutos()
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
.produtos-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 1rem;
}

.page-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.page-actions .btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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

.produtos-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
}

.produtos-sidebar {
  position: sticky;
  top: 80px;
  height: fit-content;
}

.produtos-main {
  min-height: 400px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 4rem;
  color: var(--text-tertiary);
  margin-bottom: 1rem;
  display: block;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1.5rem;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
}

.produtos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .produtos-layout {
    grid-template-columns: 1fr;
  }

  .produtos-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .produtos-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-actions {
    justify-content: flex-start;
  }

  .produtos-grid {
    grid-template-columns: 1fr;
  }
}
</style>

