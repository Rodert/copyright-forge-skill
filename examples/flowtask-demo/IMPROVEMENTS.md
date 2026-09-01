# Demo 制作中发现的改进项

## 已在 Demo 中修复：源程序审核误报

首次审核将源程序中的 `password=ref("")` 变量误判为敏感信息，也将分页 JSON 元数据作为材料正文做身份一致性检查。该问题已在 Reviewer 修复：敏感字段必须包含非空长值，JSON/YAML 仅作为审计数据，源程序材料只要求软件名称和版本一致。

## 功能声明与证据 ID 的自动绑定

当前 `software-profile.yaml` 的 `features` 字段只接受 Evidence Map 的候选文件 ID，而 Feature Graph 使用独立的 `F001` 类 ID。说明书内容由 Agent 根据真实路由、页面与服务生成，但 Reviewer 尚不能逐段将中文功能名称自动绑定到 Feature Graph 节点。

建议：建立一个可验证的 `material-claims.json`，每段说明书以 `feature_id` 显式引用 Feature Graph。Reviewer 应校验每个声明的 ID、证据分数和文档资格，而不是只做名称匹配。

## 源程序材料交付

当前 Source Builder 会生成连续代码文本、HTML、DOCX 和可选 PDF 渲染入口。当前运行环境没有 `reportlab`，因此本 Demo 保留了真实 HTML 与分页计划，不伪造 PDF。建议为 Skill 发行环境声明可选 PDF 依赖并加入渲染后的视觉回归测试。

## 项目适配器

通用扫描器已经识别 Vue 和 FastAPI 源文件，但 Feature Graph 的语义归并仍依赖文件命名。建议逐步为 FastAPI、Vue Router、SQLAlchemy 等加入适配器，使 API、页面、服务和数据库实体可形成更精确的功能图。
