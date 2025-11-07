<template>
  <div class="grafico-card">
    <div class="grafico-header">
      <h3>Vendas Mensais (R$)</h3>
      <span class="meta-info">{{ rangeTemporal }}</span>
    </div>

    <div v-if="dadosProcessados.length" class="grafico-area">
      <svg viewBox="0 0 100 40" preserveAspectRatio="none">
        <defs>
          <linearGradient id="vendas-gradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="rgba(102, 126, 234, 0.35)" />
            <stop offset="100%" stop-color="rgba(118, 75, 162, 0.05)" />
          </linearGradient>
        </defs>
        <polygon
          :points="areaPoints"
          fill="url(#vendas-gradient)"
          stroke="none"
        />
        <polyline
          :points="linePoints"
          fill="none"
          stroke="var(--color-primary)"
          stroke-width="1.5"
        />
        <g
          v-for="(item, index) in dadosProcessados"
          :key="item.mes"
          class="grafico-ponto"
        >
          <circle
            :cx="item.x"
            :cy="item.y"
            r="1.4"
            fill="var(--color-primary)"
          />
        </g>
      </svg>

      <div class="grafico-legenda">
        <div
          v-for="item in dadosProcessados"
          :key="item.mes"
          class="legenda-item"
        >
          <span class="legenda-ponto"></span>
          <span class="legenda-label">{{ item.mesFormatado }}</span>
          <span class="legenda-valor">{{ formatCurrency(item.total) }}</span>
        </div>
      </div>
    </div>

    <div v-else class="grafico-empty">
      <p>Cadastre produtos para ver o desempenho mensal.</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatCurrency } from '@/utils/formatters'

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

const dadosProcessados = computed(() => {
  if (!props.dados.length) return []

  const max = Math.max(...props.dados.map(item => item.total || 0), 1)
  const espaçamento = props.dados.length > 1 ? 100 / (props.dados.length - 1) : 0

  return props.dados.map((item, index) => {
    const percentual = max ? (item.total || 0) / max : 0
    return {
      ...item,
      x: props.dados.length > 1 ? index * espaçamento : 50,
      y: 40 - (percentual * 30) - 5, // padding superior/inferior
      mesFormatado: normalizarMes(item.mes)
    }
  })
})

const linePoints = computed(() =>
  dadosProcessados.value.map(item => `${item.x},${item.y}`).join(' ')
)

const areaPoints = computed(() => {
  if (!dadosProcessados.value.length) return ''
  const inicio = `0,40 `
  const pontos = dadosProcessados.value.map(item => `${item.x},${item.y}`).join(' ')
  const fim = ` 100,40`
  return inicio + pontos + fim
})

const rangeTemporal = computed(() => {
  if (props.dados.length < 2) return ''
  const primeiro = normalizarMes(props.dados[0].mes)
  const ultimo = normalizarMes(props.dados.at(-1).mes)
  return `${primeiro} → ${ultimo}`
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

.meta-info {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

.grafico-area {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

svg {
  width: 100%;
  height: 220px;
}

.grafico-legenda {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem 1.5rem;
}

.legenda-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.legenda-ponto {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-primary);
  display: inline-block;
}

.legenda-label {
  font-weight: 500;
  color: var(--text-primary);
}

.legenda-valor {
  margin-left: auto;
  color: var(--text-secondary);
}

.grafico-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}
</style>


