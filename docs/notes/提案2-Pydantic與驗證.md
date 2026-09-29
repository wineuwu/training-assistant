# 提案 2 筆記：Pydantic、Enum 與驗證

實作 `training-api-inmemory` 任務 1–2 時整理，供日後複習。

## 一、Python 語法：跟 JS/TS 對照

**縮排就是語法**，不是排版偏好。

| | 縮排 |
|---|---|
| class 內的 `def` | 4 |
| 函式內容 | 8 |
| `if` 內容 | 12 |

Decorator 和函式之間**不能有空行**。`raise` 之後的程式碼永遠跑不到（編輯器會標灰）。

**class 有兩種用途：**

- 有 `def`、有 `self` → 傳統物件（SQLAlchemy 會碰到）
- 只有欄位、沒有 `def` → 純宣告的資料結構（Pydantic、Enum）

看 class 裡有沒有 `def`，就知道是哪一種。

**Python 用 class 比 Java 少。** 沒有狀態、只是輸入換輸出 → 寫函式就好，
module 本身就是命名空間，不需要 `XxxUtils` 這種空殼 class。

| JS/TS | Python |
|---|---|
| `constructor` | `__init__` |
| `this`（隱含） | `self`（要明寫在參數列） |
| `new Dog()` | `Dog()` |
| `extends` | `class Dog(Animal)` |
| `throw` | `raise` |
| `` `${x}` `` | `f"{x}"` |
| `arr.includes(x)` | `x in arr` |
| `=== null` | `is None` |
| 物件 `{}` | dict，但取值只能 `d["key"]` |

## 二、Pydantic

**它是什麼：** runtime 資料驗證。Python 的型別標註本身不檢查，
Pydantic 讀了那些標註才真的擋。對照：mypy/Pyright = 靜態（像 `tsc`），
Pydantic = 執行期。

**必填 / 選填是兩件事：**

```python
distance: float                 # 必填
distance: float | None          # 必填！只是允許傳 null
distance: float | None = None   # 選填
```

- `|` 是聯集型別，跟必填無關
- **有沒有預設值**才決定必填／選填

TS 的 `distance?: number` 把這兩件事寫在一起，Python 拆開寫。
這個區分在 PATCH 會很重要：「沒傳」和「明確傳 null」語意不同。

**自動轉型：** 傳字串 `"2026-03-10"` 進來，拿到的是 `date` 物件；
傳 `"running"`，拿到 `TrainingType.running`。這叫 **parse, don't validate**
──不是檢查完繼續用字串，是在門口就轉成正確型別，後面的程式碼不用再防禦。

**一次回報所有錯誤**，不是遇到第一個就停。前端一次就能拿到全部問題。

## 三、Enum

```python
class TrainingType(str, Enum):
    hiit = "hiit"
```

**一定要繼承 `str`**，否則 JSON 序列化會壞、字串比較永遠 False。

**成員名（左）只活在 Python 裡，值（右）才是 API 合約。**

- 傳輸值一律小寫 snake_case
- 顯示名稱（HIIT、羽球）是前端的事，用對照表處理
- 混在一起 → 多語系時要拆，那時已經有資料了

規格的表格就是為此分成「值 / 顯示」兩欄。

**進 DB 前改 Enum 值很便宜，進 DB 後要寫 migration。** 要加的值趁早想齊。

## 四、跨欄位驗證

```python
@model_validator(mode="after")
def validate_menu(self):
    ...
    return self          # ← 忘了會出 warning，行為詭異
```

- `mode="after"` = 欄位各自驗證完、轉型完之後才跑
- 失敗就 `raise ValueError("訊息")`，FastAPI 自動包成 422
- **一定要 `return self`**

**型別標註 vs validator：**

- 型別標註 = 結構驗證（格式對不對）
- validator = 業務規則（這組資料在領域裡合不合理）

**規則寫在 model 而不是路由裡**，POST 和 PUT 自動共用，不會不一致。

**驗證器不認識 HTTP** ──它只丟 `ValueError`，是 FastAPI 在外面翻譯成 422。
這種「業務邏輯不碰協定」就是之後 service layer 要做的事。

