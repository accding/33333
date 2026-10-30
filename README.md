# 未言 WEIYAN

> 有些念头，不必急着说出口。

私人表达、可授权的 AI 共鸣、跨时间的自我观察。项目的产品理念保持开放，表达自由、隐私与记忆控制权是明确边界。

## 当前交付物

这是 **M1.01 手机独立原型**，**不是 Windows 电脑上尚未获取的 Android M0 原工程**。请不要将这个静态网页原型视为 Android APK，或覆盖/替换已有 Android 工程。

- `prototypes/mobile-m1/index.html`: 单文件离线 HTML/CSS/JavaScript 原型，面向手机浏览器。
- `docs/PRODUCT_PRINCIPLES.md`: 产品设计共识与边界。
- `docs/DEVELOPMENT_HANDOFF.md`: 给 Work/Codex 的仓库接续与 M0 合并说明。
- `docs/TEST_CHECKLIST.md`: 手动验收用例。

## 已实现（网页原型）

- 无界写作画布与简洁的历史文字流
- 本地文字输入、自动保存及重新打开恢复（依赖浏览器存储）
- 独白/共鸣状态的界面选择，**未接入任何真实 AI 服务**
- 共鸣态选中文字的眉批占位体验
- 图像插入（受原型限制）、两篇真实记录的平行回声对照
- JSON 导入/导出、单篇删除及全部数据清理

## 尚未实现

- Android 原生工程、APK 安装包、与 Windows M0 工程的代码合并
- AI API 接入、长程记忆或服务器同步
- 本地记录加密、安全备份与跨设备日记数据同步
- 自动化构建/单元测试/完整无障碍测试

## 隐私提示

原型不包含外部 CDN、SDK、API Key 或 AI 网络请求；但浏览器 IndexedDB/localStorage **未经加密**。勿使用它长期保存敏感日记；正式版本应具备安全存储、导出/恢复和删除机制。不要上传真实用户日记、私人照片、模型凭据或其他秘密到 GitHub。

## 运行

在手机浏览器打开 `prototypes/mobile-m1/index.html` 即可试用（不同 Android 浏览器对 `file://` 下存储的支持可能不同）。初次体验建议使用不敏感的测试记录。记得导出 JSON 备份。

## 代码同步约定

1. 私有 GitHub 仓库作为**源代码**共享中心；本地真实日记数据不同步到 GitHub。
2. 手机端通过 ChatGPT Work / 云端开发工具修改仓库并提交 PR；Windows 端拉取经审查的提交。
3. Windows Android M0 工程尚未获取；回到电脑后先备份，再导入 `android/` 目录或独立分支，做架构检查，不得直接覆盖。
4. **Git 同步不等于云端自动保存，也不等于不同设备间的日记数据同步。**

## 协同开发启动（2026-10-30）

原始 7 个文件保留在首次提交中；本次不修改 `prototypes/mobile-m1/index.html`。新增仓库安全检查、CI、PR 模板和协同文档，后续修改在任务分支经 PR 进行。

- [项目状态与验证结果](docs/PROJECT_STATUS.md)
- [安全检查及已知风险](docs/SECURITY_REVIEW.md)
- [手机与 Windows 的具体命令和冲突处理](docs/COLLABORATION.md)
- [Android M0 备份、独立导入和合并方案](docs/ANDROID_M0_IMPORT.md)
- [原始文件 SHA256 清单](docs/SOURCE_INVENTORY.json)

**当前阻塞问题：已保存的无图记录被全部擦空后，刷新可能恢复旧正文。** 已用合成数据复现；正式使用前需单独修复并验证。加密、可靠持久化、数据同步和 Android 构建均未完成。

提交前先人工检查具体文件，再运行：

```sh
python tools/check_repository.py
git diff --cached --check
git diff --cached
```

检查器读取 Git 索引，需在添加审核后的文件后运行。不要将真实日记、照片或备份放在项目中；私人仓库也不用于存储个人日记。
