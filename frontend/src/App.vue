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
  <div
    v-if="route.path === '/menu'"
    class="mobile-bar">
    <button class="btn btn-ghost" @click="go('/')">🏠 Inicio</button>
    <button id="btn-cart" class="btn btn-primary" @click="showCart = true">
      🛒 Ver carrito
    </button>  
  </div>

  <!-- Drawer del carrito -->
  <div :class="['backdrop', { 'is-open': showCart }]" @click="showCart=false"></div>
  <aside :class="['drawer', { 'is-open': showCart }]">
    <h2 style="margin-bottom:.6rem;">Tu carrito</h2>

    <div v-if="(carrito || []).length === 0" style="opacity:.8;">
      Aún no agregas nada. Ve al
      <a href="#" @click.prevent="go('/menu'); showCart=false">menú</a>.
    </div>

    <div v-else>
      <ul style="display:grid; gap:.6rem; margin-bottom:.8rem;">
        <li
          v-for="(item, i) in carrito"
          :key="i"
          style="display:flex; justify-content:space-between; gap:.8rem; border-bottom:1px solid #222; padding-bottom:.5rem;"
        >
          <div>
            <strong>{{ item.nombre }}</strong>
            — ${{ item.total?.toFixed?.(2) || Number(item.total || 0).toFixed(2) }}
            <ul style="opacity:.8; font-size:.9rem;">
              <li v-if="item.toppings?.length">Toppings:{{ item.toppings.map(t => `${t.nombre} (+$${(Number(t.precio)||0).toFixed(2)})`).join(', ') }}</li>

              <li v-if="item.sin_ingredientes?.length">Sin: {{ item.sin_ingredientes.join(', ') }}</li>
            </ul>
          </div>
          <button class="btn btn-ghost" @click="quitar(i)">Quitar</button>
        </li>
      </ul>

      <p style="margin:.6rem 0;"><strong>Total:</strong> ${{ total }}</p>

      <div class="drawer-actions">
        <button class="btn btn-primary btn-block" @click="go('/checkout'); showCart=false">
          Ir a Checkout
        </button>
        <div class="drawer-actions-row">
          <button class="btn btn-ghost" @click="vaciar">Vaciar</button>
          <button class="btn btn-ghost" @click="showCart=false">Cerrar</button>
        </div>
      </div>
    </div>
  </aside>
  <div id="toast"></div>
</template>

<style>
.toast{
  position: fixed; left: 50%; transform: translateX(-50%);
  bottom: 80px; background: rgba(0,0,0,.85); color:#fff;
  padding:.6rem .9rem; border-radius:12px; opacity:0; pointer-events:none;
  transition: opacity .25s ease, transform .25s ease;
}
.toast.show{ opacity:1; transform: translateX(-50%) translateY(-6px); }
</style>