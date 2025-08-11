// src/store.js
import { ref } from 'vue'

export const carrito = ref([])

export const agregarAlCarrito = (item) => {
  carrito.value.push(item)
}

export const quitarDelCarrito = (index) => {
  carrito.value.splice(index, 1)
}

export const vaciarCarrito = () => {
  carrito.value = []
}
