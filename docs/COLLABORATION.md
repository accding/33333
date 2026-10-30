# 手机与 Windows 协同开发

远程：`https://github.com/accding/weiyan`，必须保持 private。GitHub 负责源代码和设计文档同步；它不连接 Windows 桌面，不同步实时未提交文件，也不备份或同步个人日记。

## 分支与职责

- `main`：经过验证的共同基线。
- 手机任务：`mobile/<简短任务名>`；电脑任务：`desktop/<简短任务名>`。
- M0 初次导入：`import/android-m0`，只在拿到工程并完成备份、检查后创建。
- 每项任务一个短分支和 PR；提交消息说明行为与原因。小步改动，避免双方同时编辑同一段代码。
- 合并前检查 CI、人工 diff 和隐私清单。个人开发无需邀请其他人访问私人仓库。

## 手机端每次交接

在 Work 中指定仓库、分支、任务范围和验收条件。开发工具有连接权限并不保证新仓库已经被 GitHub App 授权；若列表看不到 weiyan，在 GitHub 应用的仓库访问设置中选中它。

1. 从最新 main 创建任务分支，先阅读项目状态与产品原则。
2. 使用合成数据验证；检查暂存文件，运行安全检查，小步提交并推送。
3. 创建 PR，记录验证结果、未测项、风险和影响目录。无需等 Windows 在线。
4. main 合并后记录提交 SHA，下一台设备用 SHA 核对版本。云工作区未提交的改动不算已同步。

可使用以下任务提示：

> 在 accding/weiyan 的 mobile/任务名 分支完成【范围】。先拉取 main，阅读 AGENTS.md；保留独白与授权边界，用合成数据验证，不上传日记或凭据。不要改写历史、覆盖 M0 或大规模重构。提交 PR，返回 SHA、验证结果和交接说明。

## Windows 第一次连接（PowerShell）

先安装 Git for Windows、GitHub CLI；通过浏览器安全登录，不在聊天、代码或命令参数中粘贴 Token。选择一个全新的空目录，绝不在当前 M0 目录执行 clone 或 init。

```powershell
gh auth login
gh auth setup-git
git clone https://github.com/accding/weiyan.git
Set-Location weiyan
git remote -v
git status
git log -3 --oneline
git config pull.ff only
```

建议使用 GitHub 的 no-reply 邮箱作为此仓库提交邮箱；不要把本机个人配置提交。

## 电脑每次开始与结束

工作区应先保持干净；若有改动，先在自己的分支检查并提交（或暂存到仅本机的 stash），禁止直接 reset/clean 丢弃。

```powershell
git switch main
git pull --ff-only origin main
git switch -c desktop/short-task
# 编辑与适当验证后，只添加本次审核过的具体文件
git add path/to/reviewed-file
python tools/check_repository.py
git diff --cached --check
git diff --cached
git commit -m "说明具体变化"
git push -u origin desktop/short-task
gh pr create --base main --head desktop/short-task
```

命令中的 `path/to/reviewed-file` 与 `short-task` 是需要替换的示例。若 Windows 使用 `py -3`，把 `python` 换为 `py -3`。

## 同步冲突

`git pull --ff-only` 失败时停止，不要 force push。先提交本分支改动，`git fetch origin`，在任务分支运行 `git merge origin/main`。逐段审查冲突；HTML 与 Android 视图可能只是同一设计的不同实现，不能互相覆盖。解决后重新测试、提交并正常 push；不确定时 `git merge --abort`，报告冲突。

## 回滚与备份

共享历史中用 `git revert <commit-SHA>` 产生新提交并提 PR；合并提交如需 `-m 1`，先核对父提交和影响。禁止 reset 后强推、删除历史或通过整目录替换回滚。代码回滚不一定能回退数据库格式，数据迁移必须另有备份与恢复计划。

Android M0 原目录及包含密钥/数据的完整备份应仅保存在用户控制的本地或加密存储中，仓库外留存。Git 仓库只保留审核后的源代码；日记数据未来若做跨设备同步，须作为独立功能重新设计加密、授权、冲突、删除与恢复。

## 主分支保护

目标：main 禁止强推及删除、必须 PR、必须通过 `Repository safety`，启用会话解决要求。是否实际启用以项目状态报告为准。

部分 GitHub 个人套餐不支持私人仓库的分支保护；若服务拒绝，流程约定和 CI 仍然可用，但不能声称具有服务器强制保护。可在账户支持该能力后启用，不得为此把仓库改为公开。
