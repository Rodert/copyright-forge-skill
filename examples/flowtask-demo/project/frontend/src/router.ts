import { createRouter, createWebHistory } from "vue-router";
import LoginView from "./views/LoginView.vue";
import DashboardView from "./views/DashboardView.vue";
import ProjectsView from "./views/ProjectsView.vue";
import TasksView from "./views/TasksView.vue";
import StatusesView from "./views/StatusesView.vue";
import PrioritiesView from "./views/PrioritiesView.vue";
import LabelsView from "./views/LabelsView.vue";
import SearchView from "./views/SearchView.vue";
import StatisticsView from "./views/StatisticsView.vue";
import LogsView from "./views/LogsView.vue";
import SettingsView from "./views/SettingsView.vue";
import ExportsView from "./views/ExportsView.vue";

export default createRouter({ history: createWebHistory(), routes: [
  { path: "/login", component: LoginView }, { path: "/", component: DashboardView },
  { path: "/projects", component: ProjectsView }, { path: "/tasks", component: TasksView },
  { path: "/statuses", component: StatusesView }, { path: "/priorities", component: PrioritiesView },
  { path: "/labels", component: LabelsView }, { path: "/search", component: SearchView },
  { path: "/statistics", component: StatisticsView }, { path: "/logs", component: LogsView },
  { path: "/settings", component: SettingsView }, { path: "/exports", component: ExportsView },
] });
