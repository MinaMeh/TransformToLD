import Home from "@/components/Home";
import Login from "@/components/AuthComponents/Login";
import Transform from "@/components/Transform";
import Project from "@/components/projects/Project";
import ProjectsList from "@/components/projects/ProjectsList";
import VueRouter from "vue-router";
import Vue from "vue";
import HomePage from "@/components/HomePage";
const routes = [
  {
    path: "/",
    component: HomePage,
    name: "homePage",
  },
  {
    path: "/home",
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
    path: "/projects-list",
    name: "projects",
    component: ProjectsList,
  },
  {
    path: "/projects/:id",
    name: "project-details",
    component: Project,
  },
];
Vue.use(VueRouter);
const router = new VueRouter({
  mode: "history",
  routes,
});
router.beforeEach((to, from, next) => {
  const publicPages = ["/login", "/signup", "/"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("t");
  // trying to access a restricted page + not logged in
  // redirect to login page
  if (to.path == "/" && loggedIn) {
    next("/home");
  } else {
    next();
  }

  if (authRequired && !loggedIn) {
    next("/login");
  } else {
    next();
  }
});
export default router;
