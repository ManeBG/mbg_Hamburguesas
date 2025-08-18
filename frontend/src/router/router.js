// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'

// Componentes existentes
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Menu from '../components/Menu.vue'
import Checkout from '../components/Checkout.vue'

// Lazy load que ya usabas
const AdminPedidos = () => import('../views/AdminPedidos.vue')

// NEW: Home (landing). Si aún no lo tienes, crea src/views/Home.vue
const Home = () => import('../views/Home.vue')

const routes = [
  // Inicio ahora es Home (landing)
  { path: '/', name: 'home', component: Home },

  // Menú va en su propia ruta
  { path: '/menu', name: 'menu', component: Menu },

  // Rutas que ya tenías
  { path: '/login', name: 'login', component: Login },
  { path: '/registro', name: 'registro', component: Register },
  { path: '/checkout', name: 'checkout', component: Checkout },
  { path: '/admin/pedidos', name: 'AdminPedidos', component: AdminPedidos },

  // Catch‑all a Inicio (evita pantallas en negro)
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior () {
    return { top: 0 }
  }
})

export default router
