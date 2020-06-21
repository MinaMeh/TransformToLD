import Home from "./components/Home";
import Login from "@/components/AuthComponents/Login";
import Register from "@/components/AuthComponents/Register";
import Transform from "./components/Transform";
import VueRouter from "vue-router";
import Vue from "vue";

const routes = [
  {
    path: "/",
    component: Home,
    name: "home",
    meta: {
      requiresLogin: true,
    },
  },
  {
    path: "/transform",
    component: Transform,
    name: "transform",
    meta: {
      requiresLogin: true,
    },
  },

  {
    path: "/login",
    component: Login,
    name: "login",
  },
  {
    path: "/signup",
    component: Register,
    name: "signup",
  },
];
Vue.use(VueRouter);
const router = new VueRouter({ routes });
router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/signup"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("t");

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) {
    next("/login");
  } else {
    next();
  }
});

export default router;