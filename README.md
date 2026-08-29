# Copyright Forge Skill

> 为中国软件著作权登记准备基于真实项目证据的材料初稿。

[简体中文](README.md) | [English](docs/README.en.md) | [日本語](docs/README.ja.md) | [한국어](docs/README.ko.md) | [Русский](docs/README.ru.md) | [Français](docs/README.fr.md)

Copyright Forge 是一款面向中国软件著作权登记申请的 AI Agent Skill。它从真实项目中
提取可追溯证据，统一软件信息，并协助准备说明书、源程序鉴别材料与申请信息填报稿。
它的目标不是“代写一套看似完整的材料”，而是让每项内容都能回到项目代码或申请人确认
的事实。

项目站点：[rodert.github.io/copyright-forge-skill](https://rodert.github.io/copyright-forge-skill/)

## 直接交给 Agent

复制以下内容，发送给你的 AI Agent：

```text
请从 https://github.com/Rodert/copyright-forge-skill 安装并使用 Copyright Forge Skill。

安装后，请读取 skills/copyright-forge/SKILL.md，并按其中的流程为我的真实软件项目准备中国软件著作权登记材料初稿。

开始准备材料前：每天首次使用时检查该 Skill 的上游 Git 更新；若发现更新且本地工作区干净，先以 fast-forward 方式更新再继续。无更新时无需提示；更新检查失败或本地改动阻塞更新时，说明原因并停止本次材料准备，绝不覆盖本地改动。

仅基于真实项目与我确认的事实工作：不得虚构功能、源代码、截图、著作权归属、开发关系、发表事实或日期；不得修改原始项目；不得伪造官方申请表或承诺登记结果。将所有输出写入项目目录外的独立输出目录，并明确标记需要我确认的字段。
```

## 安装

以下命令为**首次全局安装**。它们保留仓库的 Git 检出，并将 Skill 链接到对应工具的
全局目录，以便 Copyright Forge 在每天首次使用时检查并获取更新。若目标目录已存在，
请先处理已有安装，避免覆盖本地修改。

### Claude Code

> 若你所说的 “Cloud Code” 指的是 Claude Code，请使用本节。Claude Code 的个人
> Skill 目录为 `~/.claude/skills/`。

```bash
CF_SKILL_HOME="$HOME/.claude"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新打开 Claude Code 后，可输入 `/copyright-forge`，或直接提出“准备软件著作权登记
材料”的请求。Claude Code 会在个人目录中发现该 Skill。

### Codex

Codex 会从 `$CODEX_HOME/skills/` 发现全局 Skill；未设置 `CODEX_HOME` 时默认使用
`~/.codex/skills/`。

```bash
CF_SKILL_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新开始一个 Codex 会话后，直接说明要准备中国软件著作权登记材料，或显式调用
`$copyright-forge`。

### OpenCode

OpenCode 的全局 Skill 目录为 `~/.config/opencode/skills/`。

```bash
CF_SKILL_HOME="$HOME/.config/opencode"
mkdir -p "$CF_SKILL_HOME"
git clone --depth 1 https://github.com/Rodert/copyright-forge-skill.git "$CF_SKILL_HOME/copyright-forge-repo"
mkdir -p "$CF_SKILL_HOME/skills"
ln -s ../copyright-forge-repo/skills/copyright-forge "$CF_SKILL_HOME/skills/copyright-forge"
```

重新打开 OpenCode 后，直接描述软著材料准备任务，或使用 OpenCode 的 Skill 调用方式加载
`copyright-forge`。

安装目录均是符号链接的目标之外的 Git 检出，因此请不要把 `copyright-forge-repo` 当作
临时目录删除。各工具的目录约定请参阅 [Claude Code Skills](https://code.claude.com/docs/en/skills)、
[Codex Skills](https://developers.openai.com/codex/skills/) 和
[OpenCode Skills](https://opencode.ai/docs/skills/) 的官方文档。

## 核心能力

| 能力 | 说明 |
| --- | --- |
| 项目理解 | 扫描 Go、Java、Python、Node.js、Vue、React 项目的结构、技术栈与源文件。 |
| 证据映射 | 将候选功能关联到源代码、路由、模型或页面路径，避免无依据的功能描述。 |
| 统一事实源 | 通过 `software-profile.yaml` 统一软件名称、版本与申请事实，防止材料之间不一致。 |
| 源程序准备 | 为普通交存生成确定性的源程序选择清单，供人工复核和后续排版。 |
| 安全处理 | 检测潜在密钥与敏感内容，只在生成副本中脱敏，绝不改写原项目。 |
| 交付校验 | 校验软件信息、材料一致性与最终状态，区分阻塞项、警告和待确认事项。 |

## 工作流

```text
真实项目
  -> 项目扫描
  -> 功能证据映射
  -> 软件信息确认
  -> 说明书 / 源程序材料 / 填报信息
  -> 一致性与安全校验
```

1. **扫描与取证**：识别项目结构、技术栈和可佐证功能的代码路径。
2. **确认软件信息**：由申请人确认著作权人、开发方式、完成日期、发表状态等法律事实。
3. **准备材料初稿**：所有软件名称和版本均读取同一份 `software-profile.yaml`。
4. **执行校验**：确认功能有证据、材料身份一致，并复查生成副本中的敏感信息。

## 使用方式

Skill 入口位于 [skills/copyright-forge/SKILL.md](skills/copyright-forge/SKILL.md)。辅助脚本
需要 Python 3.10+，仅使用标准库，且不会修改待分析项目。建议将输出目录放在项目之外：

```bash
SKILL=skills/copyright-forge
OUT=/tmp/copyright-forge-output

mkdir -p "$OUT"
python3 "$SKILL/scripts/scan_project.py" /path/to/project --output "$OUT/project-scan.json"
python3 "$SKILL/scripts/build_evidence_map.py" /path/to/project --output "$OUT/evidence-map.json"
python3 "$SKILL/scripts/collect_source.py" /path/to/project --output "$OUT/source-manifest.json"
```

随后复制 [软件信息模板](skills/copyright-forge/assets/templates/software-profile.yaml) 到输出
目录，补充并确认申请人专属事实，再执行：

```bash
python3 "$SKILL/scripts/validate_profile.py" "$OUT/software-profile.yaml" \
  --output "$OUT/profile-validation.json"
```

## 可信边界

- 不提交登记申请，不生成、伪造或改写官方申请表。
- 不虚构功能、源代码、截图、著作权归属、开发关系、发表事实或日期。
- 不将 Git 时间或 AI 推断作为已确认的申请事实。
- 不修改待分析项目，不覆盖本地改动，不承诺登记申请一定通过。

当前版本支持**普通交存**。例外交存、合作开发、委托开发、继承或受让、修改他人软件
等情况会被标记为需要人工复核，而不会被强行自动化处理。提交前请以适用官方渠道的最新
要求为准。

## 项目结构

```text
skills/copyright-forge/
  SKILL.md            Skill 入口与工作流
  references/         规则、边界与材料要求
  assets/templates/   软件信息和文档模板
  assets/schemas/     JSON Schema
  scripts/            扫描、证据、源程序、脱敏与校验脚本
```

完整架构见 [docs/architecture.md](docs/architecture.md)，支持范围见
[docs/supported-projects.md](docs/supported-projects.md)，规则版本见
[docs/rules-versioning.md](docs/rules-versioning.md)。

## 开源许可

Apache-2.0，详见 [LICENSE](LICENSE)。
