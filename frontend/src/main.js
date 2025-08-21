import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/router'

// Bootstrap primero
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

// Tu tema después para que gane
import '@/assets/theme.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
