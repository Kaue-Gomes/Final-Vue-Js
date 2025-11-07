import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    tema: localStorage.getItem('tema') || 'light',
    sidebarAberto: false,
    loading: false,
    toasts: [],
    modal: {
      aberto: false,
      titulo: '',
      conteudo: null,
      tipo: 'default'
    },
    confirmDialog: {
      aberto: false,
      titulo: '',
      mensagem: '',
      onConfirm: null,
      onCancel: null
    }
  }),

  getters: {
    isDarkMode: (state) => state.tema === 'dark',
    isSidebarAberto: (state) => state.sidebarAberto
  },

  actions: {
    alternarTema() {
      this.tema = this.tema === 'light' ? 'dark' : 'light'
      localStorage.setItem('tema', this.tema)
      document.documentElement.setAttribute('data-theme', this.tema)
    },

    inicializarTema() {
      document.documentElement.setAttribute('data-theme', this.tema)
    },

    abrirSidebar() {
      this.sidebarAberto = true
    },

    fecharSidebar() {
      this.sidebarAberto = false
    },

    toggleSidebar() {
      this.sidebarAberto = !this.sidebarAberto
    },

    setLoading(loading) {
      this.loading = loading
    },

    adicionarToast(toast) {
      const id = Date.now() + Math.random()
      const novoToast = {
        id,
        tipo: toast.tipo || 'info',
        titulo: toast.titulo || '',
        mensagem: toast.mensagem || '',
        duracao: toast.duracao || 5000,
        ...toast
      }
      this.toasts.push(novoToast)
      
      if (novoToast.duracao > 0) {
        setTimeout(() => {
          this.removerToast(id)
        }, novoToast.duracao)
      }
      
      return id
    },

    removerToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    },

    abrirModal(modal) {
      this.modal = {
        aberto: true,
        titulo: modal.titulo || '',
        conteudo: modal.conteudo || null,
        tipo: modal.tipo || 'default',
        ...modal
      }
    },

    fecharModal() {
      this.modal = {
        aberto: false,
        titulo: '',
        conteudo: null,
        tipo: 'default'
      }
    },

    abrirConfirmDialog(dialog) {
      this.confirmDialog = {
        aberto: true,
        titulo: dialog.titulo || 'Confirmar',
        mensagem: dialog.mensagem || '',
        onConfirm: dialog.onConfirm || null,
        onCancel: dialog.onCancel || null
      }
    },

    fecharConfirmDialog() {
      this.confirmDialog = {
        aberto: false,
        titulo: '',
        mensagem: '',
        onConfirm: null,
        onCancel: null
      }
    }
  }
})

