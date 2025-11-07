import api from './api'

const construirQueryString = (filtros = {}) => {
  const params = new URLSearchParams()

  if (filtros.busca) params.append('busca', filtros.busca)
  if (filtros.categoria) params.append('categoria', filtros.categoria)
  if (filtros.preco_min || filtros.preco_min === 0) params.append('preco_min', filtros.preco_min)
  if (filtros.preco_max || filtros.preco_max === 0) params.append('preco_max', filtros.preco_max)
  if (filtros.ativo !== undefined && filtros.ativo !== '') params.append('ativo', filtros.ativo)
  if (filtros.ordenar) params.append('ordenar', filtros.ordenar)
  if (filtros.ordem) params.append('ordem', filtros.ordem)

  return params.toString()
}

const ProdutoService = {
  async listar(filtros = {}) {
    const queryString = construirQueryString(filtros)
    const url = queryString ? `/api/produtos?${queryString}` : '/api/produtos'
    const response = await api.get(url)
    return response.data
  },

  async buscarPorId(id) {
    const response = await api.get(`/api/produtos/${id}`)
    return response.data
  },

  async criar(produto) {
    const response = await api.post('/api/produtos', produto)
    return response.data
  },

  async atualizar(id, produto) {
    const response = await api.put(`/api/produtos/${id}`, produto)
    return response.data
  },

  async deletar(id) {
    const response = await api.delete(`/api/produtos/${id}`)
    return response.data
  },

  async listarCategorias() {
    const response = await api.get('/api/produtos/categorias')
    return response.data
  },

  async exportarCSV(filtros = {}) {
    const queryString = construirQueryString(filtros)
    const url = queryString ? `/api/produtos/export/csv?${queryString}` : '/api/produtos/export/csv'
    const response = await api.get(url, {
      responseType: 'blob'
    })
    return response.data
  },

  async exportarPDF(filtros = {}) {
    const queryString = construirQueryString(filtros)
    const url = queryString ? `/api/produtos/export/pdf?${queryString}` : '/api/produtos/export/pdf'
    const response = await api.get(url, {
      responseType: 'blob'
    })
    return response.data
  }
}

export default ProdutoService