## 五、判斷準則

**該不該抽成常數／dict？**
判準不是「有沒有字面值」，是「會不會在多處出現、會不會獨立變動」。
只出現一次的字串寫在原地最好讀，抽出去只是讓閱讀多一次跳轉。
真正該抽的時機：多處使用、數量成長到十幾條、要多語系、前端要靠錯誤碼分支。

**程式碼很繞，還是規則本來就複雜？**
雙向驗證註定有兩個條件，再怎麼重寫也降不下去。能做的只有讓它讀起來像規則
（對稱的條件、好的錯誤訊息），不是壓成一行 XOR 把規則藏起來。

**錯誤訊息是 API 的一部分，不是 debug 訊息。**
前端看不到 code，422 的 `detail` 就是全部資訊。

## 六、測試

| | 測什麼 | 抓得到 |
|---|---|---|
| model | 規則**寫對**了嗎 | 邏輯錯誤 |
| API | 規則**接上**了嗎 | 路由沒用 model、錯誤被吃掉、沒回 422 |

model 全綠不代表 API 有擋──這是常見的假安全感。

**一般分工：** 規則的各種分支測 model（便宜、快、好定位），
每支 API 挑一兩條代表案例（一成功一失敗）。
不是把所有分支在 API 層再跑一遍，那是重複。

**判準：** 這條測試如果掛了，我學到什麼新資訊？沒有新資訊就別寫。

**`pytest.raises` 比 try/except 好在：沒丟例外也算失敗。**
手寫 `try: ... except: pass` 會變成假綠燈。

**會失敗過的測試才可信。** 看過紅燈再轉綠，比一次全綠可信。

## 七、工具

**Ruff** = Prettier + ESLint + isort 合一，Rust 寫的。Prettier 不支援 Python。

```bash
uv run ruff format main.py       # 排版
uv run ruff check --fix main.py  # 找問題 + 自動修
```

format 和 check 是兩件事：format 只動空白，check 管程式碼問題。
import 排序歸在 check，因為調換順序理論上可能改變執行結果。

規則代號看得出出身：`F` 來自 Pyflakes（確定會出錯）、`I` 來自 isort（排序偏好）。
`[*]` 標記代表可自動修。

**`--dev` 的意義：** 開發工具，提案 8 打 Docker image 時不會被裝進去。

**`.gitignore` 的 `!` 例外：** 父層目錄被忽略時子檔案的 `!` 無效，
要寫 `.vscode/*` 而不是 `.vscode/`。

## 八、名詞別搞混

| 英文 | 是什麼 |
|---|---|
| **module** | 一個 `.py` 檔，程式碼容器（JS 模組化對應這個） |
| **model** | 一份資料的形狀定義 |

`from main import Training` ──`main` 是 module，`Training` 是 model。

同一個 Training 概念之後會有**三份 model**：Pydantic（API 收送）、
SQLAlchemy（資料表）、概念層。提案 3 會看到前兩者並存。

## 九、輸入 model 與完整紀錄

```python
class TrainingCreate(BaseModel):    # 收 request：八個欄位
    ...

class Training(TrainingCreate):     # 存起來 / 回傳：多一個 id
    id: int
```

**為什麼要分兩個：** `id` 由後端產生，client 不該指定（不然兩人同時新增會撞號）。
分開之後，收的時候型別上就不可能有 id，回的時候型別上保證有 id。

合成一個（`id: int | None = None`）的代價：`/docs` 會顯示「POST 可以傳 id」，
語意錯了；回傳型別變成「id 可能是 None」，前端還要多判斷一次。

**命名：** 核心概念用最短的名字（`Training` = 一筆完整紀錄），
變體帶上用途（`TrainingCreate`、之後 PATCH 會有 `TrainingUpdate`）。
判準是「三個月後看到這名字，能不能一眼知道用途」。

之後加 `created_at`、`updated_at` 也是往完整紀錄那邊加，輸入 model 保持乾淨。
安全性上這道分界更重要：輸入 model 不該包含 `is_admin` 這類欄位，
否則有人自己送進來就提權了。

