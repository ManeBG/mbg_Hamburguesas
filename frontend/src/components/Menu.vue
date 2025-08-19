<!-- src/components/Menu.vue -->
<script setup>
import { ref, onMounted, computed } from 'vue'
import PlatilloCard from './PlatilloCard.vue'
import { carrito, quitarDelCarrito, vaciarCarrito } from '@/store'
// import { useMedia } from '@/composables/useMedia'

const menu = ref([])
const extras = ref([])
const horarios = ref([])
const estadoNegocio = ref("abierto")
const nombreUsuario = ref(localStorage.getItem("nombre") || null)

const totalGeneral = computed(() =>
  (carrito.value || []).reduce((acc, item) => acc + Number(item?.total || 0), 0).toFixed(2)
)

// Mostrar carrito de página SOLO en desktop (>=1024px)
// const isDesktop = useMedia('(min-width: 1024px)')

const logout = () => {
  localStorage.removeItem("user_id")
  localStorage.removeItem("nombre")
  localStorage.removeItem("telefono")
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
    horarios.value = Array.isArray(horariosData) ? horariosData : []
  } catch (err) {
    console.error("Error al obtener horarios:", err)
  }

  try {
    const res = await fetch('/menu.json')
    const data = await res.json()
    menu.value = data.menu || []
    extras.value = data.extras_disponibles || []
  } catch (e) {
    console.error('Error cargando menú:', e)
    menu.value = []
    extras.value = []
  }
})

function agregarAlCarrito(item){
  // item ya viene con total calculado y arrays toppings/sin
  carrito.value.push(item)
}

</script>

<template>
  <div class="container">
    <!-- Sesión -->
    <div v-if="nombreUsuario" class="session-row">
      👋 Hola, {{ nombreUsuario }} |
      <a href="#" @click.prevent="logout">Cerrar sesión</a>
    </div>
    <div v-else class="session-row">
      <span>👤 No has iniciado sesión</span>
      <div class="actions-center">
        <router-link class="btn btn-ghost" to="/login">🔑 Iniciar sesión</router-link>
        <router-link class="btn btn-ghost" to="/registro">📝 Registrarse</router-link>
      </div>
    </div>

    <!-- Banner cerrado -->
    <div v-if="estadoNegocio === 'cerrado'" class="cerrado-banner">
      🚫 En este momento estamos cerrados. No se pueden hacer pedidos.
    </div>

    <!-- Horarios -->
    <section class="horarios">
      <h3>📅 Horarios de atención</h3>
      <ul>
        <li v-for="h in horarios" :key="h.dia">
          <strong>{{ h.dia }}:</strong>
          <span v-if="h.activo">{{ h.apertura }} - {{ h.cierre }}</span>
          <span v-else class="cerrado">Cerrado</span>
        </li>
      </ul>
    </section>

    <!-- Menú -->
    <!-- Menú -->
    <h1 class="mb-4 text-center text-danger fw-bold">🍔 Nuestro Menú</h1>

    <div v-if="(menu || []).length === 0" class="text-center text-muted">
      Cargando menú...
    </div>

    <div v-else class="row g-4">
      <div
        class="col-12 col-sm-6 col-md-4"
        v-for="platillo in menu"
        :key="platillo.id"
      >
        <PlatilloCard
          :platillo="platillo"
          @add="agregarAlCarrito"
        />
      </div>
    </div>



    <!-- Extras -->
    <h2 class="mt-1">Extras disponibles</h2>
    <ul class="extras-list">
      <li v-for="extra in extras" :key="extra.nombre">
        {{ extra.nombre }} - ${{ extra.precio }}
      </li>
    </ul>

    <!-- 🛒 Carrito: SOLO se ve en desktop -->
    <!-- <section v-if="isDesktop" class="cart-desktop">
      <h2>🛒 Carrito</h2>

      <div v-if="estadoNegocio === 'cerrado'">
        <p>Estamos cerrados. El carrito está deshabilitado.</p>
      </div>

      <div v-else>
        <div v-if="(carrito || []).length === 0">El carrito está vacío.</div>

        <div v-else> -->
          <!-- dentro del carrito en Menu.vue -->
          <!-- <ul class="cart-list">
            <li v-for="(item, index) in carrito" :key="index" class="cart-row">
              <div class="cart-info">
                <div class="cart-title">
                  <strong>{{ item.nombre }}</strong>
                  <span class="cart-price">
                    ${{ (Number(item.total)||0).toFixed(2) }}
                  </span>
                </div>

                <ul class="cart-sub">
                  <li>Unidad: ${{ (Number(item.subtotal)||0).toFixed(2) }} × {{ item.cantidad || 1 }}</li>
                  <li v-if="(item.toppings||[]).length">
                    Toppings:
                    {{ item.toppings.map(t => `${t.nombre} (+$${(Number(t.precio)||0).toFixed(2)})`).join(', ') }}
                  </li>
                  <li v-if="(item.sin_ingredientes||[]).length">
                    Sin: {{ item.sin_ingredientes.join(', ') }}
                  </li>
                </ul>
              </div>

              <button class="btn btn-outline-secondary" @click="quitarDelCarrito(index)">Quitar</button>
            </li>
          </ul>


          <div class="cart-footer">
            <p class="cart-total"><strong>Total:</strong> ${{ totalGeneral }}</p> -->

            <!-- Botones centrados y separados -->
            <!-- <div class="actions-center">
              <router-link class="btn btn-primary btn-lg" to="/checkout">Ir a Checkout</router-link>
              <button class="btn btn-outline-danger btn-lg" @click="vaciarCarrito">Vaciar carrito</button>
            </div>
          </div>
        </div>
      </div>
    </section> -->

  </div>
