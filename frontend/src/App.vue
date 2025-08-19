<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { carrito } from '@/store'

const showCart = ref(false)
const router = useRouter()
const route = useRoute()
const go = (p) => router.push(p)

const total = computed(() =>
  (carrito.value || []).reduce((a, i) => a + Number(i.total || 0), 0).toFixed(2)
)
function quitar(i){ carrito.value.splice(i, 1) }
function vaciar(){ carrito.value = [] }
</script>

<template>
  <router-view />

  <!-- Barra móvil SOLO en menú -->
  <div v-if="route.path === '/menu'" class="mobile-bar d-flex justify-content-between p-2 bg-dark">
    <button class="btn btn-outline-light" @click="go('/')">🏠 Inicio</button>
    <button id="btn-cart" class="btn btn-warning fw-bold" @click="showCart = true">
      🛒 Ver carrito
    </button>
  </div>

  <!-- Backdrop -->
  <div :class="['backdrop', { 'is-open': showCart }]" @click="showCart=false"></div>

  <!-- Drawer del carrito -->
  <aside :class="['drawer', { 'is-open': showCart }]">
    <h2 class="text-danger mb-3">🛒 Tu carrito</h2>

    <!-- Carrito vacío -->
    <div v-if="(carrito || []).length === 0" class="text-muted">
      Aún no agregas nada. Ve al
      <a href="#" @click.prevent="go('/menu'); showCart=false">menú</a>.
    </div>

    <!-- Carrito con productos -->
    <div v-else>
      <ul class="list-unstyled d-grid gap-3 mb-3">
        <li
          v-for="(item, i) in carrito"
          :key="i"
          class="border-bottom pb-2 d-flex justify-content-between gap-2"
        >
          <div>
            <strong class="text-white d-block">{{ item.nombre }}</strong>
            <span class="text-warning fw-bold">
              ${{ item.total?.toFixed?.(2) || Number(item.total || 0).toFixed(2) }}
            </span>
            <ul class="small text-secondary mt-1">
              <li v-if="item.toppings?.length">
                Toppings: {{ item.toppings.map(t => `${t.nombre} (+$${(Number(t.precio)||0).toFixed(2)})`).join(', ') }}
              </li>
              <li v-if="item.sin_ingredientes?.length">
                Sin: {{ item.sin_ingredientes.join(', ') }}
              </li>
            </ul>
          </div>
          <button class="btn btn-outline-secondary btn-sm" @click="quitar(i)">Quitar</button>
        </li>
      </ul>

      <p class="fw-bold text-warning fs-5">Total: ${{ total }}</p>

      <div class="drawer-actions d-grid gap-2">
        <button class="btn btn-primary btn-lg" @click="go('/checkout'); showCart=false">
          Ir a Checkout
        </button>
        <button class="btn btn-outline-danger btn-lg" @click="vaciar">Vaciar carrito</button>
        <button class="btn btn-secondary btn-lg" @click="showCart=false">Cerrar</button>
      </div>
    </div>
  </aside>
  <div id="toast"></div>
</template>


<style>
/* === Drawer del carrito móvil === */
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity .3s ease;
  z-index: 30;
}
.backdrop.is-open {
  opacity: 1;
  pointer-events: auto;
}

.drawer {
  position: fixed;
  top: 0; right: 0; bottom: 0;
  width: 90%;
  max-width: 380px;
  background: #1a1a1a;
  color: #f7f7f7;
  transform: translateX(100%);
  transition: transform .3s ease;
  padding: 1rem;
  overflow-y: auto;
  z-index: 40;
  border-left: 1px solid #333;
}
.drawer.is-open {
  transform: translateX(0);
}
.drawer h2 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.4rem;
  text-align: center;
  margin-bottom: .8rem;
  color: #ff4444;
}
.drawer-actions {
  margin-top: 1rem;
  display: grid;
  gap: .6rem;
}
.drawer-actions-row {
  display: flex;
  justify-content: space-between;
  gap: .6rem;
}

/* Botón de checkout más visible */
.btn-block {
  display: block;
  width: 100%;
}

/* Barra móvil fija abajo */
.mobile-bar {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: #141414;
  border-top: 1px solid #333;
  display: flex;
  justify-content: space-around;
  padding: .6rem;
  z-index: 50;
}
.mobile-bar .btn {
  flex: 1;
  margin: 0 .3rem;
}

/* Ajustes generales botones en drawer */
.drawer button.btn-outline-secondary {
  font-size: .85rem;
  padding: .4rem .7rem;
}
.drawer .btn-ghost {
  border: 1px solid #555;
  color: #eee;
  background: transparent;
}
.drawer .btn-ghost:hover {
  background: #333;
}
.drawer .btn-primary {
  background: #E6382B;
  border: none;
}

/* Toast (mantiene lo que ya tenías) */
.toast{
  position: fixed; left: 50%; transform: translateX(-50%);
  bottom: 80px; background: rgba(0,0,0,.85); color:#fff;
  padding:.6rem .9rem; border-radius:12px; opacity:0; pointer-events:none;
  transition: opacity .25s ease, transform .25s ease;
}
.toast.show{ opacity:1; transform: translateX(-50%) translateY(-6px); }

/* Barra inferior fija solo en mobile */
/* .mobile-bar {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  display: flex;
  justify-content: space-around;
  padding: .6rem;
  background: #111;
  border-top: 1px solid #333;
  z-index: 1000;
} */

/* En desktop la movemos arriba tipo navbar */
/* @media (min-width: 1024px) {
  .mobile-bar {
    top: 0; bottom: auto;
    border-top: none;
    border-bottom: 1px solid #333;
    justify-content: flex-end;
    gap: .8rem;
    padding: .8rem 1.2rem;
  }
} */

</style>
