import { defineStore } from 'pinia'
import DashboardService from '@/services/DashboardService'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    estatisticas: {
      total_produtos: 0,
      valor_total_estoque: 0,
      produtos_baixo_estoque: 0,
      produtos_ativos: 0
    },
    produtosPorCategoria: [],
    atividades: [],
    produtosDestaque: {
      mais_caros: [],
      baixo_estoque: []
    },
    vendasMensais: [],
    crescimentoProdutos: [],
    isLoading: false,
    error: null
  }),

  actions: {
    async carregarEstatisticas() {
      this.isLoading = true
      this.error = null
      try {
        const stats = await DashboardService.obterEstatisticas()
        this.estatisticas = stats
        return stats
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao carregar estatísticas'
        return null
      } finally {
        this.isLoading = false
      }
    },

    async carregarProdutosPorCategoria() {
      try {
        const dados = await DashboardService.produtosPorCategoria()
        this.produtosPorCategoria = dados
        return dados
      } catch (error) {
        return []
      }
    },

    async carregarAtividades() {
      try {
        const atividades = await DashboardService.atividadesRecentes()
        this.atividades = atividades
        return atividades
      } catch (error) {
        return []
      }
    },

    async carregarProdutosDestaque() {
      try {
        const produtos = await DashboardService.produtosDestaque()
        this.produtosDestaque = produtos
        return produtos
      } catch (error) {
        return { mais_caros: [], baixo_estoque: [] }
      }
    },

    async carregarVendasMensais() {
      try {
        const vendas = await DashboardService.vendasMensais()
        this.vendasMensais = vendas
        return vendas
      } catch (error) {
        this.vendasMensais = []
        return []
      }
    },

    async carregarCrescimentoProdutos() {
      try {
        const crescimento = await DashboardService.crescimentoProdutos()
        this.crescimentoProdutos = crescimento
        return crescimento
      } catch (error) {
        this.crescimentoProdutos = []
        return []
      }
    },

    async carregarTodos() {
      await Promise.all([
        this.carregarEstatisticas(),
        this.carregarProdutosPorCategoria(),
        this.carregarAtividades(),
        this.carregarProdutosDestaque(),
        this.carregarVendasMensais(),
        this.carregarCrescimentoProdutos()
      ])
    }
  }
})

