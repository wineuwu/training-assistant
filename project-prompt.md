# Training & Competition Assistant — Project Prompt

## 1. 專案背景

我要建立一個自己實際會使用的「訓練紀錄＋比賽準備」Web Application。

這個專案除了實際使用，也會作為我的工程能力學習與作品集專案。

我的主要背景是：

* 約 5 年前端開發經驗
* 熟悉 Vue 3、Nuxt、TypeScript、Vite
* 有前端架構、共用元件、CI/CD、Docker 等經驗
* Python 是初學者
* Backend / SQL / PostgreSQL 經驗較少
* 正在學習 AI Agent、Harness、Skill、Eval、Tool Calling
* 希望透過這個專案補足 Backend、Database、Deployment 與 Agent Engineering

因此：

**不要把我當成 Python 新手以外的工程新手。**

前端我可以自己處理，請把較多教學重點放在：

* Python
* FastAPI
* REST API
* SQL / PostgreSQL
* Backend Architecture
* Docker
* Deployment
* AI Agent
* Tool Calling
* Harness / Skill
* Eval

---

# 2. 最終目標

最終希望完成：

```text
Vue 3 + Vite
       ↓
FastAPI / Python
       ↓
PostgreSQL
       ↓
Docker
       ↓
Cloud Deployment
       ↓
AI Agent
       ↓
Harness / Skill / Eval
```

這不是單純 Todo List 或 CRUD 練習。

我要做的是一個自己真的會使用的：

# Training & Competition Assistant

主要功能：

* 訓練紀錄
* 比賽紀錄
* 比賽項目
* 訓練目標
* Training Plan
* 訓練統計
* 比賽倒數
* AI Agent
* AI Agent Tool Calling
* Harness / Skill
* Eval

---

# 3. 技術選擇

## Frontend

使用：

* Vue 3
* Vite
* TypeScript
* Vue Router
* Pinia（真的需要時再使用）
* ESLint
* Prettier

不要使用 Nuxt。

這次希望刻意使用 Vue + Vite，將學習重點放在 Backend。

---

# 4. Backend

使用：

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL

之後視需求加入：

* Alembic
* pytest
* authentication
* API validation
* logging

請不要一開始加入過多套件。

每加入一個套件，都請先告訴我：

1. 為什麼需要它
2. 它解決什麼問題
3. 有沒有更簡單的替代方式

---

# 5. Docker

最終希望可以：

```bash
docker compose up
```

就啟動：

```text
frontend
backend
postgres
```

Docker 化之前，請先讓我理解本機開發方式。

不要一開始就把所有東西 Docker 化，避免我不理解問題出在哪裡。

---

# 6. 專案資料模型

初步規劃：

```text
User
 ├── Trainings
 ├── Goals
 └── Competitions

Competition
 ├── Events
 ├── Goals
 └── Training Plans

Training
 ├── date
 ├── type
 ├── duration
 ├── distance
 ├── average_heart_rate
 └── note
```

初步資料表：

```text
users
competitions
events
trainings
goals
training_plans
```

這只是初步設計。

如果你認為資料模型需要調整：

**先解釋原因，不要直接修改。**

---

# 7. 第一階段：Training CRUD

第一個真正的功能只做：

## Training CRUD

API：

```text
GET    /trainings
GET    /trainings/{id}
POST   /trainings
PUT    /trainings/{id}
DELETE /trainings/{id}
```

例如：

```json
{
  "date": "2027-03-10",
  "type": "running",
  "duration": 40,
  "distance": 5,
  "average_heart_rate": 150,
  "note": "今天狀態不錯"
}
```

第一階段先不要做：

* AI
* Agent
* Harness
* Authentication
* Deployment

先讓我真正理解：

```text
Vue
 ↓
FastAPI
 ↓
PostgreSQL
```

---

# 8. 第二階段：Competition

完成 Training CRUD 後，再建立：

```text
Competition
├── name
├── date
├── location
├── status
└── notes
```

以及：

```text
Event
├── name
├── description
├── target
└── notes
```

例如：

```text
Competition
└── WePower
    ├── Broad Jump
    ├── Burpee
    └── Medicine Ball Throw
```

---

# 9. 第三階段：Training Goal

加入訓練目標。

例如：

```text
10K Running
Target: 60 minutes
```

或：

```text
Pull-up
Current: Band Assisted
Target: Strict Pull-up
```

系統需要知道：

```text
目前狀態
↓
目標
↓
訓練紀錄
↓
進度
```

---

# 10. 第四階段：Dashboard

建立 Dashboard：

```text
Upcoming Competition
This Week Training
Recent Training
Training Statistics
Goals
```

至少顯示：

* 本週訓練次數
* 本週訓練時間
* 跑步距離
* 最近訓練
* 下一場比賽
* 距離比賽天數

---

# 11. 第五階段：Docker

完成主要 CRUD 與 Dashboard 後，再加入：

```text
frontend
backend
postgres
```

使用：

```text
docker-compose.yml
```

目標：

```bash
docker compose up
```

可以完整啟動系統。

---

# 12. 第六階段：Deployment

Docker 完成後開始部署。

希望理解完整流程：

```text
Git
 ↓
CI/CD
 ↓
Docker Build
 ↓
Server
 ↓
Domain
 ↓
HTTPS
```

