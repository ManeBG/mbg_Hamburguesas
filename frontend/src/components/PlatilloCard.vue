<!-- src/components/PlatilloCard.vue -->
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  platillo: { type: Object, required: true }
})
const emit = defineEmits(['add'])

// Estado de selección
// Por default, los removibles arrancan "incluidos" (checked)
const ingredientesSeleccionados = ref(
  (props.platillo.ingredientes_base || [])
    .filter(i => i.removible !== false)
    .map(i => i.nombre)
)

const toppingsSeleccionados = ref([])

// Mapas útiles
const toppingsMap = computed(() => {
  const map = new Map()
  ;(props.platillo.toppings_opcionales || []).forEach(t => {
    map.set(t.nombre, Number(t.precio) || 0)
  })
  return map
})

// Precios
const base = computed(() => Number(props.platillo.precio_base) || 0)
const extraToppings = computed(() =>
  toppingsSeleccionados.value.reduce((sum, n) => sum + (toppingsMap.value.get(n) || 0), 0)
)
const subtotal = computed(() => base.value + extraToppings.value)
const cantidad = ref(1)
const total = computed(() => cantidad.value * subtotal.value)

// Anim/UI
const adding = ref(false)
let cooldownTimer = null

function onAdd(e){
  if (adding.value) return
  adding.value = true

  // construir payload coherente para el carrito
  const toppingsDetallados = (props.platillo.toppings_opcionales || [])
    .filter(t => toppingsSeleccionados.value.includes(t.nombre))
    .map(t => ({ nombre: t.nombre, precio: Number(t.precio) || 0 }))

  // “sin_ingredientes” = removibles que el usuario desmarcó
  const sin_ingredientes = (props.platillo.ingredientes_base || [])
    .filter(i => i.removible !== false)
    .filter(i => !ingredientesSeleccionados.value.includes(i.nombre))
    .map(i => i.nombre)

  const item = {
    id: props.platillo.id,
    nombre: props.platillo.nombre,
    cantidad: cantidad.value,
    precio_base: base.value,
    toppings: toppingsDetallados,          // [{nombre, precio}]
    sin_ingredientes,                      // ["lechuga", ...]
    subtotal: Number(subtotal.value) || 0, // precio por unidad con toppings
    total: Number(total.value) || 0        // cantidad * subtotal
  }

  emit('add', item)

  try { flyToCart(e) } catch {}
  showToast(`Añadido: ${item.nombre}`)

  clearTimeout(cooldownTimer)
  cooldownTimer = setTimeout(()=> adding.value = false, 600)
}

function flyToCart(e){
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  const card = e?.currentTarget?.closest?.('.card')
  const img  = card?.querySelector('img')
  if (!img) return

  const btnCart = document.getElementById('btn-cart') // móvil
  const desktopTarget = document.querySelector('.cart-desktop .cart-total, .cart-desktop h2, .cart-desktop')
  const target = btnCart || desktopTarget
  if (!target) return

  const imgRect = img.getBoundingClientRect()
  const tgtRect = target.getBoundingClientRect()

  const clone = img.cloneNode(true)
  Object.assign(clone.style, {
    position: 'fixed',
    left: imgRect.left + 'px',
    top: imgRect.top + 'px',
    width: imgRect.width + 'px',
    height: imgRect.height + 'px',
    borderRadius: '12px',
    zIndex: 9999,
    pointerEvents: 'none'
  })
  document.body.appendChild(clone)

  const dx = (tgtRect.left + tgtRect.width/2) - (imgRect.left + imgRect.width/2)
  const dy = (tgtRect.top + tgtRect.height/2) - (imgRect.top + imgRect.height/2)

  clone.animate(
    [
      { transform:'translate(0,0) scale(1)', opacity:1 },
      { transform:`translate(${dx*0.6}px, ${dy*0.6}px) scale(.6)`, opacity:.9 },
      { transform:`translate(${dx}px, ${dy}px) scale(.2)`, opacity:0 }
    ],
    { duration: 650, easing: 'cubic-bezier(.2,.8,.2,1)' }
  ).onfinish = () => clone.remove()
}

function showToast(text){
  const el = document.getElementById('toast')
  if (!el) return
  el.textContent = text
  el.classList.add('show')
  setTimeout(()=> el.classList.remove('show'), 900)
}
</script>

