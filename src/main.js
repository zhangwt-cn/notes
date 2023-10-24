// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 导入路由配置

const app = createApp(App);
app.use(router); // 使用路由
app.mount('#app');
