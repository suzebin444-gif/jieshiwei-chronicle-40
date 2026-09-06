# 贡献指南

## 修改内容

1. 先确认章节年代和史料依据。
2. 修改 `prompts/chapters/` 中对应章节提示词。
3. 若涉及事实纠正，同步更新 `docs/corrections-log.md` 和 `data/corrections.json`。
4. 若涉及章节元数据，同步更新 `data/chapters.json`。

## 添加图片

正式图片命名格式：

```text
ch-XX_p-YYY_v-ZZ.webp
```

示例：`ch-21_p-009_v-02.webp`。

每张图片必须登记：章节、页码、版本、来源、是否正式、审核状态、文字检查结果和备注。候选图片放在 `assets/catalog/`；确认后的正式图片放在 `assets/pages/ch-XX/`。

## 重绘流程

- 保留被替换图片，状态改为 `superseded`。
- 新图片递增版本号，初始状态为 `needs_review`。
- 检查人物名牌、对白箭头、中文准确性、史实和页码签。
- 人工通过后改为 `approved`，并重新生成画廊数据。

## 提交前

```bash
python3 scripts/validate_project.py
python3 scripts/build_site_data.py --check
```
