# FlowTask个人任务与项目管理系统 V1.0

著作权人：FlowTask Demo Studio（公开测试数据，非真实主体）

## 1. 软件概述

FlowTask 是一个个人任务与项目管理系统。系统采用 Vue 3、TypeScript 和 Vite 构建前端界面，使用 FastAPI 提供 API，并将项目、任务、标签、日志和设置保存在 SQLite 数据库中。

## 2. 登录与工作台

用户在登录页面输入邮箱和密码后调用 `/api/auth/login`。工作台调用 `/api/dashboard`，展示全部任务、已完成任务和高优先级任务数量，并显示近期任务和项目概览。

## 3. 项目与任务管理

项目管理页面调用 `/api/projects` 查询和创建项目。任务管理页面调用 `/api/tasks` 创建任务、按状态筛选任务，并显示任务标题、状态和优先级。任务数据保存项目关联、截止日期和标签信息。

## 4. 状态、优先级与标签

系统通过 `/api/task-statuses` 提供待办、进行中和已完成状态；通过 `/api/priorities` 提供高、中、低优先级；通过 `/api/labels` 查询和创建标签。三类数据均在对应页面显示和管理。

## 5. 搜索、统计与日志

搜索页面调用 `/api/search` 对项目名称、任务标题和标签进行查询。统计页面调用 `/api/statistics` 汇总任务状态和优先级。操作日志页面调用 `/api/operation-logs` 展示项目和任务操作记录。

## 6. 设置与导出

设置页面通过 `/api/settings` 查询用户设置，并可通过 `PUT /api/settings/{key}` 更新设置。数据导出页面调用 `/api/exports/tasks`，将任务字段生成 CSV 下载文件。

## 7. 运行环境

后端需要 Python 3.9+、FastAPI 和 SQLite；前端需要 Node.js、Vue 3、TypeScript 和 Vite。项目的运行步骤见 `project/README.md`。
