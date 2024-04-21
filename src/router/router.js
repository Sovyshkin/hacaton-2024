import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/components/AppLogin.vue";
import AppRegister from "@/components/AppRegister.vue";
import AppHome from "@/components/AppHome.vue";
import AppProfile from "@/components/AppProfile.vue";
import CreateVuz from "@/components/CreateVuz.vue";
import CreateNews from "@/components/CreateNews.vue";
import AppEntry from "@/components/AppEntry.vue";
import ProfileVuz from "@/components/ProfileVuz.vue";
import PublishEvent from "@/components/PublishEvent.vue";
import AppEvent from "@/components/AppEvent.vue";
import AppLenta from "@/components/AppLenta.vue";
import EvenstLenta from "@/components/EventsLenta.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: AppHome,
    },
    {
      path: "/login",
      name: "log",
      component: AppLogin,
    },
    {
      path: "/registration",
      name: "reg",
      component: AppRegister,
    },
    {
      path: "/profile",
      name: "profile",
      component: AppProfile,
    },
    {
      path: "/vuz_registration",
      name: "vuzregister",
      component: CreateVuz,
    },
    {
      path: "/publish_news",
      name: "publishnews",
      component: CreateNews,
    },
    {
      path: "/entry",
      name: "entry",
      component: AppEntry,
    },
    {
      path: "/vuz",
      name: "vuz",
      component: ProfileVuz,
    },
    {
      path: "/publish_event",
      name: "publishevent",
      component: PublishEvent,
    },
    {
      path: "/event",
      name: "event",
      component: AppEvent,
      props: true,
    },
    {
      path: "/lenta",
      name: "lenta",
      component: AppLenta,
      props: true,
    },
    {
      path: "/events",
      name: "events",
      component: EvenstLenta,
      props: true,
    },
  ],
});

export default router;
