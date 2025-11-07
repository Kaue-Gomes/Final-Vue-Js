<template>
  <div class="grafico-categoria">
    <div class="grafico-header">
      <h3>Produtos por Categoria</h3>
      <span class="total">Total: {{ totalProdutos }}</span>
    </div>

    <div v-if="dados.length" class="grafico-barras">
      <div
        v-for="item in dadosOrdenados"
        :key="item.categoria"
        class="barra-item"
      >
        <div class="barra-label">
          <span class="categoria-nome">{{ item.categoria }}</span>
          <span class="categoria-valor">{{ item.quantidade }}</span>
        </div>
        <div class="barra">
          <div
            class="barra-preenchimento"
            :style="{ width: calcularWidth(item.quantidade) }"
          ></div>
        </div>
      </div>
    </div>

    <div v-else class="grafico-empty">
      <p>Nenhuma categoria cadastrada ainda.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  dados: {
    type: Array,
    default: () => []
  }
})

const dadosOrdenados = computed(() =>
  [...props.dados].sort((a, b) => b.quantidade - a.quantidade)
)

const totalProdutos = computed(() =>
  props.dados.reduce((acc, item) => acc + (item.quantidade || 0), 0)
)

const maxQuantidade = computed(() =>
  Math.max(...props.dados.map(item => item.quantidade || 0), 1)
)

const calcularWidth = (valor) => {
  const percentual = (valor / maxQuantidade.value) * 100
  return `${percentual}%`
}
</script>

<style scoped>
.grafico-categoria {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}

.grafico-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.grafico-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.total {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

.grafico-barras {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.barra-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.barra-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.categoria-nome {
  font-weight: 500;
  color: var(--text-primary);
}

.barra {
  background: var(--bg-secondary);
  border-radius: 999px;
  overflow: hidden;
  height: 12px;
}

.barra-preenchimento {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 999px;
  transition: width 0.4s ease;
}

.grafico-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}
</style>


