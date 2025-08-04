<template>
  <div class="container">
    <h1>Menú Interactivo</h1>

    <div v-if="menu.length === 0">Cargando menú...</div>

    <div v-else>
      <PlatilloCard
        v-for="platillo in menu"
        :key="platillo.id"
        :platillo="platillo"
      />

      <h2>Extras disponibles</h2>
      <ul>
        <li v-for="extra in extras" :key="extra.nombre">
          {{ extra.nombre }} - ${{ extra.precio }}
        </li>
      </ul>
    </div>
    <h2>🛒 Carrito</h2>
    <div v-if="carrito.length === 0">
      El carrito está vacío.
    </div>
    <div v-else>
      <ul>
        <li v-for="(item, index) in carrito" :key="index">
          {{ item.nombre }} - ${{ item.total }}
          <ul>
            <li v-if="item.toppings.length">Toppings: {{ item.toppings.join(', ') }}</li>
            <li v-if="item.sin_ingredientes.length">Sin: {{ item.sin_ingredientes.join(', ') }}</li>
          </ul>
        </li>
      </ul>
      <p><strong>Total general:</strong> ${{ totalGeneral }}</p>
      <button @click="mostrarResumen = true">Confirmar pedido</button>

    </div>
    <div v-if="mostrarResumen">
      <h2>🧾 Resumen del Pedido</h2>
      <ul>
        <li v-for="(item, index) in carrito" :key="'r-' + index">
          {{ item.nombre }} - ${{ item.total }}
          <ul>
            <li v-if="item.toppings.length">Toppings: {{ item.toppings.join(', ') }}</li>
            <li v-if="item.sin_ingredientes.length">Sin: {{ item.sin_ingredientes.join(', ') }}</li>
          </ul>
        </li>
      </ul>
      <p><strong>Total:</strong> ${{ totalGeneral }}</p>

      <button @click="enviarPedido">Enviar pedido</button>
    </div>


  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PlatilloCard from './components/PlatilloCard.vue'
import { carrito } from './store'
import { computed } from 'vue'




const menu = ref([])
const extras = ref([])
const totalGeneral = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.total, 0)
)
const mostrarResumen = ref(false)
const enviarPedido = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/pedido', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pedido: carrito.value,
        total: totalGeneral.value
      })
    })

    if (!res.ok) throw new Error('Error al enviar pedido')

    const data = await res.json()
    alert('Pedido enviado: ' + data.mensaje)

    carrito.value = []
    mostrarResumen.value = false
  } catch (err) {
    alert('Hubo un error al enviar el pedido.')
    console.error(err)
  }
}



onMounted(async () => {
  const res = await fetch('/menu.json')
  const data = await res.json()
  menu.value = data.menu
  extras.value = data.extras_disponibles
})
</script>

<style>
.container {
  max-width: 800px;
  margin: auto;
  padding: 1rem;
}
</style>
