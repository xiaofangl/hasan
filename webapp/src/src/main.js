// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './assets/theme/index.css'
import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import axios from 'axios'
import moment from 'moment'

Vue.use(VueRouter);
Vue.use(ElementUI);


Vue.prototype.passport = '/api_passport/';
Vue.prototype.ym_api = '/api/v1/';
Vue.prototype.jks_api = '/api_jks/';
Vue.prototype.dns_api = '/api_dns/';
Vue.prototype.deploy_api = '/api_deploy/';
Vue.prototype.upload_api = '/api_upload/';
Vue.prototype.cmdb_api = '/api_cmdb/';
axios.defaults.headers.common['Authorization'] = window.localStorage.getItem('userhashid');
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
Vue.prototype.$http = axios;

import App from './App'
import routes from './routes'
import store from './store'
import components from './components/'

// Vue.config.productionTip = false

export const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: routes,
  scrollBehavior (to, from, savedPosition) {
    return {x: 0, y: 0}
  }
});

Object.keys(components).forEach((key) => {
  let name = key.replace(/(\w)/, (v) => v.toUpperCase()); // 首字母大写
  Vue.component(`hs${name}`, components[key])
});
Vue.filter('moment', function (value, formatString) {
  formatString = formatString || 'YYYY-MM-DD HH:mm:ss';
  return moment(value).format(formatString)
});

Vue.filter('date', function (value, formatString) {
  formatString = formatString || 'YYYY-MM-DD';
  return moment(value).format(formatString)
});

router.beforeEach((to, from, next) => {
  // let {auth = true} = to.meta;
  // let isLogin = Boolean(window.localStorage.getItem('userhashid'));
  //
  // if (auth && !isLogin) {
  //     return next({path: '/login'})
  // }

  Vue.prototype.ym_path = {to: to, from: from};
  store.commit('addTab', to.name);
  next()
});


/* eslint-disable no-new */
Vue.prototype.bus = new Vue();

new Vue({
  router,
  store,
  ...App
}).$mount('#app');
