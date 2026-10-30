# 跨设备开发接续说明（给 ChatGPT Work / Codex）

## 已知背景

- 用户目前不在 Windows 电脑旁边；桌面 Remote 无法连接。
- 用户电脑有一个处于 **M0** 阶段的 Android「未言」工程，但文件及技术栈**尚未提供**。不要假设这个网页原型已经与 M0 合并。
- 本包只有 **M1.01 独立 HTML 原型**，位置 `prototypes/mobile-m1/index.html`。
- 产品是私人日记，必须严格区分**产品源代码**与**私人日记数据**。

## 目标

在 GitHub 建立 **私人（private）** 的 `weiyan` 仓库，存入本包作为原型与产品规范。连接 Work 与 GitHub，形成手机发起任务、PC 拉取代码的工作流。

## 推荐执行顺序

1. 核实用户 GitHub 登录身份和可管理的仓库；如要创建新 `weiyan` 仓库，确保可见性 `private`，并请用户确认最终仓库名称与授权。绝不要发布到不相关的公开仓库。
2. 检查所有待提交文件，排除 API Key、密钥、用户日记、个人照片、备份 JSON、缓存和构建产物。
3. 将 README、`.gitignore`、`docs/`、`prototypes/mobile-m1/index.html` 提交到私有仓库，记录具体 commit SHA，并回读确认文件存在。
4. 生成适当的 Git 流程：主分支保护（如果权限允许）、开发分支、PR 审查与可回退提交。
5. 指导 Windows 端 `git clone` / `git pull`。等拿到 M0 原工程，先备份，在独立分支上导入，而不是直接覆盖、强制推送或混淆 HTML 与 Android 结构。
6. 新功能小步开发、每步验收。未经用户确认不发布任何线上可访问的日记服务。

## 验收

- 新仓库为 **private**；源代码可从 GitHub 仓库查看。
- README 明确标注网页原型 ≠ Android M0。
- 能从另一个设备下载/拉取相同代码版本。
- GitHub 上没有私人日记、图片或 API 密钥。
- 说明手机和电脑怎么处理同步冲突、回滚与备份。
