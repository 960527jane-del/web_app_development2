# 山資訊系統 - 路由與頁面設計 (API & Routes Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁與山域列表 | GET | `/` | `templates/index.html` | 顯示首頁搜尋框與所有山岳列表 |
| 搜尋山岳 | GET | `/search` | `templates/index.html` | 接收 Query String 並過濾山岳列表 |
| 山岳詳細資訊 | GET | `/mountain/<int:mountain_id>` | `templates/detail.html` | 顯示單筆山岳的完整資料、時間軸、裝備與評論 |
| 建立評論 | POST | `/mountain/<int:mountain_id>/comment` | — | 接收評論表單，存入 DB，重導向回詳細頁面 |

## 2. 每個路由的詳細說明

### 2.1 首頁與山域列表
- **URL**: `/`
- **HTTP 方法**: `GET`
- **輸入**: 無
- **處理邏輯**: 呼叫 `Mountain.get_all()` 取得所有山岳資料。
- **輸出**: 渲染 `templates/index.html`，並將山岳列表傳入模板。
- **錯誤處理**: 若資料庫連線失敗，回傳 500 錯誤頁面。

### 2.2 搜尋山岳
- **URL**: `/search`
- **HTTP 方法**: `GET`
- **輸入**: Query String `?q={keyword}` (例如 `?q=玉山`)
- **處理邏輯**: 取得 `q` 參數，若有值則呼叫 `Mountain.search(keyword)`；若無值則導回首頁或顯示全部。
- **輸出**: 渲染 `templates/index.html`，並將過濾後的山岳列表與搜尋關鍵字傳入模板。
- **錯誤處理**: 若無搜尋結果，模板顯示「查無結果」提示。

### 2.3 山岳詳細資訊
- **URL**: `/mountain/<int:mountain_id>`
- **HTTP 方法**: `GET`
- **輸入**: URL 參數 `mountain_id`
- **處理邏輯**: 
  1. 呼叫 `Mountain.get_by_id(mountain_id)` 取得該山岳資料。
  2. 呼叫 `UserComment.get_by_mountain_id(mountain_id)` 取得該山岳的所有歷史評論。
- **輸出**: 渲染 `templates/detail.html`，傳入 `mountain` 與 `comments` 物件。
- **錯誤處理**: 若查無該山岳 (Mountain is None)，回傳 404 錯誤頁面 (`templates/404.html`)。

### 2.4 建立評論
- **URL**: `/mountain/<int:mountain_id>/comment`
- **HTTP 方法**: `POST`
- **輸入**: URL 參數 `mountain_id`，表單欄位 `user_name`, `comment_content`
- **處理邏輯**: 
  1. 驗證表單資料是否齊全。
  2. 呼叫 `UserComment.create(mountain_id, user_name, comment_content)` 將資料存入 SQLite。
- **輸出**: 使用 HTTP 302 重新導向 (Redirect) 至 `/mountain/<int:mountain_id>`。
- **錯誤處理**: 若表單欄位空白，透過 `flash()` 訊息提示錯誤並導回原頁面。若 `mountain_id` 不存在，回傳 404。

## 3. Jinja2 模板清單

| 模板檔案路徑 | 繼承對象 | 用途說明 |
| :--- | :--- | :--- |
| `templates/base.html` | (無) | 全站共用基礎模板，包含 `<html>` 結構、Header (導覽列)、Footer 與共同載入的 CSS/JS。定義 `{% block content %}` 供子模板填寫。 |
| `templates/index.html` | `base.html` | 首頁與搜尋結果頁面。包含一個大型搜尋框與山岳列表卡片 (Cards)。 |
| `templates/detail.html` | `base.html` | 山岳詳細頁面。包含山岳簡介、安全警示區塊、裝備清單、路況時間軸，以及最下方的評論表單與歷史留言區。 |
| `templates/404.html` | `base.html` | 找不到頁面或資料時顯示的友善錯誤頁面。 |
