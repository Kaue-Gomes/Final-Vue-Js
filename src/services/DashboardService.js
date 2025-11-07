import api from './api'

const DashboardService = {
  async obterEstatisticas() {
    const response = await api.get('/api/dashboard/stats')
    return response.data
  },

  async produtosPorCategoria() {
    const response = await api.get('/api/dashboard/categorias')
    return response.data
  },

  async atividadesRecentes() {
    const response = await api.get('/api/dashboard/atividades')
    return response.data
  },

  async produtosDestaque() {
    const response = await api.get('/api/dashboard/produtos-destaque')
    return response.data
  },

  async vendasMensais() {
    const response = await api.get('/api/dashboard/vendas-mensais')
    return response.data
  },

  async crescimentoProdutos() {
    const response = await api.get('/api/dashboard/crescimento')
    return response.data
  }
}

export default DashboardService

