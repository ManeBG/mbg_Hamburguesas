// src/store.js
import { ref } from 'vue'

export const carrito = ref([])

export const agregarAlCarrito = (item) => {
  carrito.value.push(item)
}
