import { createRouter, createWebHashHistory } from "vue-router";
// import HomeView from "../views/HomeView.vue";
import Login from "../views/SignIn.vue";
import RegisterServiceman from "@/views/Serviceman/ProviderRegistration.vue";
import RegisterCustomer from "@/views/Consumer/ConsumerRegistration.vue";


//Dashes
import ServiceDash from "@/views/Serviceman/ProviderDashboard.vue";
import AdminDash from "@/views/Admin/AdministratorDashboard.vue";
import CustDash from "@/views/Consumer/ConsumerDashboard.vue";

//Customer
import MyServices from "@/views/Consumer/ConsumerProvisions.vue";
import SearchServices from "@/views/Consumer/ConsumerSearchProvisions.vue";
import Summary from "@/views/Consumer/ConsumerStatsPage.vue";
import custEditProf from "@/views/Consumer/ConsumerProfileUpdate.vue";

//Servicemen
import Requests from "@/views/Serviceman/ProviderRequests.vue";
import History from "@/views/Serviceman/ProviderStatsPage.vue";
import Editprof from "@/views/Serviceman/ProviderProfileUpdate.vue";

//Admin
import AdminProvisions from "@/views/Admin/AdministratorProvisions.vue";
import AdminStats from "@/views/Admin/AdministratorStaticstics.vue";
import ApprovalCentre from "@/views/Admin/AdministratorApprovalCentre.vue";

const routes = [
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
    path: "/ServiceDash",
    name: "ServiceDash",
    component: ServiceDash,
    children:
    [
      {
        path: 'history',
        name: 'history',
        component: History
      },      
      {
        path: 'requests',
        name: 'requests',
        component: Requests
      },      
      {
        path: 'editProfile',
        name: 'editProfile',
        component: Editprof
      },
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
    },
    {
      path: 'editProf',
      name: 'editProf',
      component: custEditProf
    }
  ]
},
  {
    path: "/adminDash",
    name: "adminDash",
    component: AdminDash,
    children:[
      {
        path: 'Services',
        name: 'Services',
        component: AdminProvisions
      },
      {
        path: 'allrequests',
        name: 'allrequests',
        component: AdminStats
      },
      {
        path: 'ApprovalCentre',
        name: 'ApprovalCentre',
        component: ApprovalCentre
      },

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