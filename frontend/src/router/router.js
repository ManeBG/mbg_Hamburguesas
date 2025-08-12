// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Menu from '../components/Menu.vue'  // tu menú principal
import Checkout from "../components/Checkout.vue"  //agregado recientemente

// Lazy load de la vista (colócala en: frontend/src/views/AdminPedidos.vue)
const AdminPedidos = () => import('../views/AdminPedidos.vue')


const routes = [
  { path: '/', component: Menu },
  { path: '/login', component: Login },
  { path: '/registro', component: Register },
  { path: "/checkout", component: Checkout },   //agregado recientemente
  { path: '/admin/pedidos', name: 'AdminPedidos', component: AdminPedidos },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
