<template>
  <div class="p-4">
    <h1 class="title">Panel de pedidos</h1>

    <div class="toolbar">
      <select v-model="filtroEstado" @change="cargar" class="input">
        <option value="pendiente">Pendientes</option>
        <option value="confirmado">Confirmados</option>
        <option value="en_preparacion">En preparación</option>
        <option value="en_camino">En camino</option>
        <option value="entregado">Entregados</option>
        <option value="cancelado">Cancelados</option>
        <option value="todos">Todos</option>
      </select>

      <input v-model="q" @keyup.enter="cargar" class="input" placeholder="Buscar nombre o teléfono" />
      <button @click="cargar" class="btn">Actualizar</button>
    </div>

    <div v-if="cargando">Cargando…</div>

    <table v-else class="tbl">
      <thead>
        <tr>
          <th>#</th><th>Cliente / Dirección</th><th>Teléfono</th><th>Total</th><th>Estado</th><th>Fecha</th><th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="p in pedidos" :key="p.id">
          <tr>
            <td>{{ p.id }}</td>
            <td>
              <div class="strong">{{ p.nombre || '—' }}</div>
              <div class="muted">{{ p.direccion || 'Sin dirección' }}</div>
            </td>
            <td>
              <a :href="'https://wa.me/52' + (p.telefono || '')" target="_blank">
                {{ formatoTel(p.telefono) }}
              </a>
            </td>
            <td>${{ Number(p.total).toFixed(2) }}</td>
            <td>
              <span class="badge" :style="badgeStyle(p.estado)">{{ etiquetaEstado(p.estado) }}</span>
            </td>
            <td>{{ formatearFecha(p.creado_en) }}</td>
            <td>
              <div class="acciones">
                <button class="btn-ghost" @click="toggleDetalles(p.id)">Detalles</button>
                <button class="btn-ghost" @click="abrirWhats(p)">WhatsApp</button>
                <button v-for="e in nextEstados(p.estado)" :key="e" class="btn" @click="cambiarEstado(p, e)">
                  Marcar {{ etiquetaEstado(e) }}
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="detallesAbiertos.has(p.id)">
            <td colspan="7" class="detalles">
              <ul class="lista-detalles">
                <li v-for="(it, idx) in p.items" :key="idx" class="item">
                  <div class="strong">
                    {{ it.cantidad || 1 }} × {{ it.producto }}
                    — ${{ ((it.cantidad || 1) * Number(it.precio_unitario)).toFixed(2) }}
                  </div>
                  <div v-if="it.toppings?.length" class="muted">Con: {{ it.toppings.join(', ') }}</div>
                  <div v-if="it.sin?.length" class="muted">Sin: {{ it.sin.join(', ') }}</div>
                  <div v-if="it.nota" class="muted"><em>Nota:</em> {{ it.nota }}</div>
                </li>
              </ul>
            </td>
          </tr>
        </template>
      </tbody>
    </table>

    <div v-if="total > pageSize" class="paginador">
      <button :disabled="page<=1" @click="page--; cargar()">«</button>
      <span>Página {{ page }} / {{ Math.ceil(total/pageSize) }}</span>
      <button :disabled="page>=Math.ceil(total/pageSize)" @click="page++; cargar()">»</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Swal from 'sweetalert2'

const pedidos = ref([])
const cargando = ref(false)
const filtroEstado = ref('pendiente')
const q = ref('')
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const detallesAbiertos = ref(new Set())

