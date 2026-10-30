# 项目状态报告

更新：2026-10-30。阶段：跨设备协同开发基线；M1.01 网页原型已检查；Android M0 等待 Windows 工程。

## 交付范围

- 完整审阅准备包内 7 个文件；首次提交保留上传内容，后续补充文档和工具，不修改 HTML 原型。
- 建立 main + 任务分支 + PR 的协同流程，提供 Windows 命令、冲突处理和 revert 回退方法。
- 增加敏感路径/凭据/用户数据检查、只读 CI、PR 模板、项目开发约定和原始文件 SHA256 清单。
- 制定 M0 完整本地备份、技术栈盘点、干净 worktree、审核后复制到 android/、独立 PR 导入和逐项合并方案。尚未执行导入。
- GitHub 建立与远程验证结果见本文末尾；未启用公开 Pages。

## 现有代码分析

单一 HTML/CSS/JavaScript 文件，无构建依赖；IIFE 管理内存 state，IndexedDB notes 对象仓库持久化，初始化失败时回退 localStorage，再失败则只存内存。新记录默认独白，输入后 500ms 防抖保存。

界面包含写作、历史文字流、本地搜索、照片压缩（最长边 1350，JPEG 质量 .76，每篇最多 4 张）、独白/共鸣占位切换、本地选段眉批、手动两篇平行回声、JSON 导入导出、演示记录、单篇删除与全部清除。历史输出使用转义或 textContent；没有真实 AI、服务器、账户或网络同步。

JSON 备份格式为 `WEIYAN_LOCAL_BACKUP`，版本 1；导入上限 35MiB，按 id 跳过重复，不处理同 id 新版本。它是手动数据备份方式，不是跨设备自动合并方案。

## 实际验证

环境：云端 Linux Chromium，393×852 手机视口，通过仅绑定 127.0.0.1 的临时 HTTP 服务打开原型；全新临时浏览器上下文，数据均为 `WEIYAN_SYNTHETIC_TEST_*`。不代表 Android 真机通过。

| 场景 | 结果 |
| --- | --- |
| 默认独白、眉批入口隐藏 | 通过 |
| 输入保存、刷新恢复 | 通过 |
| 共鸣选段本机占位、切回独白关闭折页 | 通过 |
| 两条记录平行回声 | 通过 |
| 导出两条、清空、导入恢复、重复导入跳过 | 通过 |
| 单篇删除、清空后刷新为空 | 通过（正常持久化场景） |
| 已保存正文全部擦空后刷新 | **失败：旧正文恢复** |
| 上述测试期间外部网络请求 / 页面 JavaScript 错误 | 0 / 0 |

静态扫描未发现凭据、真实日记文件、私人照片或图片载荷。完整风险和后续验证见 SECURITY_REVIEW.md。代码语法、Git 差异与索引安全检查在推送前运行。

未验证：Android file:// 存储、Windows/Android 真机、压图与照片恢复、存储限额/故障、快速切换与删除竞争、多标签页、后台进程终止、无障碍。测试清单中的照片等项目仍待执行，不将原清单整体标为通过。当前云浏览器不允许 file:// 导航，因此使用本机临时 HTTP；这不是部署服务。

## 下一阶段

1. 单独 PR 修复擦空正文后的持久化语义，并验证删除/撤销/刷新；明确空页是否保留，保障用户实际删除内容的权利。
2. 串行化保存/切换/删除，处理存储失败、多标签页与恢复；完善导入版本、冲突和图片校验。
3. Windows 可用后执行 M0 只读盘点和备份，再导入独立分支。未拿到文件前不预设 Android 架构。
4. Android 正式版建立加密与数据控制；AI 接入在授权边界可测试后另行设计。

## 远程交付记录

- 已确认 GitHub 登录身份 `accding`，并可访问此前授权的仓库；未改动公开仓库 `33333`。
- 目标地址为 `https://github.com/accding/weiyan`，**目前尚未创建或验证存在，不能作为已交付仓库链接**。
- `gh repo create --private` 返回 `Resource not accessible by integration (createRepository)`；官方 REST `POST /user/repos` 同样返回 HTTP 403。现有集成凭据没有创建仓库权限。
- 用户需在 GitHub 安全页面创建名为 weiyan 的私人空仓库（不初始化 README/License/.gitignore），并确保当前 GitHub App 可访问新仓库；无需向聊天提供 Token。
- 已完成本地 Git 提交；尚未推送、运行远程 Actions、创建 PR 或配置服务器分支保护。不能声称已经实现跨设备远程同步。
- 基线提交：`bea4fc0`（上传的 7 个原始文件）。流程与安全工具提交：`5d64342`。完整 SHA 通过 `git log` 获取，后续状态说明另有提交。
- 本地索引安全检查 17 个文件零发现，原型 JavaScript 语法检查与 Git 差异检查通过；合成凭据、私人数据路径和符号链接被检查器阻止。

### 最新目标调整

用户随后选择复用现有 `accding/33333`（五个 3），不再依赖创建 weiyan 新仓库。原始交接文档禁止使用公开 33333 的要求，按用户最新意图调整为：仅在其改为 private 后使用；项目隐私要求保持有效。

已回读确认 `accding/33333` 为空仓库且 visibility 为 PUBLIC。尝试官方 REST 更新 `private=true` 时返回 HTTP 403 `Resource not accessible by integration`，回读仍为 public。因此没有上传任何项目内容，也没有覆盖文件。需用户在 GitHub 仓库 Settings → General → Danger Zone → Change repository visibility 中改为 Private；完成后工具重新核验再正常推送。

## 权限补齐后的接续步骤

先回读 `accding/33333` 的 owner/name、`private=true`、visibility 为 private；检查默认分支和所有 refs，确认没有用户后来加入的内容。不匹配就停止，不自动覆盖已有文件。

对确认的私人空仓库添加 origin，使用普通 `git push -u origin main`，不 force。若仓库出现新提交，先 fetch 比对并在独立分支处理，避免覆盖。推送后重新读取完整 main SHA、文件树、HTML blob 哈希及仓库 private 状态；等待 CI 结果，再按账户能力尝试主分支保护，并如实记录启用结果。

这一步由开发工具在授权可用后执行；不需要用户把代码逐份复制到 GitHub。
