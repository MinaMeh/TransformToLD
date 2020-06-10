import Vue from "vue";
import Router from "vue-router";
import Home from "./components/Home.vue";
import Project from "./components/Project.vue";
import ProjectList from "./components/ProjectsList.vue";

Vue.use(Router);

export default new Router({
    mode: "history",
    routes: [{
            path: "/",
            name: "Home",
            component: Home
        },
        {
            path: "/projects-list",
            name: "projects",
            component: ProjectList
        },
        {
            path: "/projects/:id",
            name: "project-details",
            component: Project
        },
    ]
});