// router.js
import { createRouter, createWebHistory } from 'vue-router';

import IssueList from '../components/IssueList.vue';
import IssueDetail from '../components/IssueDetail.vue';

const routes = [
  {
    path: '/',
    component: IssueList,
  },
  {
    path: '/issue/:id',
    name: 'issue-detail',
    component: IssueDetail,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
