# Copyright Forge Skill

> 把真实软件项目变成可追溯、可检查、可继续修改的软著材料。

[简体中文](README.md) | [English](docs/README.en.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md) | [Русский](docs/README.ru.md) | [Français](docs/README.fr.md)

你不需要学习软著流程，也不需要填写一长串专业字段。打开自己的代码项目后，直接对 Agent 说：

```text
帮我给这个项目做一套软著材料。
```

这不是填写模板，也不是让 AI 根据项目名称编造功能。Copyright Forge 会读取真实代码、建立功能证据、确认无法从代码判断的事实，再生成材料并进行独立审核。

项目站点：[rodert.github.io/copyright-forge-skill](https://rodert.github.io/copyright-forge-skill/)

## 直接交给 Agent

复制下面文字并发送给你的 Agent，即可让它安装并使用本 Skill：

```text
请从 https://github.com/Rodert/copyright-forge-skill 安装 Copyright Forge Skill，并按其 SKILL.md 工作。

我会在真实项目中用自然语言说明需求，例如“帮我给这个项目做软著”或“继续完成刚才的软著材料”。请先自行分析项目、文档、配置和代码，建立可追溯的功能证据；不要一开始向我索要申请字段。只把无法从项目确定的权属、开发关系、真实日期和公开使用事实，用普通人语言集中向我确认。

不得虚构功能、源码、截图、权属、开发关系、发表事实或日期；不得修改原项目；所有输出必须写到项目之外的独立目录。说明书中的功能必须有项目证据。确认后锁定同一份事实源，生成后独立复查一致性、证据和敏感信息，不得伪造官方申请表或承诺登记结果。
```

## 安装

以下命令为首次全局安装。仓库保留为 Git 检出，Skill 使用符号链接引用它，因此每天首次处理材料时可以检查并获取更新。目标目录已经存在时，先处理已有安装，避免覆盖本地修改。

### Claude Code

“Cloud Code” 如指 Claude Code，请执行：

```bash
CF_SKILL_HOME="$HOME/.claude"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新打开 Claude Code 后，直接说“帮我给当前项目做软著”，或调用 `/copyright-forge`。

### Codex

```bash
CF_SKILL_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新开始 Codex 会话后，直接提出软著需求，或显式调用 `$copyright-forge`。

### OpenCode

```bash
CF_SKILL_HOME="$HOME/.config/opencode"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新打开 OpenCode 后，直接描述要做的软著任务即可。

各工具目录约定见 [Claude Code Skills](https://code.claude.com/docs/en/skills)、[Codex Skills](https://developers.openai.com/codex/skills/) 与 [OpenCode Skills](https://opencode.ai/docs/skills/) 官方文档。

## 使用

在你的项目根目录打开 Agent，然后自然表达目标：

```text
帮我给当前项目做软著。
帮我看看这个项目申请软著还缺什么。
继续帮我完成软著材料。
帮我重新检查一下刚才生成的材料。
这是版权中心让我补正的内容，帮我看看怎么改。
帮我检查软著材料规则有没有更新。
```

正常流程如下：

1. Agent 静默扫描项目、README、依赖、配置、路由、页面与源码。
2. 它会告诉你识别到的项目类型、技术和主要功能，并为功能建立代码证据。
3. 只有在调查后仍无法确定时，才会集中请你确认软件名称建议、申请主体、开发方式、真实日期和是否已公开使用等事实。
4. 确认后锁定软件事实，生成说明书、源程序鉴别材料、申请信息填写指引、功能证据清单和质量报告。
5. 源程序会从第一方核心代码中选择连续材料、进行脱敏、分页，并可输出 HTML、DOCX、PDF。
6. 独立审核八道质量门：事实、证据、一致性、源程序、说明书、隐私、幻觉与提交前检查；有问题会先自动修正，再请你处理无法自行解决的事实问题。

任务可以中断。输出目录保存 `software-profile.yaml`、`evidence-map.json`、`workflow-state.json` 与 `user-confirmations.json`；下次说“继续”时会检查项目是否变化并从上次阶段恢复。

## Official Demo

[FlowTask Official Demo](examples/flowtask-demo/) 使用一套真实可运行的 Vue 3 + TypeScript + Vite 与 FastAPI + SQLite 项目，完整记录 Copyright Forge 的实际运行结果。模拟用户只说：

> 帮我给这个项目做一个软著。

项目依次经过 Project Scan、Evidence Map、Feature Graph、用户事实确认、Fact Lock、材料生成与 Independent Review，最终产出 `READY` 的公开测试材料。浏览 [HTML Demo](https://rodert.github.io/copyright-forge-skill/demo/flowtask/) 可查看功能证据、事实锁定、说明书、源程序分页预览和八道质量门；所有身份和日期均明确为公开测试数据。

## 可靠性边界

- 只基于真实项目和用户确认的事实；没有代码证据的功能不得写入正式材料。
- 原项目只读，所有结果写到项目外的独立输出目录。
- 不提交登记申请，不生成或改写官方申请表，不承诺申请一定通过。
- 当前默认支持普通交存。合作、委托、受让、继承、修改他人软件、例外交存等情形会继续完成可由项目完成的部分，并明确标记合同、权属或提交环节需要人工复核的内容。
- 每天首次使用会尽力检查上游更新；网络不可用、非 Git 安装或本地改动不会阻断材料工作，也绝不覆盖本地改动。
- 规则库保存来源、法律属性、适用范围和核验日期。规则雷达只生成待人工审核的变化报告，绝不会自动篡改规则。

## 技术说明

核心入口是薄路由器 [skills/copyright-forge/SKILL.md](skills/copyright-forge/SKILL.md)，创建、诊断、续办、补正和规则核验均使用独立流程模块。辅助脚本适用于 Python 3.10+；PDF 渲染需要 Agent 运行环境提供 `reportlab`。详细架构见 [docs/architecture.md](docs/architecture.md)，支持范围见 [docs/supported-projects.md](docs/supported-projects.md)。

Apache-2.0，详见 [LICENSE](LICENSE)。
