#!/usr/bin/env python3
"""Build account dashboard HTML - fix undefined track issue."""
import json
import shutil

DATA_PATH = '/sessions/confident-amazing-keller/mnt/outputs/data.json'
OUTPUT_PATH = '/sessions/confident-amazing-keller/mnt/outputs/dashboard_accounts_v4.html'
WORKSPACE_PATH = '/sessions/confident-amazing-keller/mnt/对标账号月度更新/对标账号看板.html'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 确保所有账号都有赛道名称
for a in data['accounts']:
    if not a.get('赛道'):
        a['赛道'] = '未知'

template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>对标账号看板</title>
<style>
:root { color-scheme: light; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif; background: #f0f2f5; color: #333; padding: 20px; }
.header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px 24px; border-radius: 12px; margin-bottom: 20px; }
.header h1 { font-size: 22px; font-weight: 600; }
.stats-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.stat-card { background: white; border-radius: 10px; padding: 16px; min-width: 100px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.08); cursor: pointer; transition: all 0.2s; border: 2px solid transparent; }
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
.stat-card.active { border-color: #667eea; background: #f0f2ff; }
.stat-card .label { font-size: 12px; color: #888; margin-bottom: 6px; }
.stat-card .value { font-size: 24px; font-weight: 700; }
.stat-card.total .value { color: #667eea; }
.stat-card.s .value { color: #ff4d4f; }
.stat-card.a .value { color: #fa8c16; }
.stat-card.b .value { color: #1890ff; }
.stat-card.c .value { color: #52c41a; }
.stat-card.dash .value { color: #999; }
.section-title { font-size: 14px; color: #999; margin-bottom: 12px; }
.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
.chart-box { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.chart-box h3 { font-size: 14px; color: #666; margin-bottom: 12px; }
.chart-wrap { position: relative; height: 220px; }
.sheet-tabs { display: flex; gap: 0; margin-bottom: 16px; overflow-x: auto; border-bottom: 2px solid #e8e8e8; padding-bottom: 0; }
.sheet-tab { padding: 10px 16px; cursor: pointer; font-size: 13px; color: #666; border-bottom: 3px solid transparent; margin-bottom: -2px; white-space: nowrap; transition: all 0.2s; }
.sheet-tab:hover { color: #333; background: #f5f5f5; }
.sheet-tab.active { color: #667eea; border-bottom-color: #667eea; font-weight: 600; }
.sheet-tab .count { font-size: 11px; color: #aaa; margin-left: 4px; }
.sheet-tab.active .count { color: #667eea; }
.table-area { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.table-area h3 { font-size: 16px; color: #333; margin-bottom: 12px; }
.filter-bar { display: flex; gap: 10px; margin-bottom: 16px; }
.filter-bar input, .filter-bar select { padding: 8px 14px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; }
.filter-bar input { flex: 1; }
.grade-badge { display: inline-block; padding: 3px 12px; border-radius: 14px; font-size: 12px; font-weight: 600; color: white; }
.grade-S { background: #ff4d4f; }
.grade-A { background: #fa8c16; }
.grade-B { background: #1890ff; }
.grade-C { background: #52c41a; }
.grade-DASH { background: #bbb; }
.custom-table { width: 100%; border-collapse: collapse; }
.custom-table th { background: #fafafa; padding: 10px 12px; text-align: left; font-weight: 600; color: #666; border-bottom: 2px solid #eee; cursor: pointer; user-select: none; }
.custom-table th:hover { background: #f0f0f0; }
.custom-table td { padding: 10px 12px; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
.custom-table tr:hover td { background: #f5f7fa; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 16px; }
.pagination button { padding: 6px 14px; border: 1px solid #ddd; background: white; border-radius: 6px; cursor: pointer; font-size: 13px; }
.pagination button:hover { background: #f0f0f0; }
.pagination button.active { background: #667eea; color: white; border-color: #667eea; }
.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.reset-btn { display: inline-block; padding: 6px 14px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; cursor: pointer; margin-left: 10px; }
.reset-btn:hover { background: #e0e0e0; }
</style>
</head>
<body>
<div class="header"><h1>📊 对标账号发文量看板</h1></div>
<div class="stats-bar" id="statsBar"></div>
<div class="charts-grid">
  <div class="chart-box"><h3>等级分布</h3><div class="chart-wrap"><canvas id="gradeChart"></canvas></div></div>
  <div class="chart-box"><h3>赛道TOP10</h3><div class="chart-wrap"><canvas id="trackChart"></canvas></div></div>
</div>
<div class="section-title">按赛道筛选</div>
<div class="sheet-tabs" id="sheetTabs"></div>
<div class="table-area">
  <h3 id="tableTitle"></h3>
  <div class="filter-bar" id="filterBar"></div>
  <div id="tableBody"></div>
  <div class="pagination" id="pagination"></div>
</div>
<script>
var DATA = %%DATA_PLACEHOLDER%%;
var activeGrade = null;
var activeTrack = null;
var currentPage = 1;
var pageSize = 25;
var filteredAccounts = [];

function init() {
  renderStats();
  renderCharts();
  renderSheetTabs();
  renderFilters();
  applyFilters();
}

function renderStats() {
  var ag = DATA.stats.account_grades;
  var bar = document.getElementById("statsBar");
  var html = "";
  html += '<div class="stat-card total" data-filter="grade" data-value=""><div class="label">总账号</div><div class="value">' + (ag.total || DATA.accounts.length) + '</div></div>';
  html += '<div class="stat-card s" data-filter="grade" data-value="S"><div class="label">S级 (&lt;50+)</div><div class="value">' + (ag.S || 0) + '</div></div>';
  html += '<div class="stat-card a" data-filter="grade" data-value="A"><div class="label">A级 (50-100+)</div><div class="value">' + (ag.A || 0) + '</div></div>';
  html += '<div class="stat-card b" data-filter="grade" data-value="B"><div class="label">B级 (100-500+)</div><div class="value">' + (ag.B || 0) + '</div></div>';
  html += '<div class="stat-card c" data-filter="grade" data-value="C"><div class="label">C级 (&gt;500+)</div><div class="value">' + (ag.C || 0) + '</div></div>';
  html += '<div class="stat-card dash" data-filter="grade" data-value="-"><div class="label">发文数"/"</div><div class="value">' + (ag.DASH || 0) + '</div></div>';
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
  var ag = DATA.stats.account_grades;
  drawDoughnut(ag);
  drawBar();
}

function drawDoughnut(ag) {
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
  var values = [ag.S||0, ag.A||0, ag.B||0, ag.C||0, ag.DASH||0];
  var colors = ["#ff4d4f", "#fa8c16", "#1890ff", "#52c41a", "#d9d9d9"];
  var labels = ["S级", "A级", "B级", "C级", '" / "'];
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

function drawBar() {
  var canvas = document.getElementById("trackChart");
  var ctx = canvas.getContext("2d");
  var w = canvas.parentElement.offsetWidth;
  var h = canvas.parentElement.offsetHeight;
  canvas.width = w;
  canvas.height = h;
  ctx.clearRect(0, 0, w, h);
  var topTracks = DATA.stats.top_tracks || {};
  var sorted = Object.entries(topTracks).sort(function(a,b){return b[1]-a[1]}).slice(0, 10);
  if (sorted.length === 0) return;
  var maxVal = sorted[0][1];
  var barHeight = 22;
  var barGap = 6;
  var labelWidth = 100;
  var chartLeft = labelWidth + 10;
  var chartRight = w - 20;
  var chartWidth = chartRight - chartLeft;
  var startY = 10;
  ctx.font = "12px sans-serif";
  ctx.textBaseline = "middle";
  for (var i = 0; i < sorted.length; i++) {
    var y = startY + i * (barHeight + barGap);
    var label = sorted[i][0];
    var val = sorted[i][1];
    ctx.fillStyle = "#999";
    ctx.textAlign = "right";
    ctx.fillText(label, chartLeft - 8, y + barHeight / 2);
    var barW = (val / maxVal) * chartWidth;
    ctx.fillStyle = "#667eea";
    ctx.fillRect(chartLeft, y, barW, barHeight);
    ctx.fillStyle = "#666";
    ctx.textAlign = "left";
    ctx.fillText(val, chartLeft + barW + 6, y + barHeight / 2);
  }
}

// 赛道按Excel sheet顺序排列
var SHEET_ORDER = ['职场','漫画','养老金、民生','国际军事','厚黑学','美食','育儿＋高等教育','历史＋近代史','私域','地理＋旅游','职业','星座','娱乐＋剧评','小众领域','测评','毛选＋书评','鸡汤人性','自媒体、女性成长','极简、存钱','穿搭','生活小妙招＋家居','科技、数码'];
function getTrackOrder(track) {
  var idx = SHEET_ORDER.indexOf(track);
  return idx >= 0 ? idx : 999;
}

function renderSheetTabs() {
  var tabs = document.getElementById("sheetTabs");
  var tracks = [];
  var trackSet = {};
  DATA.accounts.forEach(function(a) {
    var track = a.赛道 || "未知";
    if (!trackSet[track]) {
      trackSet[track] = true;
      tracks.push(track);
    }
  });
  // 按sheet顺序排列，不在顺序表中的排到最后
  tracks.sort(function(a,b) { return getTrackOrder(a) - getTrackOrder(b); });
  var ag = DATA.stats.account_grades;
  var html = '<div class="sheet-tab" data-filter="track" data-value="" data-sheet="全部">全部<span class="count">(' + ag.total + ')</span></div>';
  tracks.forEach(function(t) {
    var count = DATA.accounts.filter(function(a) { return (a.赛道 || "未知") === t; }).length;
    html += '<div class="sheet-tab" data-filter="track" data-value="' + t + '" data-sheet="' + t + '">' + t + '<span class="count">(' + count + ')</span></div>';
  });
  tabs.innerHTML = html;
  tabs.addEventListener("click", function(e) {
    var tab = e.target.closest(".sheet-tab");
    if (!tab) return;
    var type = tab.getAttribute("data-filter");
    var value = tab.getAttribute("data-value");
    if (type === "track") toggleTrackFilter(value);
  });
}

function toggleGradeFilter(value) {
  activeGrade = (activeGrade === value) ? null : value;
  document.querySelectorAll(".stat-card").forEach(function(card) {
    var fv = card.getAttribute("data-value");
    card.classList.toggle("active", fv === activeGrade);
  });
  currentPage = 1;
  applyFilters();
}

function toggleTrackFilter(value) {
  activeTrack = (activeTrack === value) ? null : value;
  document.querySelectorAll(".sheet-tab").forEach(function(tab) {
    var fv = tab.getAttribute("data-value");
    tab.classList.toggle("active", fv === activeTrack);
  });
  currentPage = 1;
  applyFilters();
}

function renderFilters() {
  var fb = document.getElementById("filterBar");
  fb.innerHTML = '<input type="text" id="searchInput" placeholder="🔍 搜索账号名称...">';
  fb.innerHTML += '<select id="gradeFilter"><option value="">全部等级</option><option value="S">S级</option><option value="A">A级</option><option value="B">B级</option><option value="C">C级</option><option value="-">发文数"/"</option></select>';
  fb.innerHTML += '<span class="reset-btn" id="resetBtn" style="display:none">✕ 清除筛选</span>';
  document.getElementById("searchInput").addEventListener("input", function() { currentPage=1; applyFilters(); });
  document.getElementById("gradeFilter").addEventListener("change", function() { currentPage=1; applyFilters(); });
  document.getElementById("resetBtn").addEventListener("click", resetAllFilters);
}

function applyFilters() {
  var gradeVal = document.getElementById("gradeFilter").value;
  var searchVal = document.getElementById("searchInput").value;
  filteredAccounts = DATA.accounts.slice();
  if (activeTrack) filteredAccounts = filteredAccounts.filter(function(a) { return (a.赛道 || "未知") === activeTrack; });
  if (activeGrade) filteredAccounts = filteredAccounts.filter(function(a) { return a.等级 === activeGrade; });
  if (gradeVal) filteredAccounts = filteredAccounts.filter(function(a) { return a.等级 === gradeVal; });
  if (searchVal) filteredAccounts = filteredAccounts.filter(function(a) { return a.账号名称.indexOf(searchVal) !== -1; });
  renderTable();
}

function renderTable() {
  var container = document.getElementById("tableBody");
  var titleEl = document.getElementById("tableTitle");
  var resetBtn = document.getElementById("resetBtn");
  var hasFilter = activeGrade || activeTrack || document.getElementById("gradeFilter").value || document.getElementById("searchInput").value;
  if (resetBtn) resetBtn.style.display = hasFilter ? "inline-block" : "none";
  var title = "对标账号（共" + filteredAccounts.length + "个）";
  if (activeTrack) title = activeTrack + "赛道 — " + title;
  titleEl.textContent = title;
  var totalPages = Math.ceil(filteredAccounts.length / pageSize);
  if (totalPages < 1) totalPages = 1;
  if (currentPage > totalPages) currentPage = totalPages;
  var startIdx = (currentPage - 1) * pageSize;
  var endIdx = Math.min(startIdx + pageSize, filteredAccounts.length);
  var pageAccounts = filteredAccounts.slice(startIdx, endIdx);
  var html = '<table class="custom-table"><thead><tr>';
  html += '<th data-sort="等级">等级</th>';
  html += '<th data-sort="账号名称">账号名称</th>';
  html += '<th data-sort="赛道">赛道</th>';
  html += '<th data-sort="发文数量">发文数量</th>';
  html += '<th>每天发文</th>';
  html += '<th>地区</th>';
  html += '</tr></thead><tbody>';
  pageAccounts.forEach(function(item) {
    var gradeClass = item.等级 === "-" ? "grade-DASH" : "grade-" + item.等级;
    var gradeLabel = item.等级 === "-" ? "/" : item.等级;
    html += '<tr>';
    html += '<td><span class="grade-badge ' + gradeClass + '">' + gradeLabel + '</span></td>';
    html += '<td>' + item.账号名称 + '</td>';
    html += '<td>' + item.赛道 + '</td>';
    html += '<td>' + item.发文数量 + '</td>';
    html += '<td>' + item.每天发文 + '</td>';
    html += '<td>' + item.地区 + '</td>';
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

function resetAllFilters() {
  activeGrade = null;
  activeTrack = null;
  currentPage = 1;
  document.getElementById("gradeFilter").value = "";
  document.getElementById("searchInput").value = "";
  document.querySelectorAll(".stat-card").forEach(function(c) { c.classList.remove("active"); });
  document.querySelectorAll(".sheet-tab").forEach(function(t) { t.classList.remove("active"); });
  var firstTab = document.querySelector('.sheet-tab[data-value=""]');
  if (firstTab) firstTab.classList.add("active");
  applyFilters();
}

window.addEventListener("resize", function() { drawDoughnut(DATA.stats.account_grades); drawBar(); });

init();
</script>
</body>
</html>'''

# 确保stats中有total
data['stats']['account_grades']['total'] = len(data['accounts'])
data['stats']['topic_grades']['total'] = len(data['topics'])

html = template.replace('%%DATA_PLACEHOLDER%%', json.dumps(data, ensure_ascii=False))

# Validate
print('HTML length: ' + str(len(html)))

# Check JSON
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
    print('JSON VALID: ' + str(len(parsed['accounts'])) + ' accounts')
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

# Check track count
tracks = []
trackSet = {}
for a in parsed['accounts']:
    t = a.get('赛道') or '未知'
    if not trackSet.get(t):
        trackSet[t] = True
        tracks.append(t)
print('Tracks in data: ' + str(len(tracks)))
print('Track names: ' + str(sorted(tracks)))

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('Written to ' + OUTPUT_PATH + ' (' + str(len(html)) + ' bytes)')

shutil.copy2(OUTPUT_PATH, WORKSPACE_PATH)
print('Copied to workspace: ' + WORKSPACE_PATH)
