# Copyright Forge Skill

Copyright Forge Skill 是一款面向中国软件著作权登记申请的 AI Agent Skill。
它基于真实软件项目，协助准备软件说明书、源程序鉴别材料、申请信息填报稿及
相关校验报告。

它会分析项目、为功能描述保留代码证据、建立统一的软件信息档案，并在交付前检查
材料一致性和潜在敏感信息。

本项目不会提交申请、伪造或修改官方申请表、修改原始项目、虚构软件功能或权利事实，
也不保证登记申请一定通过。

## 已包含能力

- 支持 Go、Java、Python、Node.js、Vue、React 项目的结构与技术栈扫描。
- 以证据为先的功能映射，避免说明书出现无代码依据的功能。
- 以 `software-profile.yaml` 作为所有材料唯一的软件名称、版本和事实来源。
- 面向普通交存的确定性源程序选择清单。
- 仅对生成副本进行敏感信息检测与脱敏，不改动原始代码。
- 软件信息、材料一致性和最终输出的校验报告。

## 目录

可分发的 Skill 位于 [skills/copyright-forge](skills/copyright-forge)，入口是
[SKILL.md](skills/copyright-forge/SKILL.md)。规则、模板、Schema 和辅助脚本均在
该目录内。

## 快速开始

辅助脚本要求 Python 3.10+，仅使用标准库，且不会修改待分析的项目。请将输出目录
放在项目目录之外：

```bash
SKILL=skills/copyright-forge
OUT=/tmp/copyright-forge-output

python3 "$SKILL/scripts/scan_project.py" /path/to/project --output "$OUT/project-scan.json"
python3 "$SKILL/scripts/build_evidence_map.py" /path/to/project --output "$OUT/evidence-map.json"
python3 "$SKILL/scripts/collect_source.py" /path/to/project --output "$OUT/source-manifest.json"
```

将软件信息模板复制到输出目录后，确认著作权人、开发方式、完成日期、发表状态等
只能由申请人确认的字段，再运行 `validate_profile.py`。生成的 JSON 是审核材料，
不是已完成的登记申请。

## 适用范围

第一版支持普通交存流程。例外交存、合作开发、委托开发、继承或受让、修改他人软件
等情形会被标记为需要人工复核，不会强行自动化处理。

规则仅用于材料准备和校验。提交前请通过适用的官方登记渠道确认当前要求和申请事实。

## English

Copyright Forge Skill prepares evidence-backed draft materials for Chinese
software copyright registration from real projects. It supports project
analysis, a canonical software profile, source-manifest generation, redaction,
and validation. It does not submit applications, determine ownership, alter
official forms, modify source projects, or guarantee approval.

## 开源许可

Apache-2.0，详见 [LICENSE](LICENSE)。
