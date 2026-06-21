---
name: duibiao-dashboard-build-process
description: 对标账号看板制作流程：用Python从Excel解析数据嵌入HTML，纯Canvas图表，不依赖任何外部CDN
type: project
---

## 项目概述
制作两个纯离线HTML看板：对标账号发文量看板 + 爆款选题看板
数据来自两个Excel文件，嵌入HTML后用Canvas绘制图表，无任何外部依赖。

## 关键经验

### 数据解析
- Excel文件通过openpyxl读取，用Python脚本解析22个sheet
- 对标账号：每个sheet是一个赛道，用sheet名作为赛道标签
- 爆款选题：通过单元格填充色(theme=6, tint>0.7)识别黄色底色选题
- 发文数量解析：去掉"+"号取数字，"/"表示未知

### HTML生成避坑
1. **不要用模板字符串（反引号）** — 容易和HTML引号冲突导致JS报错
2. **不要用const/let** — 用var替代，兼容性更好
3. **不要依赖外部CDN** — Grid.js和Chart.js在离线环境下可能加载失败，导致白屏
4. **不要用inline onclick** — 用addEventListener替代，避免引号转义问题
5. **JSON嵌入要验证** — 用brace-counting精确定位JSON边界，不要靠字符串匹配

### 数据验证
- 生成HTML后必须检查：JSON是否合法、是否有模板字符串、是否有const/let、是否有CDN引用
- 表格数据要逐行验证：统计卡片数字、图表数据、筛选逻辑

### 部署
- 纯HTML文件可以直接发给别人双击打开
- 手机端Safari不支持file://协议，需要在线部署
- Netlify Drop免费但24小时过期，GitHub Pages永久免费
- 推送流程：git add -A → git commit → git push origin main

## 文件结构
- index.html — 对标账号看板（主页）
- topics.html — 爆款选题看板
- build_accounts_v4.py — 对标账号生成脚本
- build_topic_dashboard.py — 选题看板生成脚本
- data.json — 中间数据文件（可选，用于调试）

## 每月更新流程
1. 用户在新对话中上传两个Excel文件
2. 我读取Excel，解析数据，更新data.json
3. 运行Python脚本重新生成HTML
4. 用户git add -A && git commit && git push
