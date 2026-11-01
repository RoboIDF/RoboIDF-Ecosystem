# M0 之前的历史说明

以下状态仅代表 M0 实现前，请以仓库 README 为准。

# RoboIDF-Ecosystem

更新日期：2026-11-01。状态：社区扩展规划与 Pixi 基础环境；暂无已实现适配器或已验证资产。

[项目群总览](https://github.com/RoboIDF/RoboIDF/blob/main/docs/overview.md) · [主项目](https://github.com/RoboIDF/RoboIDF) · [评测项目](https://github.com/RoboIDF/RoboIDF-Bench)

## 定位与边界

遵循 Core Maintained, Community Extended 模式，让设备拥有者在不修改 RoboIDF Core 的情况下
贡献硬件适配、机器人描述、辨识 Profile、数据与模型。
核心团队维护通用合同；硬件拥有者维护具体设备实现和实测证据。
这里不复制 Harness 编排器，也不另行定义一套 Benchmark。

## 扩展类型

| 类型 | 内容 | 所需证据方向 |
|---|---|---|
| Hardware Adapter | 能力发现、反馈、诊断、受控实验接入与停止 | 型号/固件/SDK、反馈语义、时钟、控制模式及故障行为 |
| Robot Description | URDF/MJCF/USD、关节、传动、装配与资产 | 来源、版本、许可、坐标系、已知/未知标定 |
| Identification Profile | 执行器、时延、摩擦、负载、外参等 | 传感器条件、可辨识范围、实验约束和验证方法 |
| Dataset | 命令、状态、时间对齐及实验元数据 | 数据合同、授权、划分、版本/哈希和复现入口 |
| Validated Model | 参数补丁、模型和报告 | 基线来源、后端版本、控制模式、独立验证及适用范围 |
| Backend / Agent Skills | 新辨识器、实验设计与诊断扩展 | 版本化接口、依赖许可与回归证据 |

## 分级接入

| 等级 | 含义 | 不能据此声称 |
|---|---|---|
| L0 Description | 描述和装配可加载 | 已支持真机或已辨识 |
| L1 Offline | 支持标准离线数据与 Mock 辨识 | 已完成真机实验 |
| L2 Hardware | 通过声明范围内的真机实验协议 | 已达到数字孪生质量 |
| L3 Validated Twin | 有通过独立验证的模型及报告 | 对所有控制模式和工作区均有效 |

等级必须附设备版本、适用条件和验证证据；尚未验收的贡献标记 pending，不自动授予 L0。
MJCF 与 USD 的验证状态分别记录，不能用一个引擎的成功替代另一个。

## 贡献流程规划

1. 声明设备、维护者、目标等级、资产来源与许可。
2. 按 Core 合同提供组件描述、能力说明、关节与反馈映射；不支持项明确标注。
3. 接入标准离线数据与 Mock 验证，再按需要开展独立批准的真机验证。
4. 运行 Bench 对应套件，提交报告、复现配置和依赖版本。
5. 审核后登记支持矩阵；上游 SDK、固件或资产更新后重新验证受影响范围。

保持原始模型只读并用可追溯参数补丁产生候选模型。大数据和受限 Mesh/SDK 以授权来源引用，
不把“公开下载”当作可重新分发的许可。

## 首批参考适配

Wuji Hand 2 → Tianji Arm → 固定桌面双臂与灵巧手装配。
均为计划，尚无兼容性结论。社区后续可扩展夹爪、其他机械臂、轮式平台、躯干和人形系统；
组件接入不等于支持该系统所有参数辨识。

## 环境与操作

本仓库独立维护 `pixi.toml` 和 `pixi.lock`，无需父目录或其他项目即可安装。
当前仅配置 linux-64 / Python 3.12；尚未安装或验证机器人 SDK 与辨识后端。

```bash
pixi install --locked
pixi run --locked info
pixi run --locked python --version
```

在本仓库执行以上命令。通过 `pixi add <package>` 或 `pixi add --pypi <package>`
添加依赖，清单与锁文件一起提交；不提交 `.pixi/`。`info` 只展示本文，不执行辨识。

## 当前进展与下一步

- 已建立：扩展类型、L0–L3 规则、贡献路径、环境配置和项目文档。
- 已验证（2026-11-01）（迁移前记录）：工作区环境安装成功；`info` 与本文一致；锁定环境运行 Python 3.12.16，解释器位于工作区对应环境。
- 待实现：与 Core 共同定义最小 Adapter/资产元数据合同，然后形成首个模板与 Bench 验收入口。
- 待确认：参考设备具体版本、分发许可与支持矩阵字段。
- 验证边界：本轮只检查环境及文档入口，不代表任何设备已经适配。
- 增加组件时更新本文支持情况；合同、等级、公共依赖或里程碑变化同步根 README。

## 仓库与发布范围

仓库：https://github.com/RoboIDF/RoboIDF-Ecosystem 。首次提交仅包含规划文档、维护约定与 Pixi 配置。
当前未选择项目许可证；公开可见不代表已授予开源再分发许可。

2026-11-01 独立仓库验证：`pixi install` 成功，`pixi run --locked info` 与 README 一致；Python 解释器位于本仓库 `.pixi/envs/default`，仓库内文档链接检查通过。

## 社区网站（2026-11-01）

首版门户包含项目与论文入口、可筛选适配路线图、L0–L3 证据等级及 GitHub 贡献入口。
源码在 `website/dist/`；贡献指南见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
`pixi run website` 启动本地预览。本站没有站内账号、发帖或上传服务，协作由 GitHub 承担。
浏览器检查已确认机械臂筛选只显示一个对应方向；JavaScript 语法检查通过。
网站目录表示规划，不代表已有经过验收的适配器。

公开网站：https://roboidf-community.agile-auk-4941.chatgpt.site （Sites v1，2026-11-01 发布成功）。
