# liquid-metal-laptops

中国大陆笔记本液金产品库（2020–2026）——纯静态查询站点。

围绕"中国大陆在售笔记本是否使用液态金属（液金）导热"的双侧（CPU / GPU）信息，
提供可检索、可筛选、可逐条查证来源的元数据浏览。站点为单文件静态页面，
数据内嵌，零依赖、零请求、无 Cookie、无统计脚本。

## 在线站点

通过 Cloudflare Pages 部署（GitHub 集成，直接发布本仓库根目录）。

## 数据规模

| 指标 | 数值 |
| --- | --- |
| 商品变体 | 382 |
| 已确认（confirmed） | 288 |
| 待核实（pending） | 69 |
| 外部未验证（external） | 2 |
| 排除/无液金（excluded） | 23 |
| 来源条目 | 113 |
| 品牌 | 17 |
| 年份 | 2020–2026 |

证据等级（判定口径）：

- `A` 官方资料直接对应
- `B` 材料成立但 SKU / 中国范围待核
- `C` 原引不足、补证可支持
- `D` 当前无法充分证实
- `E` 与具体脚注冲突，须更正

## 目录结构

```text
liquid-metal-laptops/
├── index.html                 # 站点入口（自包含：内联 CSS/JS + 内嵌数据）
├── data/
│   └── products.json          # 最终数据集（构建产物 / 可下载）
├── sources/                   # 原始素材（公开）
│   ├── liquid-metal-quickref-2020-2026.csv   # 中国大陆笔记本液金速查表
│   ├── manual-extract-2020-2026.csv          # 速查手册提取表
│   ├── verification-120-rows.csv             # 120 条逐行核查
│   ├── verification-report.xlsx              # 完整核查报告（多工作表）
│   ├── legion-supplement-revised.xlsx        # 拯救者专项补漏修订版
│   ├── supplemental-data.md                  # 数据补充
│   └── analysis-brief.txt                    # 核查结论摘要
├── pipeline/                  # 构建流水线
│   ├── build_html.py          # data/products.json + template.html → index.html
│   ├── template.html          # 页面模板（含 __DATA_JSON__ 占位符）
│   ├── flat.css               # 扁平化主题样式（模板内联来源）
│   └── validate.py            # 校验内嵌 JSON 与脚本语法
├── _headers                   # Cloudflare Pages 响应头（CSP 等）
├── README.md
└── LICENSE
```

## 数据格式

`data/products.json` 顶层键：

- `meta` 标题、版本、生成日期、计数、证据等级口径、模糊判定策略
- `query_spec` 检索/归一化/布尔/模糊匹配规格
- `priority_fixes` 数据修订建议（按优先级）
- `supplementary_links` 补充来源链接
- `sources` 来源目录（编号 → 标题/链接/访问状态）
- `evidence` / `evidence_counts` 证据条目与分级统计
- `taxonomy` 品牌→系列→机型的分类树
- `products` 商品变体数组，每条主要字段：

```text
brand{zh,en,key} · name{zh,en} · sku_raw · sku_code · code_aliases ·
year · category_path[] · series_en · liquid_metal{claimed,type,target,composite} ·
source_codes[] · references[]{id,grade,type,url} ·
verification{grade,status,conclusion,basis,verified_note,evidence_strength,conditional} ·
note · variants[]{gpu,gpu_pattern,fuzzy_gpu,cpu,status,pending_reason} ·
fuzzy_fields[] · suspect · id · reference_link · pinyin{full,initials} ·
evidence{grade,ids[],conflict}
```

## 重新构建

无第三方依赖，Python 3：

```bash
python pipeline/build_html.py     # 用 data/products.json 重建 index.html
python pipeline/validate.py       # 校验内嵌 JSON 与脚本语法（需 Node.js）
```

## 免责声明

数据由公开资料整理与交叉核对而成，仅作维修/选购参考。同一机型不同
CPU/GPU/SKU/地区版本可能采用不同导热材料，动手前请以完整型号、原厂
FRU 与实际维修史为准。部分条目为待核实或外部未验证状态，请结合各条
证据等级判断。

## 许可

MIT License，见 [LICENSE](LICENSE)。
