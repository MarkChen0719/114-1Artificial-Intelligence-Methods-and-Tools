# Swimming Squid - Web 版本部署指南

## 📋 專案結構分析

### 現有專案結構

```
swimming_squid/
├── main.py              # 原始桌面版入口（使用 MLGame）
├── main_web.py          # ✨ Web 版入口（新增）
├── src/
│   ├── game.py          # 遊戲主邏輯（SwimmingSquid 類別）
│   ├── game_object.py   # 遊戲物件（Squid, Food 等）
│   ├── foods.py         # 食物和垃圾類別
│   └── env.py           # 遊戲環境設定（尺寸、顏色等）
├── ml/
│   ├── ml_play_template.py    # AI 策略（完整版）
│   ├── ml_play_manual.py      # 手動模式（鍵盤控制）
│   ├── ml_play_knn.py          # KNN 模型版本
│   └── ml_play_collect_data.py # 資料收集版本
├── asset/               # 遊戲資源（圖片、音效）
├── levels/              # 關卡設定檔
└── build_web.py         # ✨ Web 構建腳本（新增）
```

### 遊戲主循環設計

```
初始化
  ↓
選單畫面（選擇模式）
  ↓
┌─────────────────┐
│  手動模式        │  或  │  AI 模式      │
│  鍵盤輸入        │      │  AI 決策      │
└─────────────────┘      └──────────────┘
  ↓                        ↓
遊戲更新（每一幀）
  - 更新魷魚位置
  - 更新食物/垃圾
  - 檢查碰撞
  - 更新分數
  ↓
繪製畫面
  ↓
遊戲結束？
  - 是 → 顯示結果畫面
  - 否 → 繼續遊戲
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install pygbag
pip install -r requirements.txt
```

### 2. 本地測試

```bash
# 測試遊戲邏輯（不使用 pygbag）
python test_web_local.py

# 或直接運行（會使用標準 pygame）
python main_web.py
```

### 3. 構建 Web 版本

```bash
python build_web.py
```

構建完成後，產物在 `build/web/` 目錄。

### 4. 本地預覽 Web 版本

```bash
cd build/web
python -m http.server 8000
```

然後在瀏覽器打開 `http://localhost:8000`

## 📦 部署到 GitHub Pages

### 方法 1：使用 GitHub Actions（自動部署）

1. **已創建 `.github/workflows/deploy.yml`**
   - 每次推送到 main 分支時自動構建和部署
   - 無需手動操作

2. **啟用 GitHub Pages**：
   - 進入 Repository Settings → Pages
   - Source 選擇 "GitHub Actions"

3. **推送代碼**：
   ```bash
   git add .
   git commit -m "Add web version"
   git push
   ```

### 方法 2：手動部署

1. **構建 Web 版本**：
   ```bash
   python build_web.py
   ```

2. **複製到 docs 目錄**：
   ```bash
   mkdir -p docs
   cp -r build/web/* docs/
   ```

3. **啟用 GitHub Pages**：
   - Repository Settings → Pages
   - Source 選擇 "docs" 目錄

4. **提交並推送**：
   ```bash
   git add docs/
   git commit -m "Deploy web version"
   git push
   ```

## 🎮 使用說明

### 手動模式

- **控制方式**：
  - `↑` / `W`：向上
  - `↓` / `S`：向下
  - `←` / `A`：向左
  - `→` / `D`：向右

- **其他按鍵**：
  - `ESC`：返回選單
  - `R`：遊戲結束後重新開始

### AI 模式

- AI 會自動控制魷魚
- 使用 `ml/ml_play_template.py` 中的策略：
  - 躲避 -4/-10 垃圾
  - 偏好 +4 食物
  - 考慮體積和等級
  - 前方垃圾檢測

## 🔧 技術細節

### pygbag 轉換

- `main_web.py` 使用 `async/await` 語法
- 每一幀都有 `await asyncio.sleep(0)` 讓出控制權
- 這是 pygbag 的要求

### 模式切換

- **選單模式**：顯示模式選擇按鈕
- **手動模式**：使用 `game.get_keyboard_command()` 獲取鍵盤輸入
- **AI 模式**：使用 `MLPlay.update()` 獲取 AI 決策

### 資源檔案

- 所有圖片、音效等資源會自動打包
- 確保 `asset/` 目錄中的檔案路徑正確

## ⚠️ 注意事項

1. **瀏覽器相容性**：
   - 需要支援 WebAssembly 的現代瀏覽器
   - 建議使用 Chrome、Firefox、Edge

2. **性能**：
   - WebAssembly 版本可能比原生版本稍慢
   - 這是正常的，不影響遊戲體驗

3. **資源載入**：
   - 首次載入可能需要一些時間
   - 建議使用 CDN 或優化資源大小

4. **路徑問題**：
   - Web 版本使用相對路徑
   - 確保所有資源檔案可訪問

## 🐛 故障排除

### 構建失敗

- 檢查 Python 版本（需要 3.10+）
- 確認 pygbag 已正確安裝
- 檢查 `main_web.py` 是否有語法錯誤

### 遊戲無法載入

- 檢查瀏覽器控制台的錯誤訊息
- 確認所有資源檔案路徑正確
- 檢查 GitHub Pages 設定

### AI 模式不工作

- 確認 `ml/ml_play_template.py` 存在
- 檢查 AI 類別的 `update()` 方法返回格式正確

## 📝 後續優化建議

1. **添加更多關卡選擇**
2. **添加難度設定**
3. **添加分數排行榜**
4. **優化資源載入**
5. **添加音效開關**

