<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <h3 class="modal-title">{{ title }}</h3>
      <div class="modal-buttons">
        <button @click="confirm" class="confirm-btn">확인</button>
        <button @click="close" class="cancel-btn">취소</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: String,
})
const emit = defineEmits(['confirm', 'close'])

const confirm = () => emit('confirm')
const close = () => emit('close')
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 360px;
  text-align: center;
  animation: slideUp 0.25s ease;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #111827;
}

.modal-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.confirm-btn,
.cancel-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.confirm-btn {
  background-color: #2563eb;
  color: white;
}

.confirm-btn:hover {
  background-color: #1e40af;
}

.cancel-btn {
  background-color: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background-color: #e5e7eb;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
