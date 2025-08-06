<template>
  <div class="auth-container">
    <h2>Crear cuenta</h2>
    <form @submit.prevent="register">
      <label>Nombre:
        <input v-model="nombre" required />
      </label>
      <label>Correo:
        <input type="email" v-model="correo" required />
      </label>
      <label>Teléfono:
        <input v-model="telefono" required />
      </label>
      <label>Contraseña:
        <input type="password" v-model="password" required />
      </label>
      <button type="submit">Registrarse</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const nombre = ref("")
const correo = ref("")
const telefono = ref("")
const password = ref("")
const error = ref("")

const register = async () => {
  try {
    const res = await fetch("http://localhost:5000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre: nombre.value,
        correo: correo.value,
        telefono: telefono.value,
        password: password.value
      })
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.error || "Error al registrar"
      return
    }

    localStorage.setItem("user_id", data.user_id)
    alert("✅ Registro exitoso, sesión iniciada")
    error.value = ""
  } catch (err) {
    error.value = "Error de conexión"
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: auto;
  padding: 1rem;
}
</style>
