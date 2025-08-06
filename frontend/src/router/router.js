// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Menu from '../components/Menu.vue'  // tu menú principal

const routes = [
  { path: '/', component: Menu },
  { path: '/login', component: Login },
  { path: '/registro', component: Register }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
