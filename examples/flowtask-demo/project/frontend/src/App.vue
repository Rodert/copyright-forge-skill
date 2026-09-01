<script setup lang="ts">
const nav = [["/", "工作台"], ["/projects", "项目"], ["/tasks", "任务"], ["/labels", "标签"], ["/statistics", "统计"], ["/settings", "设置"]];
</script>
<template><div class="shell"><aside><strong>FlowTask</strong><small>个人任务与项目管理</small><RouterLink v-for="item in nav" :key="item[0]" :to="item[0]">{{ item[1] }}</RouterLink></aside><main><RouterView /></main></div></template>
