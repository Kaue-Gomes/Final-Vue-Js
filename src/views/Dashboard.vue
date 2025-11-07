<template>
  <div class="dashboard-page">
    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Visão geral do seu sistema de produtos</p>
    </div>

    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner size="large" />
    </div>

    <div v-else class="dashboard-content">
      <div class="stats-grid">
        <StatCard
          label="Total de Produtos"
          :valor="estatisticas.total_produtos"
          icon="bi bi-box-seam"
          color="#667eea"
          color-dark="#764ba2"
        />
        <StatCard
          label="Valor Total em Estoque"
          :valor="formatCurrency(estatisticas.valor_total_estoque)"
          icon="bi bi-currency-dollar"
          color="#10b981"
          color-dark="#059669"
        />
        <StatCard
          label="Produtos Ativos"
          :valor="estatisticas.produtos_ativos"
          icon="bi bi-check-circle"
          color="#3b82f6"
          color-dark="#2563eb"
        />
        <StatCard
          label="Estoque Baixo"
          :valor="estatisticas.produtos_baixo_estoque"
          icon="bi bi-exclamation-triangle"
          color="#f59e0b"
          color-dark="#d97706"
        />
      </div>

      <div class="dashboard-tabs">
        <button
          class="tab-button"
          :class="{ active: abaAtiva === 'visao' }"
          type="button"
          @click="abaAtiva = 'visao'"
        >
          <i class="bi bi-grid"></i>
          Visão Geral
        </button>
        <button
          class="tab-button"
          :class="{ active: abaAtiva === 'graficos' }"
          type="button"
          @click="abaAtiva = 'graficos'"
        >
          <i class="bi bi-bar-chart-line"></i>
          Gráficos
        </button>
      </div>

      <div v-if="abaAtiva === 'visao'" class="dashboard-sections">
        <div class="dashboard-grid">
          <div class="dashboard-section">
            <h2>Produtos em Destaque</h2>
            <div v-if="produtosDestaque.mais_caros.length" class="produtos-grid">
              <ProdutoCard
                v-for="produto in produtosDestaque.mais_caros"
                :key="produto.id"
                :produto="produto"
                @visualizar="visualizarProduto"
                @editar="editarProduto"
                @deletar="deletarProduto"
              />
            </div>
            <p v-else class="empty-hint">
              Cadastre produtos para vê-los em destaque.
            </p>
          </div>

          <div class="dashboard-section">
            <h2>Produtos com Estoque Baixo</h2>
            <div v-if="produtosDestaque.baixo_estoque.length" class="produtos-grid">
              <ProdutoCard
                v-for="produto in produtosDestaque.baixo_estoque"
                :key="produto.id"
                :produto="produto"
                @visualizar="visualizarProduto"
                @editar="editarProduto"
                @deletar="deletarProduto"
              />
            </div>
            <p v-else class="empty-hint">
              Nenhum produto com estoque crítico no momento.
            </p>
          </div>
        </div>

        <div class="dashboard-section">
          <AtividadeRecente :atividades="atividades" />
        </div>
      </div>

      <div v-else class="graficos-grid">
        <GraficoCategoria :dados="categorias" />
        <GraficoVendas :dados="vendasMensais" />
        <GraficoCrescimento :dados="crescimentoProdutos" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/store/dashboard'
import { useUIStore } from '@/store/ui'
import { formatCurrency } from '@/utils/formatters'
import StatCard from '@/components/dashboard/StatCard.vue'
import AtividadeRecente from '@/components/dashboard/AtividadeRecente.vue'
import ProdutoCard from '@/components/produtos/ProdutoCard.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import GraficoCategoria from '@/components/dashboard/GraficoCategoria.vue'
import GraficoVendas from '@/components/dashboard/GraficoVendas.vue'
import GraficoCrescimento from '@/components/dashboard/GraficoCrescimento.vue'

const router = useRouter()
const dashboardStore = useDashboardStore()
const uiStore = useUIStore()

const isLoading = ref(true)
const abaAtiva = ref('visao')

const estatisticas = computed(() => dashboardStore.estatisticas)
const produtosDestaque = computed(() => dashboardStore.produtosDestaque)
const atividades = computed(() => dashboardStore.atividades)
const categorias = computed(() => dashboardStore.produtosPorCategoria)
const vendasMensais = computed(() => dashboardStore.vendasMensais)
const crescimentoProdutos = computed(() => dashboardStore.crescimentoProdutos)

onMounted(async () => {
  await dashboardStore.carregarTodos()
  isLoading.value = false
})

const editarProduto = (id) => {
  router.push(`/produtos/${id}/editar`)
}

const visualizarProduto = (id) => {
  router.push(`/produtos/${id}`)
}

const deletarProduto = (id) => {
  uiStore.abrirConfirmDialog({
    titulo: 'Confirmar Exclusão',
    mensagem: 'Tem certeza que deseja excluir este produto?',
    onConfirm: async () => {
      // Lógica de exclusão será implementada
      uiStore.adicionarToast({
        tipo: 'success',
        mensagem: 'Produto excluído com sucesso!'
      })
    }
  })
}
</script>

<style scoped>
.dashboard-page {
  padding: 2rem;
  max-width: 1400px;
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

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.dashboard-tabs {
  display: flex;
  gap: 1rem;
  padding: 0.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 999px;
  align-self: flex-start;
}

.tab-button {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-button:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.tab-button.active {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  box-shadow: var(--shadow-md);
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.dashboard-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.empty-hint {
  margin: 0;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

.graficos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.dashboard-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.produtos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .produtos-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-tabs {
    align-self: stretch;
    border-radius: 16px;
  }

  .tab-button {
    flex: 1;
    justify-content: center;
  }
}
</style>

