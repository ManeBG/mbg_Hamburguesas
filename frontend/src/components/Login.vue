<template>
  <div class="auth-container">
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="login">
      <label>Correo:
        <input type="email" v-model="correo" required />
      </label>
      <label>Contraseña:
        <input type="password" v-model="password" required />
      </label>
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const correo = ref("")
const password = ref("")
const error = ref("")

const login = async () => {
  try {
    const res = await fetch("http://localhost:5000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correo.value, password: password.value })
    })

    const data = await res.json()

    if (!res.ok) {
      error.value = data.error || "Error al iniciar sesión"
      return
    }

    localStorage.setItem("user_id", data.user_id)
    alert("✅ Bienvenido, sesión iniciada")
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
