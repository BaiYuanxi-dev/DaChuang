import objFetch, {
  fetch
} from "./apiConfig"
import {
  baseUrl,
  baseImgPath
} from '@/config'
import Vue from '@/main.js'
import qs from 'qs'
import apiList from './api'

const api = {};

apiList.forEach((item, index) => {
  if (item.type === 'url') {
    api[item.name] = baseUrl + item.url;

  } else {
    api[item.name] = (params, config) => {
      let param = ''
      if (config && config.urlParam) { //url拼接参数  config:{urlParam:'参数拼接字符串'}
        param += '/' + config.urlParam;
      }
      if (config && config.params) { //get请求方式传参：{}，{params:{get参数}}
        param += '?' + qs.stringify(config.params);
      }
      return fetch(baseUrl + item.url + param, {
        method: item.method,
        headers: (() => {
          let obj = {};
          if (config && config.type && config.type === 'file') {

          } else { //设置json格式传参  config： {type:'json'}
            obj['Content-Type'] = config && config.type && config.type === 'json' ? 'application/json' : 'application/x-www-form-urlencoded';
          }
          if (config && config.header) {
            obj['C-S-RANDOM'] = config.header['C-S-RANDOM'];
          }
          //解决分布式验证码失效问题
          if (config && config['VERIFICATION-CODE']) {
            obj['VERIFICATION-CODE'] = config['VERIFICATION-CODE'];
          }
          if (localStorage.getItem("isLogin")) {
            obj['C-S-RANDOM'] = localStorage.getItem("C-S-RANDOM");
          }
          return obj;
        })(),
        body: (() => {
          if (config && config.type && config.type === 'file') {
            return params;
          } else if (item.method === 'post' && config && config.type && config.type === 'json') {
            return JSON.stringify(params)
          } else if (item.method === 'post') {
            return qs.stringify(params);
          } else {
            return null;
          }
        })(),
        credentials: 'include',
        notToJson: config && config.notToJson ? true : false
      })
    }

  }
});
//相应拦截器
objFetch.interceptors_after.push((res, next) => {
  if (res && res.code && res.code === '530' && localStorage.getItem("isLogin")) {
    Vue.$message.warning("登录过期,请重新登录");
    localStorage.setItem("toRoute", window.location.href);
    setTimeout(() => Vue.$router.push("/login"), 500)
  } else if (res && res.code && res.code === '530') {
    localStorage.setItem("toRoute", window.location.href);
    setTimeout(() => Vue.$router.push("/login"), 500)
  } else {
    next();
  }
})
export {
  api
}
