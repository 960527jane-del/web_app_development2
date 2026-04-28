# 山資訊系統 - 系統架構設計 (Architecture Document)

## 1. 技術架構說明

本專案採用傳統且穩定的伺服器端渲染 (Server-Side Rendering) 架構，不採用前後端分離，以降低開發初期的複雜度並提高開發速度。

### 選用技術與原因
- **後端框架：Python + Flask**
  - **原因**：Flask 輕量、靈活且學習曲線平緩，非常適合快速打造 MVP (最小可行性產品)。它提供了路由與 HTTP 請求處理的基礎能力。
- **模板引擎：Jinja2**
  - **原因**：Flask 內建支援 Jinja2，可以讓我們在 HTML 頁面中輕鬆嵌入 Python 變數與邏輯，實現動態頁面渲染。
- **資料庫：SQLite**
  - **原因**：SQLite 是一個輕量級、無須獨立伺服器的關聯式資料庫，資料儲存於單一檔案中，非常適合初期開發、測試與輕量級部署。

### Flask MVC 模式說明
雖然 Flask 本身不強制規定使用 MVC (Model-View-Controller) 架構，但我們將採用類似 MVC 的設計模式來組織程式碼：
- **Model (模型)**：負責與 SQLite 資料庫互動，定義資料表結構（如：山岳資料、評論、裝備清單）並處理資料的增刪改查邏輯。
- **View (視圖)**：負責呈現使用者介面。在這裡指的是 Jinja2 HTML 模板，負責將資料轉換為使用者在瀏覽器中看到的畫面。
- **Controller (控制器)**：在 Flask 中主要由「路由 (Routes)」來擔任。負責接收使用者的請求 (Request)，向 Model 取得或寫入資料，最後將資料傳遞給 View (Jinja2 模板) 進行渲染並回傳給使用者。

## 2. 專案資料夾結構

為了讓程式碼好維護，我們將專案切分為清楚的結構：

```text
web_app_development2/
├── app/                      # 應用程式主目錄
│   ├── __init__.py           # Flask App 初始化檔案
│   ├── models/               # 資料庫模型 (Models)
│   │   ├── __init__.py
│   │   ├── mountain.py       # 山岳與安全警示相關資料表
│   │   └── user_comment.py   # 用戶與評論相關資料表
│   ├── routes/               # Flask 路由控制器 (Controllers)
│   │   ├── __init__.py
│   │   ├── main.py           # 首頁與山域檢索相關路由
│   │   └── mountain.py       # 個別山岳詳細資訊、評論相關路由
│   ├── templates/            # Jinja2 HTML 模板 (Views)
│   │   ├── base.html         # 共用模板 (包含導覽列、頁尾)
│   │   ├── index.html        # 首頁與搜尋頁面
│   │   └── detail.html       # 山岳詳細資訊頁面 (含時間軸、評論區)
│   └── static/               # 靜態資源 (CSS / JS / 圖片)
│       ├── css/
│       │   └── style.css     # 全域樣式檔
│       ├── js/
│       │   └── main.js       # 前端互動邏輯 (如簡易表單驗證、警示效果)
│       └── images/           # 網站所需圖片
├── instance/                 # 放置不進版控的執行個體檔案
│   └── database.db           # SQLite 資料庫檔案
├── docs/                     # 專案文件目錄
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構設計文件 (本文件)
├── requirements.txt          # Python 依賴套件清單
└── app.py                    # 專案啟動入口檔案
```

## 3. 元件關係圖

以下是系統運作的資料與控制流程圖：

```mermaid
flowchart TD
    Browser[使用者瀏覽器]

    subgraph Flask 後端應用程式
        Controller[Flask Route (路由控制器)]
        Model[Models (資料模型)]
        View[Jinja2 Templates (HTML 模板)]
    end

    DB[(SQLite 資料庫)]

    Browser -- "1. 發送 HTTP 請求 (如: 查詢某座山)" --> Controller
    Controller -- "2. 查詢或寫入資料" --> Model
    Model -- "3. 執行 SQL 語法" --> DB
    DB -- "4. 回傳查詢結果" --> Model
    Model -- "5. 傳遞資料結構" --> Controller
    Controller -- "6. 將資料塞入模板" --> View
    View -- "7. 渲染出完整 HTML" --> Controller
    Controller -- "8. 回傳 HTTP 回應 (包含 HTML/CSS/JS)" --> Browser
```

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (Jinja2) 而非前後端分離 (如 React/Vue)**
   - **原因**：為了快速打造初版 MVP。在不需要複雜的前端互動狀態管理下，透過 Jinja2 直接輸出 HTML 能大幅減少開發時間，並簡化部署流程，也非常利於 SEO（搜尋引擎優化）。

2. **模組化的路由與模型設計 (Blueprints / 資料夾劃分)**
   - **原因**：雖然初期系統不大，但將路由 (`routes/`) 與資料庫模型 (`models/`) 切分出來，能避免所有的程式碼都擠在同一個 `app.py` 中。這樣不僅容易找 bug，未來如果要新增功能（如會員中心）也能輕易擴展。

3. **統一的基礎模板 (`base.html`)**
   - **原因**：我們會在 `templates/base.html` 中定義網站共用的 Header、Footer 以及載入 CSS/JS 的邏輯。其他頁面只要「繼承 (extend)」這個模板，就能保持全站設計風格一致，並減少重複撰寫相同的 HTML 程式碼。

4. **將評論功能作為基礎設計納入關聯資料庫**
   - **原因**：為了實現 PRD 中「山資訊欄下方有評論或分享區」的需求，我們在資料庫設計初期就會將「山岳 (Mountain)」與「評論 (Comment)」建立關聯 (一對多關係)，確保查詢單一山岳時能快速且一併載入相關的歷史評論與分享。
