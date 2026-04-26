# Steel Intel - 鋼鐵供應鏈情報追蹤

## 專案狀態：🔧 建置中 (2026-04-14)

專案已建立骨架結構，待完成爬蟲實作與 GitHub Actions 設定。

### 系統架構

| 模組 | 說明 | 狀態 |
|------|------|------|
| **股價抓取** | 27 家公司 + 1 檔 ETF，Yahoo Finance | 🔧 待設定 |
| **新聞爬蟲** | 待建立，涵蓋 27 家公司 | 🔧 待實作 |
| **規則引擎** | 關鍵字匹配、情緒分析、重要性評分、異常偵測 | ✅ 完成 |
| **報告生成** | 每日報告、7 日報告 | ✅ 完成 |
| **前端** | D3.js Dashboard、供應鏈圖、事件時間軸 | ✅ 完成 |
| **CI/CD** | daily-ingest.yml + deploy-pages.yml | 🔧 待設定 |

### 維護檢查清單

```bash
# 一鍵健康檢查
./scripts/health_check.sh

# 或手動檢查個別項目：
gh run list --limit 5                          # GitHub Actions 狀態
ls -la data/events/$(date +%Y-%m-%d).jsonl     # 今日事件
```

---

## 標準流程

```
fetch_news.py
    │
    ├─→ data/raw/{date}/news.jsonl    (原始抓取資料)
    │
    └─→ enrich_event.py
            │
            └─→ data/events/{date}.jsonl  (標準格式，唯一資料源)
                    │
            ┌───────┴───────────────┐
            │                       │
      sync_to_frontend.py     generate_metrics.py
            │                       │
            │                 data/metrics/{date}.json
            │                       │
            │                 generate_7d_report.py
            │                       │
            │                 reports/7d/{date}.json
            │                       │
      site/data/events.json   site/data/reports/7d/{date}.json
```

### 執行順序

1. `fetch_news.py` - 抓取所有公司新聞，輸出到 `data/raw/`
2. `enrich_event.py` - 標註事件，輸出到 `data/events/`（**唯一資料源**）
3. `generate_metrics.py` - 計算每日指標
4. `generate_7d_report.py` - 生成 7 日報告
5. `sync_to_frontend.py` - 同步事件到前端
6. `update_baselines.py` - 更新歷史基準線（最後執行）

**重要**：
- `data/events/*.jsonl` 是唯一的事件資料源
- 前端的 `site/data/events.json` 由 `sync_to_frontend.py` 生成
- 不要直接寫入 `site/data/events.json`

---

## 快速啟動

```bash
cd repos/steel-intel
source .venv/bin/activate

# 啟動本地伺服器
python3 -m http.server 6230 -d site

# 瀏覽器開啟
open http://localhost:6230
```

## 抓取與處理資料

```bash
source .venv/bin/activate

# 1. 抓取新聞
python scripts/fetch_news.py

# 2. 標註事件
python scripts/enrich_event.py --date 2026-04-14

# 3. 計算指標
python scripts/generate_metrics.py --date 2026-04-14

# 4. 偵測異常
python scripts/detect_anomalies.py --date 2026-04-14

# 5. 生成報告
python scripts/generate_daily.py --date 2026-04-14
python scripts/generate_7d_report.py --date 2026-04-14

# 6. 更新基準線（最後執行）
python scripts/update_baselines.py --date 2026-04-14
```

---

## 資料夾結構

```
steel-intel/
├── .venv/                      # Python 虛擬環境
├── lib/                        # 規則引擎
│   ├── __init__.py
│   ├── matcher.py              # 關鍵字匹配
│   ├── sentiment.py            # 情緒分析
│   ├── scorer.py               # 重要性評分
│   └── anomaly.py              # 異常偵測
│
├── scripts/                    # 執行腳本
│   ├── fetch_news.py           # 整合抓取
│   ├── fetch_stocks.py         # 股價抓取
│   ├── enrich_event.py         # 事件標註
│   ├── generate_metrics.py     # 每日指標
│   ├── detect_anomalies.py     # 異常偵測
│   ├── generate_daily.py       # 每日報告
│   ├── generate_7d_report.py   # 7 日報告
│   ├── sync_to_frontend.py     # 同步事件到前端
│   ├── update_baselines.py     # 更新基準線
│   └── serve.sh
│
├── configs/                    # 設定檔
│   ├── companies.yml           # 27 家公司 + 上下游關係
│   ├── topics.yml              # 5 個主題 + 關鍵字
│   ├── sentiment_rules.yml     # 情緒詞典
│   ├── importance_rules.yml    # 重要性規則
│   └── anomaly_rules.yml       # 異常偵測規則
│
├── fetchers/                   # 公司新聞爬蟲（待實作）
│   └── base.py
│
├── data/
│   ├── raw/                    # 原始抓取資料 (按日期分目錄)
│   ├── events/                 # 標準格式事件 (JSONL，唯一資料源)
│   ├── metrics/                # 每日指標 (JSON)
│   ├── baselines/              # 歷史基準線
│   ├── normalized/             # 股價資料
│   ├── financials/             # 財務資料
│   ├── holders/                # 持股資料
│   └── fund_flow/              # 資金流向
│
├── reports/
│   ├── daily/                  # 每日報告
│   └── 7d/                     # 7 日報告
│
├── site/
│   ├── index.html              # D3.js Dashboard
│   └── data/                   # 前端資料
│
└── CLAUDE.md
```