<template>
  <div class="card h-100 shadow-sm border-0 retro-dark">
    <!-- Imagen -->
    <img
      :src="platillo.img || `https://via.placeholder.com/600x450?text=${encodeURIComponent(platillo.nombre)}`"
      :alt="platillo.nombre"
      class="card-img-top img-fluid"
    />

    <!-- Cuerpo -->
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ platillo.nombre }}</h5>

      <!-- Ingredientes removibles -->
      <details v-if="(platillo.ingredientes_base || []).length" class="opt mb-2">
        <summary>🚫 Quitar ingredientes</summary>
        <ul class="opt-grid">
          <li v-for="(ing, idx) in platillo.ingredientes_base" :key="idx">
            <label class="opt-row">
              <input
                type="checkbox"
                :value="ing.nombre"
                v-model="ingredientesSeleccionados"
                :disabled="ing.removible === false"
                :checked="ing.removible !== false"
              />
              {{ ing.nombre }}
              <small v-if="ing.removible === false" class="fixed">(fijo)</small>
            </label>
          </li>
        </ul>
      </details>

      <!-- Toppings -->
      <details v-if="(platillo.toppings_opcionales || []).length" class="opt mb-2">
        <summary>➕ Toppings extra</summary>
        <ul class="list-unstyled mt-2">
          <li
            v-for="(t, idx) in platillo.toppings_opcionales"
            :key="idx"
            class="mb-2"
          >
            <div class="d-flex justify-content-between align-items-center">
              <!-- Checkbox + nombre -->
              <label class="d-flex align-items-center gap-2 m-0">
                <input
                  type="checkbox"
                  class="form-check-input"
                  :value="t.nombre"
                  v-model="toppingsSeleccionados"
                />
                {{ t.nombre }}
              </label>

              <!-- Precio -->
              <span v-if="t.precio" class="topping-price">
                + ${{ (Number(t.precio)||0).toFixed(2) }}
              </span>
            </div>
          </li>
        </ul>
      </details>



      <!-- Precio + botón -->
      <div class="mt-auto d-flex justify-content-between align-items-center">
        <span class="price">${{ subtotal.toFixed(2) }}</span>
        <button
          class="btn btn-danger add-btn"
          :disabled="adding"
          @click="onAdd($event)"
        >
          <span v-if="!adding">➕ Agregar</span>
          <span v-else>✅ Agregado</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 🎨 Estilo Retro Gourmet Oscuro */
.retro-dark {
  background: #1a1a1a;   /* Fondo oscuro */
  color: #f5f5f5;        /* Texto claro */
  border-radius: 14px;
}
.retro-dark .card-title {
  color: #ff4444;         /* Rojo apetitoso */
  font-family: 'Bebas Neue', sans-serif;
}
.retro-dark .price {
  color: #ffcc00;         /* Dorado/cheddar */
  font-size: 1.3rem;
  font-weight: bold;
}

/* Animación botón */
.add-btn { transition: transform .06s ease, filter .2s ease; }
.add-btn:active { transform: translateY(1px) scale(.98); }
.add-btn.adding { filter: brightness(1.1); }

/* Opciones (checkbox estilizados) */
.opt { background:#171717; border:1px solid #262626; border-radius:12px; padding:.6rem .8rem; }
.opt + .opt { margin-top:.5rem; }
.opt summary { cursor:pointer; font-weight:600; margin-bottom:.4rem; }
.opt-grid { display:grid; grid-template-columns: 1fr; gap:.35rem; margin-top:.5rem; }
@media (min-width: 768px) { .opt-grid { grid-template-columns: 1fr 1fr; gap: .75rem 1rem;} }
.opt-row { display:flex; align-items:center; justify-content: space-between; gap:.5rem; background: transparent;}
.opt-row input { margin-right: .5rem; }
.opt-row em { margin-left: auto; font-style: normal; opacity: .9; white-space: nowrap; }
.fixed { opacity:.6; margin-left:.25rem; }

/* Imagen efecto hover */
.card-img-top {
  aspect-ratio: 4/3;
  object-fit: cover;
  transition: transform .5s ease;
}
.card:hover .card-img-top { transform: scale(1.05); }

.topping-price {
  color: #ffcc00;      /* amarillo cheddar */
  font-weight: 600;
  font-size: 0.95rem;
  white-space: nowrap; /* evita que se corte */
}


</style>
