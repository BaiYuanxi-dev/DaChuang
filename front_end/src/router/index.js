// import Vue from 'vue'
// import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/pages/Home'
import link_try from '@/pages/link_try'
// Vue.use(Router)

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'Login',
//       component: Login
//     },
//     {
//       path: '/Login',
//       name: 'Login',
//       component: Login
//     },
//     {
//       path: '/Home',
//       name: 'Home',
//       component: Home
//     },
//     {
//       path: '/link_try',
//       name: 'link_try',
//       component: link_try
//     },
//   ]
// })


import Vue from 'vue'
import Router from 'vue-router'
// import Global from '@/assets/Global.vue'
// Vue.prototype.Global = Global;

Vue.use(Router)
import {
  routerMode
} from '@/config'

// 导出默认的新路由器


const router = new Router({
  mode: routerMode,
  base: '/',
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/link_try',
      name: 'link_try',
      component: link_try
    },
  ]
})


router.beforeEach((to, from, next) => {
  //to表示将要访问的路径
  //from表示从哪个路径跳转过来
  //next是个函数表示放行
  if (to.matched.some(m => m.meta.auth)) {
    // 对路由进行验证判断是否登录
    if (!localStorage.getItem("isFirst")) {
      api.judgeIslogin().then(res => {
        if (res.success) {
          localStorage.setItem("isFirst", '1');
          next();
        } else {
          localStorage.setItem("toRoute", window.location.href)
          next({
            path: '/login'
          })
        }
      });
    } else {
      next();
    }
  } else {
    if (localStorage.getItem("isFirst")) {
      localStorage.removeItem("isFirst")
    }
    next()
  }

  // 处理页面title
  if (to.meta.title) {
    document.title = to.meta.title;
  }
})
// 路由切换后滚动条滚动到页面顶部
router.afterEach((to, from, next) => {
  window.scrollTo(0, 0);
});

export default router;

const originalPush = Router.prototype.push
Router.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}