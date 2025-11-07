import api from './api'

const AuthService = {
  async login(email, senha) {
    const response = await api.post('/api/auth/login', { email, senha })
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('usuario', JSON.stringify(response.data.usuario))
    }
    return response.data
  },

  async register(dados) {
    const response = await api.post('/api/auth/register', dados)
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('usuario', JSON.stringify(response.data.usuario))
    }
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('usuario')
  },

  async obterPerfil() {
    const response = await api.get('/api/auth/perfil')
    return response.data
  },

  async atualizarPerfil(dados) {
    const response = await api.put('/api/auth/perfil', dados)
    if (response.data.usuario) {
      localStorage.setItem('usuario', JSON.stringify(response.data.usuario))
    }
    return response.data
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  getToken() {
    return localStorage.getItem('token')
  },

  getUsuario() {
    const usuarioStr = localStorage.getItem('usuario')
    return usuarioStr ? JSON.parse(usuarioStr) : null
  }
}

export default AuthService

