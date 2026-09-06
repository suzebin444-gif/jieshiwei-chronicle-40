# AGENTS.md

本仓库是历史内容与视觉资产并重的项目。自动化工具或协作者修改仓库时必须遵守以下规则。

1. `data/chapters.json` 是章节编号、年代、页数与状态的唯一机器可读真源。
2. 第1—40章不得改变时间顺序；第41—50章在前四十章完成前不得擅自补题。
3. 史实陈述须按 `docs/historical-source-policy.md` 校验；无法确认的内容标记为“待考”或“艺术化重构”。
4. 人名牌绝不加箭头；对白框靠近人物，并以短箭头指向说话者；旁白框、页码签无箭头。
5. 不得把候选图直接提升为正式图。只有章号、页号、文字和画面均通过人工检查后，才可将 `review_status` 改为 `approved`。
6. 新增或替换图片必须更新 `data/image-manifest.json`，并运行 `python3 scripts/validate_project.py`。
7. 重绘保留旧版本，使用递增版本号；不要覆盖可追溯的历史文件。
8. 避免无依据补写具体人数、武器型号、工程规模、战果、官职和对白。

提交前检查：

```bash
python3 scripts/validate_project.py
python3 scripts/build_site_data.py --check
```
