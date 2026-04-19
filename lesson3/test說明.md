# test.py 說明

這份 `lesson3/test.py` 檔案定義了一個 `Filter` 類別，用於在聊天或 WebUI 請求進入系統前後進行檢查或處理。

## 檔案功能概述

- `Filter`: 主類別，包含過濾邏輯
- `Valves`: 系統層級設定，用來控制整體過濾規則
- `UserValves`: 使用者層級設定，用來記錄每個使用者的限制值
- `inlet`: 請求進入前的預處理函式，用於驗證、檢查或修改請求內容
- `outlet`: 請求處理後的後處理函式，用於檢查或修改回應內容

## 主要欄位說明

### `Valves`

- `priority`: 過濾器優先權，預設為 `0`
- `max_turns`: 系統允許的最大對話輪數，預設為 `8`

### `UserValves`

- `max_turns`: 使用者允許的最大對話輪數，預設為 `4`

## `Filter.__init__`

- 建立 `Filter` 實例時，會初始化一個 `Valves` 物件並儲存在 `self.valves`
- 這代表系統預設的過濾設定

## `Filter.inlet(body, __user__)`

- 這個方法在請求進入前執行
- 會印出請求內容與使用者資訊，方便除錯
- 若使用者角色為 `user` 或 `admin`，會檢查 `body` 裡的 `messages` 長度
- 將 `__user__` 的 `valves.max_turns` 與系統的 `self.valves.max_turns` 取最小值，確保遵守最嚴格限制
- 若訊息數超過上限，會丟出例外並停止後續處理
- 若未超過，則回傳原始 `body`

## `Filter.outlet(body, __user__)`

- 這個方法在 API 處理完成後執行
- 目前只會印出回應內容與使用者資訊，並回傳原始 `body`
- 未對回應資料做任何修改

## 使用情境

1. 當聊天系統收到請求時，先呼叫 `Filter.inlet(...)` 檢查對話輪數是否超過限制
2. 若通過檢查，繼續執行後端處理
3. 處理完成後，呼叫 `Filter.outlet(...)` 做後處理或紀錄

## 注意事項

- `__user__` 參數預期是一個字典，包含 `role` 和 `valves`
- `valves` 物件需含 `max_turns` 屬性，否則 `inlet` 會發生錯誤
- 目前 `outlet` 並未修改回應，因此其主要作用是用於除錯或未來擴充