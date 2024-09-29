import { createRouter, createWebHashHistory } from "vue-router";
// import HomeView from "../views/HomeView.vue";
import Login from "../views/Login.vue";
import RegisterServiceman from "@/views/Serviceman/RegisterServiceman.vue";
import RegisterCustomer from "@/views/Customer/RegisterCustomer.vue";
import ServicemanNav from "@/components/ServicemanNav.vue";

//Dashes
import ServiceDash from "@/views/Serviceman/ServiceDash.vue";
import AdminDash from "@/views/Admin/AdminDash.vue";
import CustDash from "@/views/Customer/CustDash.vue";

//Customer
import MyServices from "@/views/Customer/MyServices.vue";
import SearchServices from "@/views/Customer/SearchServices.vue";
import Summary from "@/views/Customer/Summary.vue";
import Servicemen from "@/views/Customer/Servicemen.vue";


//Admin
import AdminServices from "@/views/Admin/AdminServices.vue";
import test from "@/views/Admin/test.vue";


const routes = [
  // {
  //   path: "/",
  //   name: "home",
  //   component: HomeView,
  // },
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/ServiceRegistration",
    name: "ServiceRegistration",
    component: RegisterServiceman,
  },
  {
    path: "/CustomerRegistration",
    name: "CustomerRegistration",
    component: RegisterCustomer,
  },


  //Serviceman Dashboard with navbar and child components
  {
    path: "/Serviceman",
    name: "ServicemanNav",
    component: ServicemanNav,
    children:[
    ]
  },

//Customer Dashboard with navbar and child components
{
  path: '/Custdash',
  name: 'Custdash',
  component: CustDash,
  children: [
    {
      path: 'MyServices',
      name: 'MyServices',
      component: MyServices
    },
    {
      path: 'SearchServices',
      name: 'SearchServices',
      component: SearchServices
    },
    {
      path: 'Summary',
      name: 'Summary',
      component: Summary
    }
  ]
},
  // {
  //   path: "/Customer",
  //   name: "CustomerNav",
  //   component: CustomerNav,
  //   children:[

  //   ]
  // },
  {
    path: "/adminDash",
    name: "adminDash",
    component: AdminDash,
    children:[
      {
        path: 'Services',
        name: 'Services',
        component: AdminServices
      },
      {
        path: 'test',
        name: 'test',
        component: test
      },
      // {
      //   path: 'Servicemen',
      //   name: 'Servicemen',
      //   component: viewServicemen
      // },
      
    ]
  },
  // {
  //   path: "/about",
  //   name: "about",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  // },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;


// {
//   path: '/Udashboard',
//   name: 'Udashboard',
//   component: Udash,
//   children: [
//     {
//       path: 'my-books',
//       name: 'mybooks',
//       component: UmyBooks
//     },
//     {
//       path: 'all-books',
//       name: 'allbooks',
//       component: UallBooks
//     },
//     {
//       path: 'stats',
//       name: 'stats',
//       component: Ustats
//     }
//   ]
// },
