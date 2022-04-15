// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import * as Echarts from 'echarts'

import {
  api
} from '@/api';
import axios from 'axios'
import qs from 'qs'
Vue.prototype.$qs = qs


axios.defaults.baseURL = 'http://127.0.0.1:5000';
Vue.prototype.$ajax = axios;



Vue.prototype.$echarts = Echarts
Vue.use(ElementUI);

Vue.config.productionTip = false



Vue.prototype.$api = api;//请求接口

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