## 十、REST 狀態碼與請求解析

| 動作 | 成功 | 失敗 |
|---|---|---|
| POST 新增 | 201 Created | 422 驗證失敗 |
| GET | 200 | 404 找不到 |
| PUT 更新 | 200 | 404 / 422 |
| DELETE | 204 No Content（body 必須空） | 404 |

**FastAPI 靠參數型別決定資料從哪來：**

```python
def update_training(training_id: int, payload: TrainingCreate):
    #                ↑ 路徑參數（名字要對應 {training_id}）
    #                                ↑ Pydantic model → 自動從 body 拿
```

不用標註誰從哪來。路徑參數標 `int` 的話，`/trainings/abc` 會直接回 422，
函式根本不會被呼叫。

**`response_model` 兩個作用：** 產生 `/docs` 的回應文件、過濾掉不該回的欄位。
DELETE 回 204 不帶 body，所以不寫 `response_model`。

**405 vs 404：** 405 是「路徑存在但不支援這個方法」（通常是方法打錯），
404 是「資源不存在」。

## 十一、PUT 與它的副作用

**PUT = 全量替換**，client 送完整資料，沒送的欄位會變成 null。
**PATCH = 局部更新**，只送要改的。

判準：**使用者是在編輯整筆資料，還是對某個欄位做動作？**
編輯表單 → PUT；按讚、標記、改狀態 → PATCH。

PUT 的三個副作用：

1. **漏送 = 清空。** 前端表單少放一個欄位，那欄就被清成 null，不會報錯，
   使用者只會發現「我只改時間，備註怎麼不見了」。
   → PUT 帶來的前端約束：編輯表單必須涵蓋所有欄位。
2. **覆蓋別人的改動（lost update）。** 兩人各自載入舊資料再送出，
   後送的會把先送的洗掉。目前單人使用不會遇到，加 Agent 自動寫入後要重新評估。
3. **流量與過期欄位。** 每次都送整筆；後端計算的欄位若被 client 送回舊值會蓋錯。

PUT 是 idempotent（送一次和送十次結果相同），POST 不是。
所以網路不穩時 PUT 可以安心重試。

## 十二、兩種例外的分工

| 丟什麼 | 誰丟 | 意義 |
|---|---|---|
| `ValueError` | model validator | 業務規則錯誤，**不認識 HTTP** |
| `HTTPException` | 路由函式 | HTTP 層錯誤（404 等） |

FastAPI 負責把 `ValueError` 翻譯成 422。驗證規則因此可以完全不碰協定——
這就是之後 service layer 要做到的分工，現在已經先做到一次。

**錯誤格式目前不一致：**

```
404 → {"detail": "找不到相關訓練紀錄"}    ← 字串
422 → {"detail": [{...}, {...}]}         ← 陣列
```

422 裡每個錯誤的 `loc` 是路徑陣列，第一段說明來源（`body` / `path` / `query` / `header`），
最後一段是欄位名。前端靠它把錯誤標在對應的輸入框。

跨欄位驗證（`validate_menu`）的 `loc` 只有 `["body"]` 沒有欄位名，
因為錯的是整組資料的組合，標不到特定輸入框。

`input` 欄位會把收到的原始值回傳，除錯方便，但正式環境要小心把敏感資料吐回去。

**統一錯誤格式**（`code` + `message` + 欄位路徑）已決定要做，排在提案 2 之後。
決定它的時機是前端開始串接時，那時需求才是真的。

## 十三、留給提案 3 的問題

- 記憶體儲存的兩個限制：重啟即失、多個 worker 各有一份。
  後者在開發時（單一 process）完全看不出來，要到部署才會炸。
- `next_id` 這個手動計數器會被資料庫的自動遞增主鍵取代，
  `global` 也會跟著消失——多個 process 各有各的計數器本來就會撞號。
- 從 list 找單筆是 O(n) 逐筆掃描，資料庫用 index 解決。
- `trainings.append(...)` 現在直接寫在路由裡，換 DB 時每支 API 都要改。
  抽一層 repository 就只改那一層——這是提案 3 要親手做的抽取。
