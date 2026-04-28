# 山資訊系統 - 流程圖設計 (Flowchart)

根據 PRD 與系統架構文件，以下為本專案的「使用者流程圖」與核心操作的「系統序列圖」，並附上對應的功能路由清單。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者進入網站後，如何進行搜尋、瀏覽山岳資訊以及發表評論的完整動線。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 山域搜尋]
    B --> C{輸入關鍵字或選擇分類?}
    C -->|送出搜尋| D[搜尋結果列表]
    D -->|點擊特定山岳| E[山岳詳細資訊頁]
    
    E --> F[查看基本資料與安全警示]
    E --> G[查看路況時間軸]
    E --> H[查看裝備清單與注意事項]
    E --> I[查看評論與分享區]
    
    I --> J{是否登入並發表評論?}
    J -->|是| K[填寫評論表單並送出]
    K --> L[系統重新載入]
    L --> E
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述了核心互動流程：「使用者在某座山的頁面送出評論」到「資料存入資料庫並重新渲染頁面」的系統後端運作過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Controller
    participant Model as 資料模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 在山岳詳細頁填寫評論並點擊送出
    Browser->>Flask: POST /mountain/{id}/comment (攜帶評論內容)
    Flask->>Model: 驗證資料並呼叫新增評論的方法
    Model->>DB: INSERT INTO user_comment ...
    DB-->>Model: 執行成功
    Model-->>Flask: 回傳新增成功狀態
    Flask-->>Browser: HTTP 302 Redirect (重新導向回山岳詳細頁)
    Browser->>Flask: GET /mountain/{id}
    Flask->>Model: 查詢該山岳資料與最新評論
    Model->>DB: SELECT ...
    DB-->>Model: 回傳資料
    Model-->>Flask: 回傳山岳物件與評論列表
    Flask-->>Browser: 渲染 Jinja2 模板回傳完整的 HTML 頁面
    Browser-->>User: 顯示包含最新評論的山岳資訊頁面
```

## 3. 功能清單與路由對照表

以下表格定義了各項功能所對應的 URL 路徑 (Routes) 與 HTTP 方法：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **首頁與山域檢索** | `/` 或 `/search` | `GET` | 顯示首頁搜尋列，或根據 Query String (如 `?q=玉山`) 顯示搜尋結果列表 |
| **山岳詳細資訊** | `/mountain/<int:mountain_id>` | `GET` | 顯示單一山岳的完整資訊，包含安全警示、時間軸、裝備清單與歷史評論 |
| **發表評論** | `/mountain/<int:mountain_id>/comment` | `POST` | 接收使用者送出的評論表單資料，儲存後導向回詳細資訊頁 |
| **會員登入 (未來擴充)** | `/login` | `GET`, `POST` | 顯示登入頁面與處理登入邏輯 |
| **會員註冊 (未來擴充)** | `/register` | `GET`, `POST` | 顯示註冊頁面與處理註冊邏輯 |
