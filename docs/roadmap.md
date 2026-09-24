# Training & Competition Assistant 開發路線圖

依 `project-prompt.md` 的階段切成一串 SDD 提案。一次只進行一個提案,
每個提案在 `docs/sdd/<短名>/` 有自己的 規格.md 與 任務.md;
完成後歸檔至 `docs/sdd/archive/`。

| # | 提案短名 | 對應 prompt 章節 | 範圍一句話 | 狀態 |
|---|---|---|---|---|
| 1 | `project-setup` | §21 | 目錄、Git、venv、pnpm、Vue + Vite 與 FastAPI 空專案,能各自跑起來 | 已完成 |
| 2 | `training-api-inmemory` | §7 | 五支 Training API,資料先放記憶體 list,不接 DB | 未開始 |
| 3 | `training-postgres` | §7 | 接 PostgreSQL + SQLAlchemy,取代記憶體 list | 未開始 |
| 4 | `training-frontend` | §7 | Vue 呼叫 API 完成 Training CRUD 畫面 | 未開始 |
| 5 | `competition-event` | §8 | Competition 與 Event 的 API 與畫面 | 未開始 |
| 6 | `training-goal` | §9 | 訓練目標:目前狀態、目標、進度 | 未開始 |
| 7 | `dashboard` | §10 | 本週統計、最近訓練、下一場比賽倒數 | 未開始 |
| 8 | `docker-compose` | §11 | `docker compose up` 啟動 frontend、backend、postgres | 未開始 |
| 9 | `deployment` | §12 | CI/CD、Server、Domain、HTTPS(進行時可能再拆) | 未開始 |
| 10 | `agent-query` | §13 第一、二階段 | Agent 只讀:查訓練、查準備狀況 | 未開始 |
| 11 | `agent-plan` | §13 第三階段 | Agent 讀過往訓練與教練課表,產生 Training Plan 並透過 API 寫入 | 未開始 |
| 12 | `training-planner-skill` | §14 | Skill / Harness 規則限制 Agent 行為 | 未開始 |
| 13 | `agent-eval` | §15 | 測試案例,比較 With / Without Skill | 未開始 |

## 切法原則

- Training CRUD 拆成 2、3、4 三個提案:每次只面對一個新概念
  (FastAPI request/response → SQLAlchemy → 前後端串接與 CORS)。
- 每個提案的任務不超過 10 條;進行中若發現超過,先拆再做。
- 每加入一個套件,先說明:為什麼需要、解決什麼問題、有沒有更簡單的替代。