---

## 追蹤範圍

### 公司 (27 家)

**上游 - 鐵礦砂/焦煤/廢鋼** (7 家)
- Vale 淡水河谷, BHP 必和必拓, Rio Tinto 力拓, Fortescue FMG
- Warrior Met Coal, SunCoke Energy, Commercial Metals

**中游 - 鋼鐵製造** (16 家)
- ArcelorMittal 安賽樂米塔爾, Nippon Steel 日本製鐵, JFE鋼鐵
- POSCO 浦項製鐵, Tata Steel 塔塔鋼鐵
- Nucor, Steel Dynamics, Cleveland-Cliffs, U.S. Steel, Gerdau
- China Steel 中鋼, Chung Hung 中鴻, Tung Ho 東和, Feng Hsin 豐興
- Baoshan Steel 寶鋼, Hyundai Steel 現代製鐵

**下游 - 通路/加工** (4 家)
- Reliance Inc, Ta Chen 大成鋼, Spring Rain 春雨, Tenaris

### ETF (1 檔)
- SLX VanEck Steel ETF

### 主題 (configs/topics.yml)

- 鐵礦砂價格
- 鋼品價格（HRC、CRC、鋼筋）
- 產能利用率
- 焦煤與廢鋼
- 貿易政策（關稅、反傾銷、CBAM）

---

## 事件結構

```json
{
  "id": "china_steel-2026-04-14-001",
  "date": "2026-04-14",
  "time_tags": {
    "year": 2026, "quarter": "Q2", "month": 4, "week": 16, "weekday": "Tue"
  },
  "entities": {
    "companies": ["china_steel"],
    "customers": ["chung_hung", "ta_chen"],
    "suppliers": ["vale", "bhp"]
  },
  "topics": ["steel_price", "iron_ore_price"],
  "sentiment": {
    "label": "positive",
    "score": 0.6,
    "keywords": ["調漲", "漲價"]
  },
  "importance": {
    "score": 0.85,
    "reasons": ["涉及鋼品價格", "供應鏈上下游同時提及"]
  },
  "title": "中鋼宣布下季盤價調漲",
  "content": "...",
  "sources": [
    {"url": "https://...", "type": "company_news", "fetched_at": "..."}
  ]
}
```

---

## 故障排除

### 常見問題

1. **GitHub Actions 失敗**
   - 檢查 `gh run view <run-id> --log-failed`
   - 常見原因：網站結構變更、API 限制

2. **爬蟲抓不到資料**
   - 檢查目標網站是否改版
   - 更新 `fetchers/` 對應的爬蟲

3. **前端資料未更新**
   - 確認 `sync_to_frontend.py` 有執行
   - 檢查 `site/data/events.json` 時間戳

### 手動執行流程

```bash
source .venv/bin/activate
python scripts/fetch_news.py           # 抓取新聞
python scripts/enrich_event.py         # 標註事件
python scripts/generate_metrics.py     # 計算指標
python scripts/generate_7d_report.py   # 7 日報告
python scripts/sync_to_frontend.py     # 同步前端
```


---

## 每日例行（進入此 repo 時自動提醒）

當你讀取此 CLAUDE.md 時，主動執行以下檢查並提醒用戶：

### 自動檢查清單

1. **同步最新** — `git pull origin main`
2. **今日 Actions 狀態** — `gh run list --limit 1`
3. **今日事件數** — `wc -l data/events/$(date +%Y-%m-%d).jsonl`
4. **關鍵字審計** — 讀取 `site/data/reports/daily/$(date +%Y-%m-%d).json` 的 `filter_audit` 欄位

### 提醒格式

```
📋 每日狀態
- Actions: ✅/❌
- 今日事件: N 筆
- 關鍵字審計: ✅ 通過 / ⚠️ gate2 擋住率 XX%，建議檢視
```

若 `filter_audit.alert` 為 true 或 `gate2_block_rate > 30%`，提醒用戶：「有關鍵字需要調整，要執行關鍵字審計嗎？」

### 關鍵字審計流程（用戶確認後執行）

1. 檢視 `filter_audit.gate2_samples` 中被擋住的文章標題
2. 判斷每篇是否與本追蹤產業相關
3. 相關的文章 → 找出缺少的關鍵字，建議新增到 `configs/topics.yml`
4. 呈現結果：

```
## 關鍵字審計結果

通過率：XX% | Gate 2 擋住率：XX%

### 被擋住但應通過的文章
| 標題 | 缺少的關鍵字 | 建議加入的主題 |
|------|-------------|--------------|

### 建議新增關鍵字
topics.yml → {topic_id} → keywords 新增：
- keyword1
- keyword2
```

5. 用戶確認後更新 `configs/topics.yml`，commit + push

