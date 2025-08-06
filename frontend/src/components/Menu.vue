<template>
  <div>
    <div v-if="nombreUsuario">
      👋 Hola, {{ nombreUsuario }} | <a href="#" @click="logout">Cerrar sesión</a>
    </div>
    <div v-else>
        <p>👤 No has iniciado sesión</p>
        <router-link to="/login">🔑 Iniciar sesión</router-link> | 
        <router-link to="/registro">📝 Registrarse</router-link>
    </div>


    <div v-if="estadoNegocio === 'cerrado'" class="cerrado-banner">
      🚫 En este momento estamos cerrados. No se pueden hacer pedidos.
    </div>

    <div class="horarios">
      <h3>📅 Horarios de atención</h3>
      <ul>
        <li v-for="h in horarios" :key="h.dia">
          <strong>{{ h.dia }}:</strong>
          <span v-if="h.activo">{{ h.apertura }} - {{ h.cierre }}</span>
          <span v-else class="cerrado">Cerrado</span>
        </li>
      </ul>
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import PlatilloCard from './PlatilloCard.vue'
import { carrito } from '../store'


const nombreCliente = ref("")
const direccionEntrega = ref("")
const mostrarResumen = ref(false)


const menu = ref([])
const extras = ref([])
const horarios = ref([])
const estadoNegocio = ref("abierto")
const nombreUsuario = ref(localStorage.getItem("nombre") || null)
const telefonoCliente = ref(localStorage.getItem("telefono") || "")




const totalGeneral = computed(() =>
  carrito.value.reduce((acc, item) => acc + item.total, 0)
)

const enviarPedido = async () => {
  if (estadoNegocio.value !== "abierto") {
    alert("🚫 El negocio está cerrado. No se pueden enviar pedidos.");
    return;
  }

  if (!nombreCliente.value || !telefonoCliente.value || !direccionEntrega.value) {
    alert("Por favor llena todos los campos del cliente.");
    return;
  }

  const user_id = localStorage.getItem("user_id")

  try {
    const res = await fetch("http://localhost:5000/api/pedido", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pedido: carrito.value,
        total: totalGeneral.value,
        nombre: nombreCliente.value,
        telefono: telefonoCliente.value,
        direccion_entrega: direccionEntrega.value,
        user_id: user_id || null
      })
    })

    if (!res.ok) throw new Error("Error al enviar pedido")

    const data = await res.json()
    alert("✅ Pedido enviado: " + data.mensaje)

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

const logout = () => {
  localStorage.removeItem("user_id")
  localStorage.removeItem("nombre")
  nombreUsuario.value = null
  alert("Sesión cerrada")
}

onMounted(async () => {
  try {
    const estadoRes = await fetch("http://localhost:5000/api/estado")
    const estadoData = await estadoRes.json()
    estadoNegocio.value = estadoData.estado
  } catch (err) {
    console.error("Error al obtener estado del local:", err)
  }

  try {
    const horarioRes = await fetch("http://localhost:5000/api/horarios")
    const horariosData = await horarioRes.json()
    horarios.value = horariosData
  } catch (err) {
    console.error("Error al obtener horarios:", err)
  }

  const res = await fetch('/menu.json')
  const data = await res.json()
  menu.value = data.menu
  extras.value = data.extras_disponibles

  // 🧠 Autocompletar nombre si está logueado
  if (nombreUsuario.value) {
    nombreCliente.value = nombreUsuario.value
  }
  if (localStorage.getItem("telefono")) {
    telefonoCliente.value = localStorage.getItem("telefono")
  }
})

</script>

<style>
.container {
  max-width: 800px;
  margin: auto;
  padding: 1rem;
}
.cerrado-banner {
  background: #f44336;
  color: white;
  padding: 1rem;
  text-align: center;
}
</style>
