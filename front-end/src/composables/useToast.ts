import { ref } from 'vue'
import type { Component } from 'vue'
import ToastNotification from '@/components/ToastNotification.vue'

interface Toast {
  id: string
  component: Component
  props: Record<string, any>
}

interface ToastOptions {
  type?: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
  autoClose?: boolean
}

const toasts = ref<Toast[]>([])

let nextId = 1

export const useToast = () => {
  const addToast = (options: ToastOptions) => {
    const id = `toast-${nextId++}`
    
    const toast: Toast = {
      id,
      component: ToastNotification,
      props: {
        ...options,
        onClose: () => removeToast(id)
      }
    }
    
    toasts.value.push(toast)
    return id
  }

  const removeToast = (id: string) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const success = (title: string, message?: string) => {
    return addToast({ type: 'success', title, message })
  }

  const error = (title: string, message?: string) => {
    return addToast({ type: 'error', title, message })
  }

  const warning = (title: string, message?: string) => {
    return addToast({ type: 'warning', title, message })
  }

  const info = (title: string, message?: string) => {
    return addToast({ type: 'info', title, message })
  }

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info
  }
}
