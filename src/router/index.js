import Vue from 'vue'
import VueRouter from 'vue-router'
import Default from '@/views/Default.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Default',
        component: Default,
    },
]

const router = new VueRouter({
    mode:'history',
    routes
})

export default router
