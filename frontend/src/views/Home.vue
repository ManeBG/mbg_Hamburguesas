<!-- src/views/Home.vue -->
<script setup>
import { ref, onMounted } from 'vue'

const horarioHoy = ref('')

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:5000/api/horarios')
    const data = await res.json()

    const hoy = new Date().toLocaleDateString('es-MX', { weekday: 'long' }).toLowerCase()

    const dia = data.find(h => h.dia.toLowerCase() === hoy)
    if (dia && dia.activo) {
      horarioHoy.value = `Hoy abrimos de ${dia.apertura} a ${dia.cierre}`
    } else {
      horarioHoy.value = 'Hoy estamos cerrados'
    }
  } catch (err) {
    console.error('Error cargando horario:', err)
    horarioHoy.value = 'No se pudo cargar el horario'
  }
})
</script>

<template>
  <section class="container" style="padding-block:1rem;">
    <h1>🍔 ¡Bienvenido!</h1>
    <p>Arma tu smash con queso, tocino y más.</p>
    <router-link class="btn btn-primary" to="/menu">Ver menú</router-link>

    <div style="margin-top:1rem;">
      <h3>📅 Horario de hoy</h3>
      <p>{{ horarioHoy }}</p>
    </div>
  </section>
</template>
