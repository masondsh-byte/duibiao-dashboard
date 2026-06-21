# 对标账号看板项目规则

## 技术约束
- HTML看板必须是纯离线的，不依赖任何外部CDN（Grid.js、Chart.js等都不能用）
- 图表用Canvas手绘，不用任何JS图表库
- JS代码用var，不用const/let；事件监听用addEventListener，不用inline onclick
- 所有数据嵌入HTML文件内，不依赖外部资源

## 数据规范
- 对标账号看板：Excel的每个sheet代表一个赛道，sheet名就是赛道名称
- 发文量分级：S(<50+), A(50-100+), B(100-500+), C(>500+)
- 爆款选题看板：S级=黄色底色(最新月), A(≥10万), B(5-10万), C(1-5万), D(<1万)
- 所有数据按等级分组后，组内按阅读量降序排列

## 每月更新流程
1. 用户上传两个新的Excel文件
2. 我运行Python脚本解析数据
3. 运行build_accounts_v4.py和build_topic_dashboard.py生成HTML
4. 用户git add -A && git commit && git push origin main

## 部署
- GitHub Pages: https://masondsh-byte.github.io/duibiao-dashboard/
- index.html = 对标账号看板, topics.html = 爆款选题看板
