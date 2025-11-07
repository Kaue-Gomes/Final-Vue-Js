<template>
  <div class="filtros-produtos">
    <div class="filtros-header">
      <h3>Filtros</h3>
      <button class="btn-link" @click="limparFiltros">Limpar</button>
    </div>

    <div class="filtros-content">
      <div class="filtro-group">
        <label>Buscar</label>
        <input
          v-model="filtros.busca"
          type="text"
          class="form-control"
          placeholder="Nome ou descrição..."
          @input="aplicarFiltros"
        />
      </div>

      <div class="filtro-group">
        <label>Categoria</label>
        <select
          v-model="filtros.categoria"
          class="form-control"
          @change="aplicarFiltros"
        >
          <option value="">Todas</option>
          <option v-for="cat in categorias" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <div class="filtro-group">
        <label>Preço Mínimo</label>
        <input
          v-model.number="filtros.preco_min"
          type="number"
          step="0.01"
          min="0"
          class="form-control"
          placeholder="0.00"
          @input="aplicarFiltros"
        />
      </div>

      <div class="filtro-group">
        <label>Preço Máximo</label>
        <input
          v-model.number="filtros.preco_max"
          type="number"
          step="0.01"
          min="0"
          class="form-control"
          placeholder="9999.99"
          @input="aplicarFiltros"
        />
      </div>

      <div class="filtro-group">
        <label>Status</label>
        <select
          v-model="filtros.ativo"
          class="form-control"
          @change="aplicarFiltros"
        >
          <option value="">Todos</option>
          <option value="true">Ativos</option>
          <option value="false">Inativos</option>
        </select>
      </div>

      <div class="filtro-group">
        <label>Ordenar por</label>
        <select
          v-model="filtros.ordenar"
          class="form-control"
          @change="aplicarFiltros"
        >
          <option value="data_criacao">Data de Criação</option>
          <option value="nome">Nome</option>
          <option value="preco">Preço</option>
        </select>
      </div>

      <div class="filtro-group">
        <label>Ordem</label>
        <select
          v-model="filtros.ordem"
          class="form-control"
          @change="aplicarFiltros"
        >
          <option value="desc">Decrescente</option>
          <option value="asc">Crescente</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, computed, onMounted } from 'vue'
import { useProdutosStore } from '@/store/produtos'

const produtosStore = useProdutosStore()

const filtros = reactive({
  busca: '',
  categoria: '',
  preco_min: null,
  preco_max: null,
  ativo: '',
  ordenar: 'data_criacao',
  ordem: 'desc'
})

const categorias = computed(() => produtosStore.categorias)

const aplicarFiltros = () => {
  produtosStore.atualizarFiltros({ ...filtros })
  produtosStore.listarProdutos()
}

const limparFiltros = () => {
  Object.assign(filtros, {
    busca: '',
    categoria: '',
    preco_min: null,
    preco_max: null,
    ativo: '',
    ordenar: 'data_criacao',
    ordem: 'desc'
  })
  produtosStore.limparFiltros()
  produtosStore.listarProdutos()
}

onMounted(async () => {
  await produtosStore.listarCategorias()
})

watch(
  () => produtosStore.filtros,
  (novosFiltros) => {
    if (!novosFiltros) return
    Object.assign(filtros, {
      busca: novosFiltros.busca ?? '',
      categoria: novosFiltros.categoria ?? '',
      preco_min: novosFiltros.preco_min ?? null,
      preco_max: novosFiltros.preco_max ?? null,
      ativo: novosFiltros.ativo ?? '',
      ordenar: novosFiltros.ordenar ?? 'data_criacao',
      ordem: novosFiltros.ordem ?? 'desc'
    })
  },
  { immediate: true, deep: true }
)
</script>

<style scoped>
.filtros-produtos {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.filtros-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.filtros-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.btn-link {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  text-decoration: underline;
}

.btn-link:hover {
  color: var(--color-secondary);
}

.filtros-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filtro-group {
  display: flex;
  flex-direction: column;
}

.filtro-group label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-control {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
</style>

