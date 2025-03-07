import { createApp } from 'vue'
import './style.css'
import 'floating-vue/dist/style.css'
import FloatingVue from "floating-vue"
import App from './App.vue'

createApp(App).use(FloatingVue).mount('#app')
