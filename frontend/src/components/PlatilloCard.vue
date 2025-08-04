<script setup>
import { ref, computed } from 'vue'
import { agregarAlCarrito } from '../store'

const props = defineProps({
  platillo: Object
})

const ingredientesQuitados = ref([])
const toppingsSeleccionados = ref([])

const calcularTotal = computed(() => {
  let total = props.platillo.precio_base
  for (const top of props.platillo.toppings_opcionales) {
    if (toppingsSeleccionados.value.includes(top.nombre)) {
      total += top.precio
    }
  }
  return total
})

const agregar = () => {
  const item = {
    nombre: props.platillo.nombre,
    total: calcularTotal.value,
    toppings: [...toppingsSeleccionados.value],
    sin_ingredientes: [...ingredientesQuitados.value]
  }
  agregarAlCarrito(item)
  // opcional: limpiar selección después
  ingredientesQuitados.value = []
  toppingsSeleccionados.value = []
  alert('Agregado al carrito')
}
</script>

<template>
  <div class="card">
    <h2>{{ platillo.nombre }}</h2>
    <p><strong>Precio base:</strong> ${{ platillo.precio_base }}</p>

    <div v-if="platillo.ingredientes_base.length">
      <h4>Ingredientes base:</h4>
      <ul>
        <li v-for="ing in platillo.ingredientes_base" :key="ing.nombre">
          <label>
            <input
              type="checkbox"
              v-if="ing.removible"
              :value="ing.nombre"
              v-model="ingredientesQuitados"
            />
            {{ ing.nombre }}
            <span v-if="ing.removible">(puede quitarse)</span>
          </label>
        </li>
      </ul>
    </div>

    <div v-if="platillo.toppings_opcionales.length">
      <h4>Toppings opcionales:</h4>
      <ul>
        <li v-for="top in platillo.toppings_opcionales" :key="top.nombre">
          <label>
            <input
              type="checkbox"
              :value="top.nombre"
              v-model="toppingsSeleccionados"
            />
            {{ top.nombre }} (+${{ top.precio }})
          </label>
        </li>
      </ul>
    </div>

    <p><strong>Total:</strong> ${{ calcularTotal }}</p>
    <button @click="agregar">Agregar al carrito</button>
  </div>
</template>
