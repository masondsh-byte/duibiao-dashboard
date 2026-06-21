---
name: duibiao-dashboard-monthly-update
description: 每月更新对标账号看板的完整流程，包括数据解析、HTML生成、Git部署
type: reference
---

## 每月更新流程

### 输入
用户在对话中上传两个Excel文件：
1. `6月各领域对标账号整理最新版.xlsx` — 22个sheet，每个sheet是一个赛道的对标账号
2. `755个自媒体IP爆款选题一览.xlsx` — 755条爆款选题，黄色底色表示最新月

### 处理步骤

#### Step 1: 解析对标账号
```python
from openpyxl import load_workbook
wb = load_workbook('对标账号文件.xlsx')
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    # 找到表头行（包含"序号"的那一行）
    # 从表头下一行开始读取数据
    # sheet_name作为赛道名称
    # 发文数量解析：去掉"+"取数字，"/"表示未知
    # 分级：S(<50), A(50-100), B(100-500), C(>500)
```

#### Step 2: 解析爆款选题
```python
wb2 = load_workbook('选题文件.xlsx')
ws2 = wb2.active
for row_num in range(4, ws2.max_row + 1):
    # 检查单元格填充色判断是否黄色背景
    fill = cell.fill
    is_yellow = (fg and fg.theme == 6 and fg.tint > 0.7)
    # 阅读量解析：10万+ = 100000, 6.3万 = 63000
    # 分级：S=黄色, A=10万+, B=5-10万, C=1-5万, D=<1万
```

#### Step 3: 生成data.json
- 保存解析后的结构化数据
- 包含accounts数组、topics数组、stats统计信息

#### Step 4: 运行Python脚本生成HTML
```bash
python3 build_accounts_v4.py    # 生成对标账号看板
python3 build_topic_dashboard.py # 生成爆款选题看板
```

#### Step 5: 推送到GitHub
```bash
cd ~/Notes/Projects/流量主/运营/对标账号月度更新
git add -A
git commit -m "Update dashboard for YYYY年MM月"
git push origin main
```

### 注意事项
- Excel文件可能上传后是0字节（空文件），需要用uploads目录下的
- 赛道名称必须用sheet名，不能用细分字段
- 发文数量为"/"的账号单独列为"-"级
- 所有JS代码用var，不用const/let
- 所有事件监听用addEventListener，不用inline onclick
- 不依赖任何外部CDN，图表用Canvas手绘
