# Mobile Widget App Template

这个模板用于快速启动一个支持以下能力的移动端项目：

- 预留接口调用逻辑（后续替换成你的真实 API）
- 支持桌面小组件（通过 `home_widget` 同步数据）
- 使用 GitHub Actions 做自动构建
- 使用测试证书进行签名打包（通过 GitHub Secrets 注入）

## 目录结构

- `.github/workflows/`：CI 打包流程（Android / iOS）
- `mobile_template/`：Flutter 项目模板（含接口和小组件预留）

## 1. 本地初始化

1. 安装 Flutter 与对应平台工具链（Android Studio / Xcode）。
2. 进入模板目录后执行：

```bash
cd mobile_template
flutter pub get
flutter run
```

## 2. 接口配置位置

接口调用预留在：

- `mobile_template/lib/services/api_service.dart`

当前已接入天气接口：

- `GET https://api.suol.cc/v1/tq_tips.php?type=today&msg=青岛&n=1`

你后续可修改：

- `msg` 参数（城市）
- `fetchLatestData()` 内的字段映射（如 weather/audio）
- 鉴权逻辑（如接口后续增加 token/sign）

## 3. 小组件预留位置

小组件同步逻辑预留在：

- `mobile_template/lib/widget/widget_sync_service.dart`

当前流程：

1. 拉取接口数据
2. 写入 Widget 共享数据
3. 请求刷新桌面小组件

## 4. 上传 GitHub 后自动打包

当前配置已支持：你把代码上传到 GitHub 后，推送到 `main/master` 会自动触发打包；也可以手动点 `Run workflow` 触发。

### Android Secrets

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

### iOS Secrets（测试证书）

- `IOS_P12_BASE64`
- `IOS_P12_PASSWORD`
- `IOS_PROVISION_BASE64`
- `IOS_TEAM_ID`
- `IOS_BUNDLE_ID`

工作流文件：

- `.github/workflows/android-test-sign.yml`
- `.github/workflows/ios-test-sign.yml`

### 首次使用步骤

1. 在 GitHub 新建仓库（例如 `weather-widget-app`）。
2. 把当前目录代码推送到 GitHub：

```bash
git init
git add .
git commit -m "init weather widget app"
git branch -M main
git remote add origin <你的仓库地址>
git push -u origin main
```

3. 在仓库 `Settings -> Secrets and variables -> Actions` 中配置上面列出的 Secrets。
4. 进入 `Actions` 页面，运行：
   - `Android Test Signed Build`
   - `iOS Test Signed Build`
5. 打包产物在每次任务的 `Artifacts` 下载。

> 注意：CI 会自动执行 `flutter create . --platforms=android,ios`，所以即使本地未生成原生目录，也可以在云端构建。

## 5. 下一步建议

- 补齐 `android/` 与 `ios/` 原生 Widget 扩展代码（模板中已预留 Flutter 侧逻辑）
- 接入你的真实接口鉴权（Token / Sign）
- 增加错误重试和离线缓存
