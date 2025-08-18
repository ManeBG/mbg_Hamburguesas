<!-- src/components/ProductCard.vue
<script setup>
import { ref } from 'vue'

const props = defineProps({
  producto: { type: Object, required: true }
})
const emit = defineEmits(['add'])

const adding = ref(false)
let cooldownTimer = null

function onAdd(e){
  if (adding.value) return
  adding.value = true

  // 1) actualiza store/padre
  emit('add', props.producto)

  // 2) animación
  try { flyToCart(e) } catch (_) {}

  // 3) feedback rápido
  const el = document.getElementById('toast')
  if (el){
    el.textContent = `Añadido: ${props.producto.nombre}`
    el.classList.add('show')
    setTimeout(()=> el.classList.remove('show'), 900)
  }

  clearTimeout(cooldownTimer)
  cooldownTimer = setTimeout(()=> adding.value = false, 600)
}

function flyToCart(e){
  // Respeta reduced-motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  // ORIGEN: imagen de esta card
  const card = e?.currentTarget?.closest?.('.card')
  const img  = card?.querySelector('img')
  if (!img) return

  // DESTINO:
  // 1) móvil: #btn-cart (barra)
  // 2) escritorio: bloque del carrito en página
  const btnCart = document.getElementById('btn-cart')
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

  const anim = clone.animate([
    { transform:'translate(0,0) scale(1)', opacity:1 },
    { transform:`translate(${dx*0.6}px, ${dy*0.6}px) scale(.6)`, opacity:.9 },
    { transform:`translate(${dx}px, ${dy}px) scale(.2)`, opacity:0 }
  ], { duration: 650, easing: 'cubic-bezier(.2,.8,.2,1)' })

  anim.onfinish = () => {
    clone.remove()
    // “bump” si existe botón móvil
    if (btnCart){
      btnCart.classList.remove('bump')
      // reflow
      // eslint-disable-next-line no-unused-expressions
      btnCart.offsetWidth
      btnCart.classList.add('bump')
      setTimeout(()=> btnCart.classList.remove('bump'), 280)
    }
  }
}
</script>

<template>
  <article class="card">
    <div class="card-media">
      <img :src="producto.img" :alt="producto.nombre" loading="lazy" decoding="async" />
    </div>

    <div class="card-body">
      <h3 class="card-title">{{ producto.nombre }}</h3>
      <p class="card-desc">{{ producto.desc }}</p>

      <div class="card-meta">
        <span class="price">${{ Number(producto.precio).toFixed(2) }}</span>

        <!-- OJO: pasa el evento -->
        <!-- <button
          class="btn btn-primary add-btn"
          :class="{ adding }"
          @click="onAdd($event)"
        >
          <span v-if="!adding">➕ Agregar</span>
          <span v-else>✅ Agregado</span>
        </button>
      </div>
    </div>
  </article>
</template>

<style>
.add-btn { transition: transform .06s ease, filter .2s ease; }
.add-btn:active { transform: translateY(1px) scale(.98); }
.add-btn.adding { filter: brightness(1.1); }

.card { background:#1a1a1a; border-radius:18px; overflow:hidden; display:grid; grid-template-rows:auto 1fr; box-shadow:0 1px 0 #222; }
.card-media img{ width:100%; aspect-ratio:4/3; object-fit:cover; transition: scale .5s ease; }
.card:hover .card-media img{ scale:1.05; }
.card-body{ padding:1rem; display:grid; gap:.5rem; }
.card-meta{ display:flex; align-items:center; justify-content:space-between; gap:.8rem; }
.price{ color:#FFC531; font-weight:800; }
</style> --> -->
