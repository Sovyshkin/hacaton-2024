import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router";

import axios from "axios";
// при пустом url запросы автоматически идут на исходный сервер,
// поэтому коренной рут по сути не нужен
axios.defaults.baseURL = "http://localhost:5010/v1";

const app = createApp(App);

app.use(router);

app.mount("#app");
