# M5 离线 CSV 插件登记

`registry.py` 提供显式内存注册表，登记格式为 `registry.v1`，复用 Core `interface.v1` 元数据校验和 `m0.v1` Dataset。当前只绑定本仓库 `adapter.read_csv`，不会执行 manifest 中的代码、模块名、路径或入口点。注册表随进程结束清空；manifest 是数据，不能扩展可执行能力。

## 运行与预期结果

```bash
pixi install --locked
pixi run --locked python registry.py
pixi run --locked python registry.py --manifest examples/registry-offline-v1.json
pixi run --locked python registry.py --hardware
pixi run --locked python -m unittest discover -s tests -p test_registry.py -v
```

前两项退出 0，表示内建离线 CSV 示例登记成功；硬件项退出 1，表示预期拒绝。输出均为严格 JSON。依赖的 Core Git 提交必须包含 `roboidf.validation`，升级后重新执行全部测试。开发期间可以临时设置 `PYTHONPATH` 指向本地 Core，但正式复现应使用仓库固定依赖。

## Manifest 字段

完整文件见 `examples/registry-offline-v1.json`。只接受以下字段，未知字段（包括 entrypoint）拒绝：

| 字段 | 约束 |
| --- | --- |
| schema_version | registry.v1 |
| id | 非空且在本次注册表中唯一 |
| implementation | builtin-csv-v1；唯一预先绑定的实现 |
| level | offline-synthetic；真实硬件和孪生等级一律拒绝 |
| source | uri、license、provenance 均必填，只是来源声明 |
| contract | Core interface.v1；offline / offline-only；offline-csv；单一 prismatic 关节，m、m/s、N |
| evidence | 内建可重现 synthetic-csv-roundtrip，固定 seed=91、samples=8 及 Dataset SHA-256 |

Core 合同字段详情见 Core `docs/validation.md`。当前 CSV 列名固定为 `time_s,velocity_m_s,effort_n`，最后一行 effort 留空，采样必须均匀且严格递增；实际解析复用 `adapter.read_csv`，不另造兼容性不同的 CSV 实现。

## 实际证据与读取示例

注册时用 `MockRobot` 生成固定 8 步、9 个速度样本的合成数据，使用既有 `write_csv` 写临时 CSV，再用既有 `read_csv` 回读，并验证得到 Core Dataset 且数据哈希吻合。登记成功后保存 manifest 深拷贝，调用者修改原对象不会改变登记信息。重复 ID 拒绝。此测试证明的是当前唯一内建适配器的离线回读，不能代表其他插件或真实机器人。

```python
from registry import Registry, example_manifest
registry = Registry()
evidence = registry.register(example_manifest())
data = registry.read('synthetic-csv', 'examples/registry-synthetic-v1.csv',
                     split='validation', seed=91)
assert data.digest() == evidence['evidence']['dataset_sha256']
```

`examples/registry-synthetic-v1.csv` 是实际生成的输入，`registry-evidence-v1.json` 是登记产生的报告；与 manifest 中哈希一致。fixture 来源为 synthetic://roboidf/slider，没有采集设备数据。license 字段仅描述合成测试来源，不代表仓库已确立开源许可证。

`examples/replay-reference-v1.json` 和 `replay-candidate-v1.json` 是确定性三点合成速度，`replay-error-evidence-v1.json` 记录 0.03 m/s 中点偏差导致阈值失败。XML/USDA 示例只做基本结构或文件头检查；对应报告位于 `asset-structure-evidence-v1.json`。这些证据不证明实际物理引擎可加载或动力学一致。

## 失败与权限边界

未知版本、重复 ID、不支持的等级/实现、缺失来源、无证据、合同不兼容及任意可执行入口全部拒绝。登记不下载任何文件、不安装 SDK、不启动设备；`read` 只解析调用者明确指定的本地 CSV。没有注册的 ID 不能读取。

`hardware-pending-v1.json` 明确标记真实硬件待验收；`hardware-refusal-v1.json` 列出缺失 sdk、calibration、approval、stop。即使补齐字符串引用，仍不能执行硬件。所有报告维持 hardware_status=pending、twin_status=pending、execution_authorized=false。下一步支持新插件必须经过显式代码集成、合同与证据测试；不得依靠 manifest 自称升级等级。

CLI 默认同时写入 `artifacts/registry.json`，可用 `--output path/to/report.json` 指定位置。拒绝报告同样保存，无法写入则返回非零。重复运行覆盖同名报告，CI 可为正常登记与硬件拒绝分别指定输出名。
