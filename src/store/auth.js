import { defineStore } from 'pinia'
import AuthService from '@/services/AuthService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    usuario: AuthService.getUsuario(),
    token: AuthService.getToken(),
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    nomeUsuario: (state) => state.usuario?.nome || '',
    emailUsuario: (state) => state.usuario?.email || ''
  },

  actions: {
    async login(email, senha) {
      this.isLoading = true
      this.error = null
      try {
        const data = await AuthService.login(email, senha)
        this.token = data.token
        this.usuario = data.usuario
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao fazer login'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async register(dados) {
      this.isLoading = true
      this.error = null
      try {
        const data = await AuthService.register(dados)
        this.token = data.token
        this.usuario = data.usuario
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao registrar'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async atualizarPerfil(dados) {
      this.isLoading = true
      this.error = null
      try {
        const data = await AuthService.atualizarPerfil(dados)
        this.usuario = data.usuario
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao atualizar perfil'
        return { success: false, error: this.error }
      } finally {
        this.isLoading = false
      }
    },

    async obterPerfil() {
      this.isLoading = true
      try {
        const usuario = await AuthService.obterPerfil()
        this.usuario = usuario
        return usuario
      } catch (error) {
        this.error = error.response?.data?.mensagem || 'Erro ao obter perfil'
        return null
      } finally {
        this.isLoading = false
      }
    },

    logout() {
      AuthService.logout()
      this.usuario = null
      this.token = null
      this.error = null
    },

    verificarAutenticacao() {
      const token = AuthService.getToken()
      const usuario = AuthService.getUsuario()
      if (token && usuario) {
        this.token = token
        this.usuario = usuario
      } else {
        this.logout()
      }
    }
  }
})

