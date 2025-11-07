import { defineStore } from 'pinia'
import ProdutoService from '@/services/ProdutoService'

export const useProdutosStore = defineStore('produtos', {
  state: () => ({
    produtos: [],
    produtoAtual: null,
    categorias: [],
    filtros: {
      busca: '',
      categoria: '',
      preco_min: null,
      preco_max: null,
      ativo: '',
      ordenar: 'data_criacao',
      ordem: 'desc'
    },
    isLoading: false,
    error: null
  }),

  getters: {
    produtosFiltrados: (state) => {
      return state.produtos
    },
    totalProdutos: (state) => state.produtos.length
  },

  actions: {
    async listarProdutos() {
      this.isLoading = true
      this.error = null
      try {
        const produtos = await ProdutoService.listar(this.filtros)
        this.produtos = produtos
        return produtos
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao listar produtos'
        return []
      } finally {
        this.isLoading = false
      }
    },

    async buscarProduto(id) {
      this.isLoading = true
      this.error = null
      try {
        const produto = await ProdutoService.buscarPorId(id)
        this.produtoAtual = produto
        return produto
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao buscar produto'
        return null
      } finally {
        this.isLoading = false
      }
    },

    async criarProduto(produto) {
      this.isLoading = true
      this.error = null
      try {
        const novoProduto = await ProdutoService.criar(produto)
        this.produtos.push(novoProduto)
        return { success: true, produto: novoProduto }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao criar produto'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async atualizarProduto(id, produto) {
      this.isLoading = true
      this.error = null
      try {
        const produtoAtualizado = await ProdutoService.atualizar(id, produto)
        const index = this.produtos.findIndex(p => p.id === id)
        if (index !== -1) {
          this.produtos[index] = produtoAtualizado
        }
        if (this.produtoAtual?.id === id) {
          this.produtoAtual = produtoAtualizado
        }
        return { success: true, produto: produtoAtualizado }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao atualizar produto'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async deletarProduto(id) {
      this.isLoading = true
      this.error = null
      try {
        await ProdutoService.deletar(id)
        this.produtos = this.produtos.filter(p => p.id !== id)
        if (this.produtoAtual?.id === id) {
          this.produtoAtual = null
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao deletar produto'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async listarCategorias() {
      try {
        const categorias = await ProdutoService.listarCategorias()
        this.categorias = categorias
        return categorias
      } catch (error) {
        return []
      }
    },

    async exportarCSV() {
      this.error = null
      try {
        return await ProdutoService.exportarCSV(this.filtros)
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao exportar CSV'
        return null
      }
    },

    async exportarPDF() {
      this.error = null
      try {
        return await ProdutoService.exportarPDF(this.filtros)
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao exportar PDF'
        return null
      }
    },

    atualizarFiltros(novosFiltros) {
      this.filtros = { ...this.filtros, ...novosFiltros }
    },

    limparFiltros() {
      this.filtros = {
        busca: '',
        categoria: '',
        preco_min: null,
        preco_max: null,
        ativo: '',
        ordenar: 'data_criacao',
        ordem: 'desc'
      }
    },

    resetarProdutoAtual() {
      this.produtoAtual = null
    }
  }
})

