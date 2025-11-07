<template>
  <div class="grafico-card">
    <div class="grafico-header">
      <h3>Crescimento do Catálogo</h3>
      <div class="metricas">
        <span class="metrica">
          <strong>{{ totalProdutos }}</strong> produtos
        </span>
        <span v-if="ultimoMes" class="metrica">
          Último mês: {{ ultimoMes }}
        </span>
      </div>
    </div>

    <div v-if="dadosProcessados.length" class="grafico-conteudo">
      <div class="grafico-colunas">
        <div
          v-for="item in dadosProcessados"
          :key="item.mes"
          class="coluna-item"
        >
          <div class="coluna-wrapper">
            <div class="coluna" :style="{ height: `${item.percentual}%` }">
              <span class="coluna-valor">{{ item.quantidade }}</span>
            </div>
          </div>
          <span class="coluna-label">{{ item.mesFormatado }}</span>
        </div>
      </div>

      <ul class="grafico-legenda">
        <li>
          <span class="legenda-cor barra"></span>
          Novos produtos
        </li>
        <li>
          <span class="legenda-cor linha"></span>
          Total acumulado: <strong>{{ totalProdutos }}</strong>
        </li>
      </ul>
    </div>

    <div v-else class="grafico-empty">
      <p>Os produtos cadastrados aparecerão aqui por mês.</p>
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

const normalizarMes = (mesISO) => {
  if (!mesISO) return '—'
  const [ano, mes] = mesISO.split('-')
  return `${mes}/${ano}`
}

const maxQuantidade = computed(() =>
  Math.max(...props.dados.map(item => item.quantidade || 0), 1)
)

const dadosProcessados = computed(() =>
  props.dados.map(item => ({
    ...item,
    percentual: ((item.quantidade || 0) / maxQuantidade.value) * 100,
    mesFormatado: normalizarMes(item.mes)
  }))
)

const totalProdutos = computed(() => {
  if (!props.dados.length) return 0
  return props.dados.at(-1).acumulado || 0
})

const ultimoMes = computed(() => {
  if (!props.dados.length) return ''
  return normalizarMes(props.dados.at(-1).mes)
})
</script>

<style scoped>
.grafico-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  height: 100%;
}

.grafico-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
  gap: 1rem;
}

.grafico-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.metricas {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-align: right;
}

.metrica strong {
  color: var(--text-primary);
}

.grafico-conteudo {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.grafico-colunas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
  gap: 1rem;
  align-items: end;
  min-height: 220px;
}

.coluna-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.coluna-wrapper {
  width: 100%;
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 0.5rem;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  height: 100%;
}

.coluna {
  width: 100%;
  max-width: 32px;
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 10px 10px 0 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  transition: height 0.3s ease;
  position: relative;
  min-height: 4px;
}

.coluna-valor {
  font-size: 0.75rem;
  color: white;
  padding: 0.25rem 0.4rem;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(4px);
}

.coluna-label {
  font-size: 0.8rem;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.grafico-legenda {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  padding: 0;
  margin: 0;
  list-style: none;
  flex-wrap: wrap;
}

.grafico-legenda li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legenda-cor {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.legenda-cor.barra {
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
}

.legenda-cor.linha {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.grafico-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .grafico-colunas {
    grid-template-columns: repeat(auto-fit, minmax(48px, 1fr));
  }
}
</style>


