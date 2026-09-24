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

## 九、留給任務 3 的問題

- 第一次碰到**狀態**：跨請求活著的 list。誰能改、什麼時候改、
  多個 worker 各自一份怎麼辦──之後所有資料庫議題的起點。
- **輸入 model ≠ 輸出 model**：POST 進來沒有 `id`，回傳要有，
  現在的 `Training` 兩邊共用會打架。
