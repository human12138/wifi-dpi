import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import history from '@/components/history'
import parserinfo from '@/components/parserinfo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/history',
      name: 'history',
      component: history
    },
    {
      path: '/parserinfo',
      name: 'parserinfo',
      component: parserinfo
    }
  ]
})