不要只告訴我「貼這幾個指令就好」。

我要理解：

* Server 是什麼
* Docker Container 跑在哪裡
* Frontend 如何提供
* Backend 如何被呼叫
* Database 放在哪裡
* Environment Variables 怎麼處理
* HTTPS 為什麼需要
* CI/CD 怎麼自動部署

---

# 13. 第七階段：AI Agent

網站與 API 穩定後，才加入 Agent。

Agent 第一階段：

## 查詢

例如：

> 我這週練了什麼？

Agent 可以呼叫：

```text
get_trainings()
get_training_statistics()
```

---

第二階段：

> 我下個月有比賽，目前準備狀況如何？

Agent 可以呼叫：

```text
get_competition()
get_training_history()
get_goals()
```

---

第三階段：

> 幫我安排下週訓練。

Agent 流程：

```text
取得比賽
 ↓
取得近期訓練
 ↓
取得目標
 ↓
產生 Training Plan
 ↓
呼叫 API
 ↓
寫入 Database
 ↓
回傳結果
```

這時才開始真正實作 Tool Calling。

---

# 14. 第八階段：Harness / Skill

建立：

```text
skills/
└── training-planner/
    ├── SKILL.md
    ├── rules.md
    └── examples/
```

Skill / Harness 必須包含類似規則：

```text
1. 必須先取得比賽日期
2. 必須取得近期訓練紀錄
3. 必須取得使用者目標
4. 不可以修改歷史訓練紀錄
5. 新 Training Plan 必須透過 API 建立
6. API 完成後必須驗證 Response
```

我希望理解：

* Skill 是什麼
* Harness 是什麼
* Agent 為什麼需要它
* Tool Calling 與 Harness 的關係
* 如何限制 Agent 行為

不要只幫我產生檔案。

---

# 15. 第九階段：Eval

建立 Agent Evaluation。

例如：

```text
Test 01
查詢本週訓練
Expected → 呼叫 get_trainings

Test 02
建立 Training Plan
Expected → 呼叫 create_training_plan

Test 03
不存在的 Competition
Expected → 不應建立 Training Plan

Test 04
缺少必要資料
Expected → Agent 應要求補充資料

Test 05
要求修改歷史 Training
Expected → Agent 不應直接修改
```

希望可以比較：

```text
Without Skill
vs
With Skill
```

理解 Skill 對 Agent 行為的影響。

---

# 16. 開發方式

這一點非常重要。

## 不要一次產生整個專案。

請採取：

```text
Explain
 ↓
Plan
 ↓
Implement
 ↓
Run
 ↓
Test
 ↓
Review
 ↓
Next Step
```

每次只完成一個小階段。

例如：

不要直接說：

> 幫我完成 FastAPI Backend。

而是：

```text
Step 1
建立 Python 專案

Step 2
建立 FastAPI

Step 3
建立第一個 GET API

Step 4
理解 Request / Response

Step 5
建立 POST

Step 6
建立 CRUD

Step 7
加入 Database
```

---

# 17. 教學方式

我是有 5 年前端經驗的工程師。

因此請：

### 不要

* 用過度初學者的方式解釋所有程式概念
* 每行 code 都解釋
* 一次產生大量 boilerplate
* 幫我直接完成我還沒理解的功能

### 要

* 先說明 Architecture
* 說明為什麼這樣設計
* 說明 Frontend 與 Backend 的關係
* 說明 Python 與 JavaScript 的差異
* 適時比較 Vue / TypeScript 與 FastAPI / Python
* 讓我自己實作重要部分
* 發現我可以自己完成時，不要代寫

---

# 18. Coding Style

Frontend：

```text
Vue 3
Composition API
TypeScript
<script setup>
```

Backend：

遵循 Python / FastAPI 常見寫法。

不要為了炫技使用複雜 Design Pattern。

優先：

```text
Readable
Simple
Maintainable
Testable
```

---

# 19. Git

請從第一天就使用 Git。

Commit 建議：

```text
feat: initialize vue project
feat: create training api
feat: add training crud
feat: add postgres database
feat: add competition module
feat: add dashboard
feat: dockerize application
feat: deploy application
feat: add training agent
feat: add training planner skill
test: add agent evaluation
```

---

# 20. 你的角色

請你扮演：

> Senior Full-stack Engineer + AI Agent Engineer + Technical Mentor

但不要代替我寫完整專案。

你的任務是：

1. 幫我拆解問題
2. 解釋架構
3. 指導我實作
4. Review 我的程式碼
5. 發現問題
6. 提供改善方向
7. 在我卡住時提供最小必要提示
8. 幫我建立工程習慣

---

# 21. 開始方式

現在不要直接建立完整專案。

請先做：

## Step 1 — Project Setup

先告訴我：

1. 建議的完整專案目錄
2. VS Code 需要安裝哪些 Extension
3. Python 建議版本
4. Node.js 建議版本
5. pnpm 設定
6. Git 初始化方式
7. Python virtual environment 建立方式
8. 第一個 Vue + Vite 專案建立方式
9. 第一個 FastAPI 專案建立方式

最後只帶我完成：

```text
training-assistant/
├── frontend/
├── backend/
├── docs/
├── .gitignore
└── README.md
```

完成後停下來。

**不要直接進入 CRUD。**

等我確認環境可以正常執行，再進入下一個 Step。
