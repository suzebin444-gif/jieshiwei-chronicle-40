# 《碣石卫》历史漫画：前四十章项目档案

这是一个以碣石建卫至当代发展为时间主轴的历史漫画生产项目。项目把前四十章的时间线、434页规划、史实校验规则、统一视觉规范、Codex 生图提示词、修订记录和已找回图片整理为一套可复用、可追溯、可持续补全的工程化资料。

> 当前状态：40章时间线已定稿；第7—40章章节提示词已完整整理；已找回的历史生成图片纳入素材目录，正式页与候选图分开管理。缺失或尚未可靠对应页码的图片不会被假装为“已完成”。

## 快速开始

```bash
python3 scripts/validate_project.py
python3 scripts/build_site_data.py
python3 -m http.server 8000
```

然后访问 `http://localhost:8000/site/`，即可按时代、章节和图片状态浏览项目。

## 项目结构

```text
.
├── data/                    # 章节、图片、史料和修订的机器可读数据
├── docs/                    # 时间线、史实规范、视觉圣经、工作流与审计
├── prompts/                 # 全局母提示词与40章章节提示词
├── assets/
│   ├── pages/               # 已核对章页号的正式图片
│   ├── catalog/             # 已找回但仍需人工复核的候选图片
│   └── references/          # 五色狮等视觉原型
├── scripts/                 # 校验、提示词拆分、站点数据构建脚本
└── site/                    # 零依赖静态时间线与图片画廊
```

## 核心约定

- 第1—40章严格按历史时间顺序展开；第41—50章待前四十章完成后再作专题设计。
- 史料优先级以《陆丰县志》《陆丰市志》及官方资料为首，传说必须显式标注。
- 人名牌放在对应人物身旁，不加箭头；只有人物对白框使用短箭头指向说话者。
- 简体中文必须逐字准确；无明确要求时，旗帜、城门和牌匾不放文字。
- 所有图片都通过 `data/image-manifest.json` 管理，保留来源、章页号、版本、审核状态与问题说明。

## 内容入口

- [40章时间线](docs/timeline.md)
- [项目状态与缺口](docs/project-status.md)
- [统一视觉圣经](docs/visual-bible.md)
- [史实与资料规范](docs/historical-source-policy.md)
- [已知修订记录](docs/corrections-log.md)
- [完整母提示词](prompts/MASTER-PROMPT.md)
- [生产工作流](docs/workflow.md)

## 版权与复用

- 脚本与站点代码：MIT License，见 `LICENSE-CODE`。
- 文本、提示词和项目编排：CC BY-NC-SA 4.0，见 `LICENSE-CONTENT`。
- 图片包含 AI 生成内容及用户提供参考图；复用、传播或商业使用前，应逐项核验权利、来源和平台政策。图片状态与说明以清单为准。

## 贡献

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。提交新图片时，不要只复制文件；必须同步登记清单并运行校验脚本。
