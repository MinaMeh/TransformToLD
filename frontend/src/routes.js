import Login from './components/authenticationComponents/Login.vue';
//import Dismiss from './components/authenticationComponents/Dismiss.vue';
import Home from './components/Home.vue';
import {
    authMixin
} from './mixins/authMixin';

export const routes = [{
        path: '/',
        component: Login
    },
    {
        path: '/home',
        component: Home,
        beforeEnter: (to, from, next) => {
            authMixin.methods.checkToken("google", next)
        }
    },
]