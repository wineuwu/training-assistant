# Training & Competition Assistant

個人的訓練紀錄與比賽準備 Web App，同時是學習 Backend、Deployment、
AI Agent 的作品集專案。完整規格見 `project-prompt.md`，
階段路線見 `docs/roadmap.md`，需要時才讀，不要整份塞進 context。

## 教學深度

- 前端實作由 Claude 寫，但**結構、元件設計與寫法先問我的想法**：
  元件邊界怎麼切、狀態放哪一層、目錄怎麼組織、什麼時候抽共用、
  用哪種寫法。先問我怎麼想，討論出結論後才實作，不要自己決定完就寫。
- 我的想法你覺得有問題就直說，講清楚哪裡不合理、你會怎麼做、
  差別在哪，不要一味照做。我聽完仍堅持原做法時，照我的做。
- 教學重點放在 Python、FastAPI、REST API、SQL / PostgreSQL、
  Backend 架構、Docker、Deployment、AI Agent、Tool Calling、
  Harness / Skill、Eval。
- 我想補的後端概念：OOP、後端分層（API / service / repository）、
  資料庫請求怎麼處理。這些不另外排階段，做到自然會碰到時停下來講透：
  為什麼要這樣分、不這樣會怎樣、什麼情況不值得。講到能讓我對外
  解釋得出取捨，不是只會照做。
- 先說架構與「為什麼這樣設計」，不要逐行解釋語法。
- 適時拿 Vue / TypeScript 的對應概念來對照 Python / FastAPI。

## 這個專案額外的節奏

- 每加入一個套件，先講三件事：為什麼需要、解決什麼問題、
  有沒有更簡單的替代。
- 覺得資料模型該調整時，先解釋原因，不要直接改。

## SDD

每個提案在 `docs/sdd/<提案短名>/` 有 `規格.md` 與 `任務.md`，
短名用 `docs/roadmap.md` 表格裡的那一欄。完成後歸檔到 `docs/sdd/archive/`。

## 分支

- 一個提案一條分支，名稱 `feat/<提案短名>`，從 `master` 開出。
- `master` 不直接 commit（專案建置那次是例外，已完成）。
- merge 後刪掉分支。

## Commit 時機

- `任務.md` 的一條任務做完並打勾，就 commit 一次，訊息對應該任務。
- 打勾與 code 同一個 commit，讓歷史上每個 commit 都看得到當時進度。
- 任務做完但跑不起來，不打勾也不 commit，先修到能跑。

## PR

- 提案做完、分支推上去後，Claude 自動寫好 PR 標題與內文
  （做了什麼、為什麼、怎麼驗證），開 PR 的動作等我同意。


## 技術選擇

Frontend：Vue 3 + Vite + TypeScript + Vue Router，`<script setup>`
Composition API。Pinia 真的需要再加。不用 Nuxt——這次刻意用 Vue + Vite，
把學習重心留給 Backend。

Backend：Python + FastAPI + Pydantic + SQLAlchemy + PostgreSQL，
以 `uv` 管理相依與虛擬環境。Alembic、pytest、auth、logging 之後視需求再加。
