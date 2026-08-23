# Copyright Forge Skill

> 基于真实项目，为中国软件著作权登记准备可核验的材料初稿。

Copyright Forge Skill 是一款面向中国软件著作权登记申请的 AI Agent Skill。它从
真实项目代码中提取证据，协助准备软件说明书、源程序鉴别材料、申请信息填报稿和
校验报告。

```text
真实项目
  -> 项目扫描
  -> 功能证据映射
  -> 统一软件信息档案
  -> 说明书 / 源程序材料 / 填报信息
  -> 一致性与安全校验
```

## 能做什么

- 扫描 Go、Java、Python、Node.js、Vue、React 项目的技术栈与源文件。
- 建立功能与代码路径的证据映射，减少无依据的功能描述。
- 使用 `software-profile.yaml` 统一软件名称、版本和申请事实，避免材料间不一致。
- 生成面向普通交存的确定性源程序选择清单。
- 检测潜在密钥并只在生成副本中脱敏，原始项目保持不变。
- 输出软件信息、材料一致性和最终状态校验报告。

## 不做什么

- 不提交登记申请，也不生成、伪造或修改官方申请表。
- 不虚构功能、源代码、截图、著作权归属、开发关系或发表事实。
- 不将 Git 时间或 AI 推断当作申请事实；这些内容必须由申请人确认。
- 不修改待分析项目，不承诺登记申请一定通过。

## 工作方式

1. **扫描项目**：识别项目结构、语言、框架和候选源文件。
2. **建立证据**：为候选功能记录对应的源代码、路由、模型或页面路径。
3. **确认软件信息**：由申请人确认著作权人、开发方式、完成日期、发表状态等事实。
4. **生成并校验**：根据统一档案准备材料初稿，检查名称、版本、证据与敏感信息。

## 快速开始

要求：Python 3.10+。所有脚本只使用标准库；建议将输出目录放在待分析项目之外。

1. 扫描项目并生成基础材料：

   ```bash
   SKILL=skills/copyright-forge
   OUT=/tmp/copyright-forge-output

   mkdir -p "$OUT"
   python3 "$SKILL/scripts/scan_project.py" /path/to/project --output "$OUT/project-scan.json"
   python3 "$SKILL/scripts/build_evidence_map.py" /path/to/project --output "$OUT/evidence-map.json"
   python3 "$SKILL/scripts/collect_source.py" /path/to/project --output "$OUT/source-manifest.json"
   ```

2. 将 [软件信息模板](skills/copyright-forge/assets/templates/software-profile.yaml)复制到
   输出目录，填写并确认申请人专属事实。

3. 校验软件信息：

   ```bash
   python3 "$SKILL/scripts/validate_profile.py" "$OUT/software-profile.yaml" \
     --output "$OUT/profile-validation.json"
   ```

4. 使用 [SKILL.md](skills/copyright-forge/SKILL.md) 指引 Agent 生成材料；提交前按官方
   渠道的最新要求复核。

## 项目结构

```text
skills/copyright-forge/
  SKILL.md            Skill 入口与工作流
  references/         规则、边界与材料要求
  assets/templates/   软件信息和文档模板
  assets/schemas/     JSON Schema
  scripts/            扫描、证据、源程序、脱敏与校验脚本
```

完整架构说明见 [docs/architecture.md](docs/architecture.md)，支持范围见
[docs/supported-projects.md](docs/supported-projects.md)。

## 适用范围

第一版支持普通交存流程。例外交存、合作开发、委托开发、继承或受让、修改他人软件
等情形会被标记为需要人工复核，不会强行自动化处理。

规则仅用于材料准备和校验。提交前请通过适用的官方登记渠道确认当前要求和申请事实。

## English

Copyright Forge Skill prepares evidence-backed draft materials for Chinese
software copyright registration from real projects. It analyzes projects, maps
features to evidence, uses one canonical software profile, and validates source
materials and likely secrets. It does not submit applications, determine legal
facts, alter official forms, modify source projects, or guarantee approval.

## 开源许可

Apache-2.0，详见 [LICENSE](LICENSE)。
