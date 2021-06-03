import Vue from 'vue'
// import Default from "@/views/Default";
import App from "@/App";
import router from './router'
import VueResource from 'vue-resource'
import Vuetify from "vuetify";

Vue.use(VueResource)
Vue.use(Vuetify)

Vue.config.productionTip = false

new Vue({
    router,
    vuetify: new Vuetify(),
    render: h => h(App),
}).$mount('#app')