function badgeStyle(estado){
  const map = {
    pendiente:       { bg:'#FEF3C7', fg:'#92400E' },
    confirmado:      { bg:'#E0F2FE', fg:'#075985' },
    en_preparacion:  { bg:'#EDE9FE', fg:'#5B21B6' },
    en_camino:       { bg:'#DBEAFE', fg:'#1E40AF' },
    entregado:       { bg:'#DCFCE7', fg:'#166534' },
    cancelado:       { bg:'#F3F4F6', fg:'#374151' },
  }
  const s = map[estado] || { bg:'#EEE', fg:'#333' }
  return { background:s.bg, color:s.fg, padding:'2px 8px', borderRadius:'999px', fontSize:'12px' }
}
function etiquetaEstado(e){
  return {
    pendiente:'pendiente',
    confirmado:'confirmado',
    en_preparacion:'en preparación',
    en_camino:'en camino',
    entregado:'entregado',
    cancelado:'cancelado'
  }[e] || e
}
function nextEstados(actual){
  return {
    pendiente:      ['confirmado','cancelado'],
    confirmado:     ['en_preparacion','cancelado'],
    en_preparacion: ['en_camino','cancelado'],
    en_camino:      ['entregado','cancelado'],
    entregado:      [],
    cancelado:      []
  }[actual] || []
}
function formatearFecha(ts){ try { return new Date(ts).toLocaleString() } catch { return ts } }
function formatoTel(t){ return t ? `${t.slice(0,2)} ${t.slice(2,6)} ${t.slice(6)}` : '—' }
function toggleDetalles(id){ detallesAbiertos.value.has(id) ? detallesAbiertos.value.delete(id) : detallesAbiertos.value.add(id) }

async function cargar(){
  cargando.value = true
  try{
    const params = new URLSearchParams()
    if (filtroEstado.value && filtroEstado.value !== 'todos') params.set('estado', filtroEstado.value)
    if (q.value) params.set('q', q.value)
    params.set('page', String(page.value))
    params.set('page_size', String(pageSize.value))
    const res = await fetch(`/api/admin/pedidos?${params.toString()}`)
    const j = await res.json()
    pedidos.value = j.pedidos || []
    total.value = j.total || 0
  }catch(err){
    console.error(err)
    Swal.fire('Ups', 'No pude cargar pedidos', 'error')
  }finally{
    cargando.value = false
  }
}

async function cambiarEstado(p, nuevo){
  try{
    const res = await fetch(`/api/pedidos/${p.id}/status`, {
      method:'PATCH',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({ estado: nuevo })
    })
    const j = await res.json()
    if (!res.ok) throw new Error(j?.error || 'No se pudo actualizar el estado')

    p.estado = nuevo
    Swal.fire({ toast:true, position:'top-end', timer:1500, showConfirmButton:false, icon:'success',
      title:`Pedido #${p.id} → ${etiquetaEstado(nuevo)}` })
  }catch(err){
    console.error(err)
    Swal.fire('Error', err.message, 'error')
  }
}

function abrirWhats(p){
  const tel = `52${(p.telefono || '').replace(/\D/g,'')}`
  const texto = encodeURIComponent(
    `Hola ${p.nombre || ''}, tu pedido #${p.id} está ${etiquetaEstado(p.estado)}.\nTotal: $${Number(p.total).toFixed(2)}\n` +
    (p.items?.length ? p.items.map(it => `• ${it.cantidad || 1}× ${it.producto}`).join('\n') : '')
  )
  window.open(`https://wa.me/${tel}?text=${texto}`, '_blank')
}

onMounted(cargar)
</script>

<style scoped>
.title{ font-weight:700; font-size:1.25rem; }
.toolbar{ display:flex; gap:.5rem; align-items:center; margin:.75rem 0; flex-wrap:wrap; }
.input{ border:1px solid #d1d5db; border-radius:8px; padding:.4rem .6rem; }
.btn{ border:1px solid #111827; background:#111827; color:white; border-radius:8px; padding:.35rem .6rem; }
.btn-ghost{ border:1px solid #070707; background:rgb(7, 7, 7); border-radius:8px; padding:.35rem .6rem; }
.tbl{ width:100%; border-collapse:collapse; }
.tbl th,.tbl td{ text-align:left; padding:.5rem .5rem; border-bottom:1px solid #0d0d0e; vertical-align:top; }
.muted{ font-size:12px; color:#6b7280; max-width:520px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.strong{ font-weight:600; }
.acciones{ display:flex; flex-wrap:wrap; gap:.4rem; }
.detalles{ background:#f7f7f8; }
.lista-detalles{ display:grid; gap:.5rem; padding:.75rem; margin:0; }
.item{ border:1px solid #e5e7eb; border-radius:8px; padding:.5rem .6rem; background:white; list-style:none; }
.paginador{ margin-top:.75rem; display:flex; align-items:center; gap:.5rem; }
.badge{ display:inline-block; }
</style>
