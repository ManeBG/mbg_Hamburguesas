// src/router/router.js
import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Menu from '../components/Menu.vue'  // tu menú principal
import Checkout from "../components/Checkout.vue"  //agregado recientemente

const routes = [
  { path: '/', component: Menu },
  { path: '/login', component: Login },
  { path: '/registro', component: Register },
  { path: "/checkout", component: Checkout }   //agregado recientemente
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