</template>

<style>
/* Layout base */
.container {
  width: min(100% - 24px, 1100px);
  margin: auto;
  padding: 1rem;
}

/* Mensajes */
.cerrado-banner {
  background: #f44336;
  color: white;
  padding: 1rem;
  text-align: center;
  border-radius: 12px;
  margin: .5rem 0 1rem 0;
}

/* Grid de cards del menú */
.menu-grid{
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

/* Extras */
.mt-1{ margin-top: 1rem; }
.extras-list{ margin-left: 1.2rem; }

/* Sesión */
.session-row{
  display:flex; align-items:center; gap:.6rem; flex-wrap:wrap; margin-bottom:.5rem;
}

/* Utilidades de botones centrados/separados */
.actions-center{
  display:flex; justify-content:center; gap:.75rem; flex-wrap:wrap; margin-top:.75rem;
}
.btn{
  display:inline-flex; align-items:center; justify-content:center;
  padding:.6rem .9rem; border-radius:12px; border:1px solid #333; background:#141414; color:#f7f7f7;
  cursor:pointer; min-height:44px;
}
.btn-ghost{ background:transparent; }
.btn-primary{ background:#E6382B; color:#fff; border-color:transparent; }
.btn-lg{ padding: .9rem 1.1rem; }

/* Carrito Desktop */
.cart-desktop{
  margin-top: 1rem;
  padding: 1rem 1.2rem;
  border: 1px solid #222;
  border-radius: 14px;
  background: #1a1a1a;
  color: #f5f5f5;
  font-size: 0.95rem;
  line-height: 1.4;
}
.cart-desktop h2{
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.4rem;
  color: #ff4444; /* rojo retro para destacar */
  margin-bottom: .8rem;
  display: flex;
  justify-content: center; /* centra horizontalmente */
  align-items: center;
  gap: .4rem;
}

.cart-list{
  display: grid;
  gap: .6rem;
}
.cart-row{
  display: flex;
  justify-content: space-between;
  gap: .8rem;
  padding-bottom: .6rem;
  border-bottom: 1px solid #222;
}
.cart-info{ flex: 1; }
.cart-title{
  display:flex; justify-content:space-between; gap:.5rem; align-items: baseline;
  font-weight: 600;
}
.cart-title strong{
  color: #fff; /* nombres en blanco */
  font-size: 1rem;
}
.cart-price{ 
  color: #ffcc00; /* dorado para precios */
  font-weight: 700;
  font-size: 1rem;
}

.cart-sub{ 
  font-size:.9rem; 
  color: #ccc; /* subdetalles en gris claro */
  margin:.3rem 0 0 0; 
  padding-left: 1rem; 
}
.cart-sub li{ margin-bottom: .2rem; }

.cart-footer{ margin-top: .8rem; }
.cart-total{ 
  font-size: 1.1rem; 
  font-weight: 700; 
  color: #ffcc00; /* total en dorado */
  margin-bottom: .8rem; 
}

/* Ocultar carrito de página en móvil por si acaso (refuerzo) */
@media (max-width: 1023px){
  .cart-desktop{ display:none; }
}
</style>







<!-- <template>
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
        <router-link to="/checkout">
          <button>Ir a Checkout</button>
        </router-link>
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
    const res = await fetch("http://localhost:5000/api/pedidos", {
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
</style> -->
