import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router'  // ✅ sin .js?? usa la ruta correcta si se llama router.js
import '@/assets/theme.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


const app = createApp(App)
app.use(router)               // ✅ aquí conectas Vue con el enrutador
app.mount('#app')
