<template>
  <div class="produto-detalhes">
    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner size="large" />
    </div>

    <div v-else-if="produto" class="produto-content">
      <div class="produto-imagem-grande">
        <img :src="imagemUrl" :alt="produto.nome" />
        <div class="produto-badges">
          <span v-if="produto.estoque < 10" class="badge badge-warning">
            <i class="bi bi-exclamation-triangle"></i>
            Estoque Baixo
          </span>
          <span v-if="!produto.ativo" class="badge badge-danger">
            <i class="bi bi-x-circle"></i>
            Inativo
          </span>
          <span v-else class="badge badge-success">
            <i class="bi bi-check-circle"></i>
            Ativo
          </span>
        </div>
      </div>

      <div class="produto-info">
        <div class="produto-header">
          <div>
            <h1 class="produto-nome">{{ produto.nome }}</h1>
            <div class="produto-meta">
              <span class="produto-categoria">
                <i class="bi bi-tag"></i>
                {{ produto.categoria || 'Sem categoria' }}
              </span>
              <span class="produto-data">
                <i class="bi bi-calendar"></i>
                Criado em {{ formatDate(produto.data_criacao) }}
              </span>
            </div>
          </div>
          <div class="produto-actions-header">
            <router-link :to="`/produtos/${produto.id}/editar`" class="btn btn-primary">
              <i class="bi bi-pencil"></i>
              Editar
            </router-link>
            <button class="btn btn-danger" @click="$emit('deletar', produto.id)">
              <i class="bi bi-trash"></i>
              Excluir
            </button>
          </div>
        </div>

        <div class="produto-descricao">
          <h3>Descrição</h3>
          <p>{{ produto.descricao || 'Nenhuma descrição disponível.' }}</p>
        </div>

        <div class="produto-stats">
          <div class="stat-item">
            <div class="stat-label">Preço</div>
            <div class="stat-value price">{{ formatCurrency(produto.preco) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Estoque</div>
            <div class="stat-value" :class="{ 'low-stock': produto.estoque < 10 }">
              {{ produto.estoque }} unidades
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Valor Total</div>
            <div class="stat-value">{{ formatCurrency(produto.preco * produto.estoque) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Status</div>
            <div class="stat-value">
              <span :class="produto.ativo ? 'status-active' : 'status-inactive'">
                {{ produto.ativo ? 'Ativo' : 'Inativo' }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="produto.data_atualizacao" class="produto-updated">
          <i class="bi bi-clock-history"></i>
          Última atualização: {{ formatDate(produto.data_atualizacao) }}
        </div>
      </div>
    </div>

    <div v-else class="error-state">
      <i class="bi bi-exclamation-circle"></i>
      <h3>Produto não encontrado</h3>
      <p>O produto que você está procurando não existe ou foi removido.</p>
      <router-link to="/produtos" class="btn btn-primary">
        Voltar para Produtos
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatCurrency, formatDate } from '@/utils/formatters'
import { getImageUrl } from '@/utils/helpers'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const props = defineProps({
  produto: {
    type: Object,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['deletar'])

const imagemUrl = computed(() => {
  if (!props.produto) return 'https://via.placeholder.com/600x600?text=Sem+Imagem'
  return getImageUrl(props.produto.imagem_url)
})
</script>

<style scoped>
.produto-detalhes {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.produto-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.produto-imagem-grande {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 16px;
  overflow: hidden;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
}

.produto-imagem-grande img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.produto-badges {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: var(--shadow-md);
}

.badge-warning {
  background: var(--color-warning);
  color: white;
}

.badge-danger {
  background: var(--color-danger);
  color: white;
}

.badge-success {
  background: var(--color-success);
  color: white;
}

.produto-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.produto-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.produto-nome {
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.produto-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.produto-categoria,
.produto-data {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.produto-actions-header {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.produto-descricao h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.produto-descricao p {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 1rem;
}

.produto-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-value.price {
  color: var(--color-primary);
  font-size: 2rem;
}

.stat-value.low-stock {
  color: var(--color-warning);
}

.status-active {
  color: var(--color-success);
  font-weight: 600;
}

.status-inactive {
  color: var(--color-danger);
  font-weight: 600;
}

.produto-updated {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.error-state i {
  font-size: 4rem;
  color: var(--text-tertiary);
  margin-bottom: 1rem;
  display: block;
}

.error-state h3 {
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-size: 1.5rem;
}

.error-state p {
  margin: 0 0 1.5rem 0;
  color: var(--text-secondary);
}

@media (max-width: 968px) {
  .produto-content {
    grid-template-columns: 1fr;
  }

  .produto-header {
    flex-direction: column;
  }

  .produto-actions-header {
    width: 100%;
  }

  .produto-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .produto-detalhes {
    padding: 1rem;
  }

  .produto-nome {
    font-size: 2rem;
  }

  .produto-actions-header {
    flex-direction: column;
  }

  .produto-actions-header .btn {
    width: 100%;
  }
}
</style>

