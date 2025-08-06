<template>
  <div v-if="estadoNegocio === 'cerrado'" class="cerrado-banner">
    🚫 En este momento estamos cerrados. No se pueden hacer pedidos.
  </div>

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

    <!-- Carrito -->
    <h2>🛒 Carrito</h2>

    <div v-if="estadoNegocio === 'cerrado'">
      <p>Estamos cerrados. El carrito está deshabilitado.</p>
    </div>

    <div v-else>
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
        <button 
          @click="estadoNegocio === 'abierto' ? mostrarResumen = true : alert('🚫 El negocio está cerrado.')"
        >
          Confirmar pedido
        </button>
      </div>
    </div>

    <!-- Resumen -->
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

      <h3>📝 Datos del Cliente</h3>
      <div class="form">
        <label>Nombre:
          <input v-model="nombreCliente" type="text" required />
        </label>
        <label>Teléfono:
          <input v-model="telefonoCliente" type="text" required />
        </label>
        <label>Dirección:
          <textarea v-model="direccionEntrega" required></textarea>
        </label>
      </div>

      <button @click="enviarPedido">Enviar pedido</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import PlatilloCard from './components/PlatilloCard.vue'
import { carrito } from './store'

const menu = ref([])
const extras = ref([])
const mostrarResumen = ref(false)
const nombreCliente = ref("")
const telefonoCliente = ref("")
const direccionEntrega = ref("")
const estadoNegocio = ref("abierto")

const totalGeneral = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.total, 0)
)

const enviarPedido = async () => {
  // 🚫 Bloquear por estado cerrado
  if (estadoNegocio.value !== "abierto") {
    alert("🚫 El negocio está cerrado. No se pueden enviar pedidos.");
    return;
  }

  if (!nombreCliente.value || !telefonoCliente.value || !direccionEntrega.value) {
    alert("Por favor llena todos los campos del cliente.");
    return;
  }

  try {
    const res = await fetch("http://localhost:5000/api/pedido", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pedido: carrito.value,
        total: totalGeneral.value,
        nombre: nombreCliente.value,
        telefono: telefonoCliente.value,
        direccion_entrega: direccionEntrega.value
      })
    })

    if (!res.ok) throw new Error("Error al enviar pedido")

    const data = await res.json()
    alert("✅ Pedido enviado: " + data.mensaje)

    // limpiar
    carrito.value = []
    mostrarResumen.value = false
    nombreCliente.value = ""
    telefonoCliente.value = ""
    direccionEntrega.value = ""
  } catch (err) {
    alert("Hubo un error al enviar el pedido.")
    console.error(err)
  }
}

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:5000/api/estado")
    const data = await res.json()
    estadoNegocio.value = data.estado
  } catch (err) {
    console.error("Error al obtener estado del local:", err)
  }

  const resMenu = await fetch('/menu.json')
  const data = await resMenu.json()
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
.cerrado-banner {
  background: #ffdddd;
  color: #a00;
  text-align: center;
  font-weight: bold;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 2px solid #a00;
  border-radius: 5px;
}
</style>
