# Windows Android M0 安全导入方案

当前未获得 M0 源文件、目录结构、技术栈、历史、包名或构建结果；本方案尚未执行。M1.01 不是 APK，也未和 M0 合并。

## 1. 完整备份与只读盘点

回到 Windows，先停止 IDE 构建，完整复制 M0 到仓库外的新备份目录，包含原有 `.git`、未提交文件和必要本地配置。验证文件数量与关键源文件 SHA256；备份可能含密钥和日记，应留在用户控制的加密存储中，禁止上传。已有 Git 历史时可额外用 `git bundle create <仓库外路径>/m0-history.bundle --all` 备份历史；bundle 不包含未提交/忽略文件，不能替代完整备份。

只读记录：原目录 git status、当前分支与 SHA、已有 remote、Gradle/AGP/Kotlin/JDK 版本、Compose 或 XML、模块结构、包名、min/target SDK、Room/其他存储方案、AI/联网代码、构建脚本、测试和数据迁移版本。盘点文档只能含安全的技术信息，不附真实路径、账户、日记或凭据。

## 2. 在干净工作树中导入

clone 本仓库到另一个目录。确认 worktree 干净，从最新 main 建立独立工作树；不要在原 M0 工程内执行这些命令：

```powershell
git switch main
git pull --ff-only origin main
git worktree add ..\weiyan-m0-import -b import/android-m0 main
Set-Location ..\weiyan-m0-import
New-Item -ItemType Directory android
```

仅当 `android/` 尚不存在时创建；发现现有 Android 内容就停止并比对。用资源管理器将审核后的源文件**复制**到 `android/`，保持原 M0 不变。建议目录：

```text
android/
  settings.gradle(.kts)
  build.gradle(.kts)
  gradle.properties          # 先检查是否有密码/本机路径
  gradlew / gradlew.bat
  gradle/wrapper/            # JAR 单独审核来源、哈希
  app/src/                  # 检查 assets、res/raw 中有无真实用户内容
  app/build.gradle(.kts)
```

不要复制 `.git`、`.idea`、`.gradle`、build、local.properties、签名材料、google-services.json、私人图片、导出 JSON、数据库或真实数据。不得运行目录镜像/删除式复制，不移动或删除原工程。不得将完整 M0 ZIP 或 Git bundle 推送作为“备份”。

已有 M0 Git 历史：优先在原处和本地 bundle 中保留；记录安全的原始 SHA。是否将全部历史纳入新仓库应另行审查所有历史中的秘密，并与用户确认。不要直接 `--allow-unrelated-histories` 合并未经审查的历史。

## 3. 导入 PR 与验证

先审查全部文件和构建脚本，再添加明确的源目录；运行 `git status --short`、`git diff --cached --stat`、`git diff --cached` 和安全检查。对被检查器阻止的合法 Wrapper JAR 等内容，先核验供应链来源和 SHA，再单独精确放行；不能使用 blanket 例外绕过数据检查。

Android SDK/JDK/本机路径和签名配置留在本地；凭据使用受保护的本地配置或今后专门设计的 secret 管理，不硬编码。首次只在电脑本地验证，不上传签名密钥到 CI。

在技术栈确认后按项目实际任务运行：

```powershell
Set-Location android
.\gradlew.bat --version
.\gradlew.bat assembleDebug
.\gradlew.bat test
.\gradlew.bat lint
```

任务是否存在以实际 Gradle 工程为准；依赖下载与构建脚本需要联网且会执行代码，先审查。不要提交生成的 APK、测试运行日志或用户数据。验证首次启动、独白离线、保存/删除/恢复、已有本地数据库升级；全部只用合成数据。

提交 `import/android-m0`，PR 附技术栈、导入清单、排除项、原始 SHA、构建结果和未测内容。用户审查确认后再合并 main，禁止强推。

## 4. M1 与 M0 功能合并

先做功能对照表，按独白与授权、本地存储、写作/文字流、备份删除、图像、平行回声逐项评估。HTML 保留在 prototypes 下；Android 保留原架构。每个功能另开 PR，实现 Android 对应交互与验收，不直接把 HTML 覆盖成 Android 文件，也不默认套 WebView。

数据库迁移必须保留向前迁移及失败恢复方案，不用破坏性重建。正式版 AI 接入必须先建立可测试的授权边界；共鸣与记忆授权分开。仅在工程成功导入、构建和设备验收后才能宣布 Android 阶段完成。
