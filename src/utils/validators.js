export function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

export function validarSenhaForte(senha) {
  return senha.length >= 8 &&
         /[A-Z]/.test(senha) &&
         /[a-z]/.test(senha) &&
         /[0-9]/.test(senha)
}

export function validarSenha(senha) {
  return senha && senha.length >= 6
}

export function validarPreco(preco) {
  const num = parseFloat(preco)
  return !isNaN(num) && num > 0
}

export function validarEstoque(estoque) {
  const num = parseInt(estoque)
  return !isNaN(num) && num >= 0
}

export function validarNome(nome) {
  return nome && nome.trim().length >= 2
}

export function validarObrigatorio(valor) {
  return valor !== null && valor !== undefined && valor !== ''
}

