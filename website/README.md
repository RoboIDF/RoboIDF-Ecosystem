# 社区门户

静态 HTML/CSS/JavaScript，文件位于 dist/，无需额外构建或 npm 环境。
从仓库根目录执行 `pixi run website`，访问 http://127.0.0.1:8765 。

通过 Sites 发布；`.openai/hosting.json` 保存站点标识，不含凭据。
后续部署先同步精确源版本、打包 dist 与 hosting manifest，再保存并部署新版本。
GitHub 保存可审查源码；Sites 的源仓库是独立的部署镜像。

功能：项目入口、M0–M5 实际进度、代码与验证文档链接、组件类型筛选、等级说明、贡献指南与 GitHub Issue 提案。
本地检查：node --check website/dist/app.js；浏览器筛选检查通过。
页面包含响应式布局、标签关联、键盘焦点样式及结果状态播报；移动端未单独做设备验证。

当前页面明确标注 v0.2 未发布，M2 真机与 M4 数字孪生待验收。软件演示不升级设备支持等级。
