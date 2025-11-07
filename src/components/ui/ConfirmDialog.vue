<template>
  <Modal
    :aberto="aberto"
    :titulo="titulo"
    tamanho="small"
    @fechar="cancelar"
  >
    <p class="confirm-mensagem">{{ mensagem }}</p>
    <template #footer>
      <button class="btn btn-secondary" @click="cancelar">
        Cancelar
      </button>
      <button class="btn btn-primary" @click="confirmar">
        Confirmar
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import { useUIStore } from '@/store/ui'
import Modal from './Modal.vue'

const uiStore = useUIStore()

const aberto = computed(() => uiStore.confirmDialog.aberto)
const titulo = computed(() => uiStore.confirmDialog.titulo)
const mensagem = computed(() => uiStore.confirmDialog.mensagem)

const confirmar = () => {
  if (uiStore.confirmDialog.onConfirm) {
    uiStore.confirmDialog.onConfirm()
  }
  uiStore.fecharConfirmDialog()
}

const cancelar = () => {
  if (uiStore.confirmDialog.onCancel) {
    uiStore.confirmDialog.onCancel()
  }
  uiStore.fecharConfirmDialog()
}
</script>

<style scoped>
.confirm-mensagem {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}
</style>

