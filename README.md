# RoboIDF-Ecosystem

2026-11-01：离线适配、显式插件注册和兼容性工具开发版。**v0.2 未发布；没有已验收的真机适配或数字孪生。**

```bash
pixi install --locked
pixi run --locked test
pixi run --locked demo-all
```

Linux x86_64 / Python 3.12，Pixi 锁定 Core Git 提交，单独克隆即可运行。报告保存在 `artifacts/`。

| 命令 | 功能 |
|---|---|
| `pixi run demo` | CSV 合成日志转换为 Core Dataset，拟合并独立回放 |
| `pixi run registry-demo` | 显式插件注册与兼容性检查，展示有效离线示例及拒绝路径 |
| `pixi run website` | 本地社区网站预览 http://127.0.0.1:8765 |

参见 [CSV入门](docs/m0.md)、[插件注册与验证](docs/registry.md)、[贡献指南](CONTRIBUTING.md)。不从清单动态导入或执行任意代码；未知单位、SDK、标定和资产来源不得自动补全。离线示例不授予 L2/L3 等级。Wuji Hand 2 与 Tianji Arm 均待设备和 SDK 接入。

[社区门户](https://roboidf-community.agile-auk-4941.chatgpt.site) · [Core](https://github.com/RoboIDF/RoboIDF) · [Bench](https://github.com/RoboIDF/RoboIDF-Bench)。门户提供文档、实际进度和 GitHub 协作入口，不提供站内账户或文件上传。

网站源码位于 `website/dist/`，部署流程见 [网站维护](website/README.md)。项目许可证待确定。[旧说明](docs/pre-m0-status.md)仅作历史参考。论文工作已停止。
