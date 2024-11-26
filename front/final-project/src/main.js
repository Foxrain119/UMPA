import "@/assets/main.css";

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// AOS
// import AOS from 'aos';
// import "aos/dist/aos.css";

// new Vue({
//     created() {
//         AOS.init();
//     },
//   el: '#app',
//   router,
//   render: h => h(App)
// })
import AOS from 'aos';
import 'aos/dist/aos.css'; // You can also use <link> for styles
// ..
AOS.init();
// 카카오맵 API 스크립트 로드
const script = document.createElement('script')
script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&libraries=services,clusterer,drawing&autoload=false`

// 스크립트 로드 완료 후 카카오맵 초기화
script.onload = () => {
  window.kakao.maps.load(() => {
    console.log('Kakao Maps API loaded successfully');
  });
};

document.head.appendChild(script)

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.mount('#app')
