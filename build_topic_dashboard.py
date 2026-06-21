#!/usr/bin/env python3
"""Build topic dashboard HTML from data.json - no string escaping issues."""
import json
import shutil

DATA_PATH = '/sessions/confident-amazing-keller/mnt/outputs/data.json'
OUTPUT_PATH = '/sessions/confident-amazing-keller/mnt/outputs/dashboard_topics_clean.html'
WORKSPACE_PATH = '/sessions/confident-amazing-keller/mnt/对标账号月度更新/爆款选题看板.html'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>爆款选题看板</title>
<style>
:root { color-scheme: light; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: #f0f2f5; color: #333; padding: 20px; }
.header { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px 24px; border-radius: 12px; margin-bottom: 20px; }
.header h1 { font-size: 22px; font-weight: 600; }
.header .subtitle { font-size: 13px; opacity: 0.85; margin-top: 4px; }
.stat-card.d .value { color: #bbb; }
.grade-D { background: #bbb; }
.stats-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.stat-card { background: white; border-radius: 10px; padding: 16px; min-width: 100px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.08); cursor: pointer; transition: all 0.2s; border: 2px solid transparent; }
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.stat-card.active { border-color: #ff6b6b; background: #fff5f5; }
.stat-card .label { font-size: 12px; color: #888; margin-bottom: 6px; }
.stat-card .value { font-size: 24px; font-weight: 700; }
.stat-card.total .value { color: #667eea; }
.stat-card.s .value { color: #ff6b6b; }
.stat-card.a .value { color: #fa8c16; }
.stat-card.b .value { color: #1890ff; }
.stat-card.c .value { color: #52c41a; }
.section-title { font-size: 14px; color: #999; margin-bottom: 12px; }
.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
.chart-box { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.chart-box h3 { font-size: 14px; color: #666; margin-bottom: 12px; }
.chart-wrap { position: relative; height: 220px; }
.filter-bar-top { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
.filter-bar-top select, .filter-bar-top input { padding: 8px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; }
.filter-bar-top input { flex: 1; min-width: 200px; }
.table-area { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.table-area h3 { font-size: 16px; color: #333; margin-bottom: 12px; }
.grade-badge { display: inline-block; padding: 3px 12px; border-radius: 14px; font-size: 12px; font-weight: 600; color: white; }
.grade-S { background: #ff6b6b; }
.grade-A { background: #fa8c16; }
.grade-B { background: #1890ff; }
.grade-C { background: #52c41a; }
.custom-table { width: 100%; border-collapse: collapse; }
.custom-table th { background: #fafafa; padding: 10px 12px; text-align: left; font-weight: 600; color: #666; border-bottom: 2px solid #eee; cursor: pointer; user-select: none; }
.custom-table th:hover { background: #f0f0f0; }
.custom-table td { padding: 10px 12px; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
.custom-table tr:hover td { background: #f5f7fa; }
.topic-cell { max-width: 500px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.yellow-row td { background: #fffbe6 !important; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 16px; }
.pagination button { padding: 6px 14px; border: 1px solid #ddd; background: white; border-radius: 6px; cursor: pointer; font-size: 13px; }
.pagination button:hover { background: #f0f0f0; }
.pagination button.active { background: #ff6b6b; color: white; border-color: #ff6b6b; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.reset-btn { display: inline-block; padding: 6px 14px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; cursor: pointer; }
.reset-btn:hover { background: #e0e0e0; }
</style>
</head>
<body>
<div class="header">
  <h1>🔥 爆款选题看板</h1>
  <div class="subtitle">S级=黄色底色最新月选题(30条) ｜ A级=10万+ ｜ B级=5-10万 ｜ C级=1-5万 ｜ D级=1万以下</div>
</div>
<div class="stats-bar" id="statsBar"></div>
<div class="charts-grid">
  <div class="chart-box"><h3>等级分布</h3><div class="chart-wrap"><canvas id="gradeChart"></canvas></div></div>
  <div class="chart-box"><h3>阅读量分布</h3><div class="chart-wrap"><canvas id="readChart"></canvas></div></div>
</div>
<div class="table-area">
  <h3 id="tableTitle"></h3>
  <div class="filter-bar-top" id="filterBar"></div>
  <div id="tableBody"></div>
  <div class="pagination" id="pagination"></div>
</div>
<script>
var DATA = %%DATA_PLACEHOLDER%%;
var activeGrade = null;
var currentPage = 1;
var pageSize = 25;
var filteredTopics = [];

function init() {
  renderStats();
  renderCharts();
  renderFilters();
  applyFilters();
}

function renderStats() {
  var tg = DATA.stats.topic_grades;
  var bar = document.getElementById("statsBar");
  var html = "";
  html += '<div class="stat-card total" data-filter="grade" data-value=""><div class="label">总选题</div><div class="value">' + (tg.total || DATA.topics.length) + '</div></div>';
  html += '<div class="stat-card s" data-filter="grade" data-value="S"><div class="label">S级 (黄色)</div><div class="value">' + (tg.S || 0) + '</div></div>';
  html += '<div class="stat-card a" data-filter="grade" data-value="A"><div class="label">A级 (10万+)</div><div class="value">' + (tg.A || 0) + '</div></div>';
  html += '<div class="stat-card b" data-filter="grade" data-value="B"><div class="label">B级 (5-10万)</div><div class="value">' + (tg.B || 0) + '</div></div>';
  html += '<div class="stat-card c" data-filter="grade" data-value="C"><div class="label">C级 (1-5万)</div><div class="value">' + (tg.C || 0) + '</div></div>';
  html += '<div class="stat-card d" data-filter="grade" data-value="D"><div class="label">D级 (1万以下)</div><div class="value">' + (tg.D || 0) + '</div></div>';
  bar.innerHTML = html;
  bar.addEventListener("click", function(e) {
    var card = e.target.closest(".stat-card");
    if (!card) return;
    var type = card.getAttribute("data-filter");
    var value = card.getAttribute("data-value");
    if (type === "grade") toggleGradeFilter(value);
  });
}

function renderCharts() {
  var tg = DATA.stats.topic_grades;
  drawDoughnut(tg);
  drawReadChart();
}

function drawDoughnut(tg) {
  var canvas = document.getElementById("gradeChart");
  var ctx = canvas.getContext("2d");
  var w = canvas.parentElement.offsetWidth;
  var h = canvas.parentElement.offsetHeight;
  canvas.width = w;
  canvas.height = h;
  ctx.clearRect(0, 0, w, h);
  var cx = w / 2;
  var cy = h / 2 - 20;
  var radius = Math.min(w, h) / 2 - 40;
  var inner = radius * 0.6;
  var values = [tg.S||0, tg.A||0, tg.B||0, tg.C||0, tg.D||0];
  var colors = ["#ff6b6b", "#fa8c16", "#1890ff", "#52c41a", "#bbb"];
  var labels = ["S级(黄色)", "A级(10万+)", "B级(5-10万)", "C级(1-5万)", "D级(1万-)"];
  var total = values.reduce(function(a,b){return a+b}, 0);
  if (total === 0) return;
  var startAngle = -Math.PI / 2;
  for (var i = 0; i < values.length; i++) {
    var sliceAngle = (values[i] / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, startAngle + sliceAngle);
    ctx.arc(cx, cy, inner, startAngle + sliceAngle, startAngle, true);
    ctx.closePath();
    ctx.fillStyle = colors[i];
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.stroke();
    startAngle += sliceAngle;
  }
  var legendY = h - 30;
  var legendX = 10;
  ctx.font = "11px sans-serif";
  for (var i = 0; i < labels.length; i++) {
    ctx.fillStyle = colors[i];
    ctx.fillRect(legendX, legendY, 10, 10);
    ctx.fillStyle = "#666";
    ctx.fillText(labels[i] + ": " + values[i], legendX + 14, legendY + 9);
    legendX += ctx.measureText(labels[i] + ": " + values[i]).width + 30;
  }
}

function drawReadChart() {
  var canvas = document.getElementById("readChart");
  var ctx = canvas.getContext("2d");
  var w = canvas.parentElement.offsetWidth;
  var h = canvas.parentElement.offsetHeight;
  canvas.width = w;
  canvas.height = h;
  ctx.clearRect(0, 0, w, h);
  var topics = DATA.topics;
  var ranges = [
    { label: "10万+", min: 100000, max: Infinity, color: "#ff6b6b" },
    { label: "5-10万", min: 50000, max: 100000, color: "#ffa940" },
    { label: "1-5万", min: 10000, max: 50000, color: "#69c0ff" },
    { label: "1万以下", min: 0, max: 10000, color: "#d9d9d9" },
  ];
  var counts = ranges.map(function(r) {
    return { label: r.label, count: topics.filter(function(t){return t.阅读量数值>=r.min && t.阅读量数值<r.max}).length, color: r.color };
  });
  var maxVal = Math.max.apply(null, counts.map(function(c){return c.count}));
  var barHeight = 28;
  var barGap = 8;
  var labelWidth = 60;
  var chartLeft = labelWidth + 10;
  var chartRight = w - 20;
  var chartWidth = chartRight - chartLeft;
  ctx.font = "12px sans-serif";
  ctx.textBaseline = "middle";
  for (var i = 0; i < counts.length; i++) {
    var y = 10 + i * (barHeight + barGap);
    ctx.fillStyle = "#999";
    ctx.textAlign = "right";
    ctx.fillText(counts[i].label, chartLeft - 8, y + barHeight / 2);
    var barW = (counts[i].count / maxVal) * chartWidth;
    ctx.fillStyle = counts[i].color;
    ctx.fillRect(chartLeft, y, barW, barHeight);
    ctx.fillStyle = "#666";
    ctx.textAlign = "left";
    ctx.fillText(counts[i].count, chartLeft + barW + 6, y + barHeight / 2);
  }
}

function renderFilters() {
  var fb = document.getElementById("filterBar");
  fb.innerHTML = '<input type="text" id="searchInput" placeholder="🔍 搜索选题关键词...">';
  fb.innerHTML += '<select id="gradeFilter"><option value="">全部等级</option><option value="S">S级(黄色)</option><option value="A">A级</option><option value="B">B级</option><option value="C">C级</option><option value="D">D级</option></select>';
  fb.innerHTML += '<span class="reset-btn" id="resetBtn" style="display:none">✕ 清除筛选</span>';
  document.getElementById("searchInput").addEventListener("input", function() { currentPage=1; applyFilters(); });
  document.getElementById("gradeFilter").addEventListener("change", function() { currentPage=1; applyFilters(); });
  document.getElementById("resetBtn").addEventListener("click", resetAllFilters);
}

function applyFilters() {
  var gradeVal = document.getElementById("gradeFilter").value;
  var searchVal = document.getElementById("searchInput").value;
  filteredTopics = DATA.topics.slice();
  if (activeGrade) filteredTopics = filteredTopics.filter(function(t) { return t.等级 === activeGrade; });
  if (gradeVal) filteredTopics = filteredTopics.filter(function(t) { return t.等级 === gradeVal; });
  if (searchVal) filteredTopics = filteredTopics.filter(function(t) { return t.选题.indexOf(searchVal) !== -1 || t.阅读量.indexOf(searchVal) !== -1; });
  renderTable();
}

function renderTable() {
  var container = document.getElementById("tableBody");
  var titleEl = document.getElementById("tableTitle");
  var resetBtn = document.getElementById("resetBtn");
  var hasFilter = activeGrade || document.getElementById("gradeFilter").value || document.getElementById("searchInput").value;
  if (resetBtn) resetBtn.style.display = hasFilter ? "inline-block" : "none";
  var title = "爆款选题（共" + filteredTopics.length + "条）";
  titleEl.textContent = title;
  var totalPages = Math.ceil(filteredTopics.length / pageSize);
  if (totalPages < 1) totalPages = 1;
  if (currentPage > totalPages) currentPage = totalPages;
  var startIdx = (currentPage - 1) * pageSize;
  var endIdx = Math.min(startIdx + pageSize, filteredTopics.length);
  var pageTopics = filteredTopics.slice(startIdx, endIdx);
  var html = '<table class="custom-table"><thead><tr>';
  html += '<th style="width:60px">序号</th>';
  html += '<th style="width:65px">等级</th>';
  html += '<th style="width:90px">阅读量</th>';
  html += '<th>爆款选题</th>';
  html += '</tr></thead><tbody>';
  pageTopics.forEach(function(item) {
    var gradeClass = 'grade-' + item.等级;
    var isYellow = item.is_yellow;
    html += '<tr' + (isYellow ? ' class="yellow-row"' : '') + '>';
    html += '<td>#' + item.序号 + '</td>';
    html += '<td><span class="grade-badge ' + gradeClass + '">' + item.等级 + '</span></td>';
    html += '<td>' + item.阅读量 + '</td>';
    html += '<td class="topic-cell" title="' + item.选题 + '">' + item.选题 + '</td>';
    html += '</tr>';
  });
  html += '</tbody></table>';
  container.innerHTML = html;
  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  var pag = document.getElementById("pagination");
  if (totalPages <= 1) { pag.innerHTML = ""; return; }
  var html = '<button ' + (currentPage<=1 ? 'disabled' : '') + ' onclick="goPage(' + (currentPage-1) + ')">« 上一页</button>';
  for (var i = 1; i <= totalPages; i++) {
    if (totalPages > 7 && i > 2 && i < totalPages - 1 && Math.abs(i - currentPage) > 1) continue;
    html += '<button class=' + (i === currentPage ? 'active' : '') + ' onclick="goPage(' + i + ')">' + i + '</button>';
  }
  html += '<button ' + (currentPage>=totalPages ? 'disabled' : '') + ' onclick="goPage(' + (currentPage+1) + ')">下一页 »</button>';
  html += '<span> 共' + totalPages + '页</span>';
  pag.innerHTML = html;
}

function goPage(n) { currentPage = n; applyFilters(); }

function toggleGradeFilter(value) {
  activeGrade = (activeGrade === value) ? null : value;
  document.querySelectorAll(".stat-card").forEach(function(card) {
    var fv = card.getAttribute("data-value");
    card.classList.toggle("active", fv === activeGrade);
  });
  currentPage = 1;
  applyFilters();
}

function resetAllFilters() {
  activeGrade = null;
  currentPage = 1;
  document.getElementById("gradeFilter").value = "";
  document.getElementById("searchInput").value = "";
  document.querySelectorAll(".stat-card").forEach(function(c) { c.classList.remove("active"); });
  applyFilters();
}

init();
</script>
</body>
</html>'''

# Fix topic grades to include DASH for "-" key
tg = data['stats']['topic_grades']
if '-' in tg:
    tg['DASH'] = tg.pop('-')
data['stats']['topic_grades'] = tg

# Also ensure total is set
if 'total' not in tg:
    tg['total'] = len(data['topics'])
data['stats']['topic_grades'] = tg

html = template.replace('%%DATA_PLACEHOLDER%%', json.dumps(data, ensure_ascii=False))

# Validate
print('HTML length: ' + str(len(html)))

start = html.find('var DATA = ') + 11
brace_count = 0
in_obj = False
json_end = -1
for i in range(start, len(html)):
    if html[i] == '{' and not in_obj:
        brace_count = 1
        in_obj = True
    elif html[i] == '{' and in_obj:
        brace_count += 1
    elif html[i] == '}' and in_obj:
        brace_count -= 1
        if brace_count == 0:
            json_end = i
            break

json_str = html[start:json_end+1]
try:
    parsed = json.loads(json_str)
    print('JSON VALID: ' + str(len(parsed['topics'])) + ' topics')
except Exception as e:
    print('JSON ERROR: ' + str(e))

js_section = html.split('<script>')[1].split('</script>')[0]
if '`' in js_section:
    print('WARNING: template literals')
else:
    print('OK: no template literals')

if 'const ' in js_section or 'let ' in js_section:
    print('WARNING: const/let')
else:
    print('OK: no const/let')

if 'cdn.jsdelivr' in html:
    print('WARNING: external CDN')
else:
    print('OK: fully offline')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Written to ' + OUTPUT_PATH + ' (' + str(len(html)) + ' bytes)')

shutil.copy2(OUTPUT_PATH, WORKSPACE_PATH)
print('Copied to workspace: ' + WORKSPACE_PATH)
FIXEOF
