# Swimming Squid - Web 版本

這是 Swimming Squid 遊戲的 Web 版本，可以在瀏覽器中執行。

## 功能特色

- ✅ **手動模式**：使用鍵盤方向鍵控制魷魚
- ✅ **AI 模式**：使用訓練好的 AI 自動遊玩
- ✅ **模式選擇**：遊戲開始時可選擇模式
- ✅ **關卡系統**：支援多個關卡，通關後自動進入下一關

## 構建 Web 版本

### 前置需求

1. Python 3.10+
2. 安裝 pygbag：
   ```bash
   pip install pygbag
   ```

### 構建步驟

1. **使用構建腳本（推薦）**：
   ```bash
   python build_web.py
   ```

2. **或手動構建**：
   ```bash
   python -m pygbag --app_name swimming_squid --title "Swimming Squid" main_web.py
   ```

3. **構建產物**：
   - 構建完成後，產物會在 `build/web/` 目錄
   - 將該目錄的內容部署到 GitHub Pages

## 部署到 GitHub Pages

### 方法 1：使用 GitHub Actions（推薦）

1. 在專案根目錄創建 `.github/workflows/deploy.yml`：
   ```yaml
   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [ main ]
   
   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         - run: pip install pygbag
         - run: python build_web.py
         - uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./build/web
   ```

### 方法 2：手動部署

1. 構建 Web 版本：
   ```bash
   python build_web.py
   ```

2. 將 `build/web/` 目錄的內容複製到 `docs/` 目錄

3. 在 GitHub 設定中啟用 GitHub Pages，選擇 `docs` 目錄作為來源

## 使用方式

### 在瀏覽器中

1. 打開部署的網頁
2. 選擇遊戲模式：
   - 點擊「手動模式」按鈕或按 `M` 鍵
   - 點擊「AI 模式」按鈕或按 `A` 鍵

### 手動模式控制

- `↑` / `W`：向上移動
- `↓` / `S`：向下移動
- `←` / `A`：向左移動
- `→` / `D`：向右移動
- `ESC`：返回選單

### AI 模式

- AI 會自動控制魷魚移動
- 使用 `ml/ml_play_template.py` 中的策略
- 包含完整的垃圾躲避、+4 偏好等邏輯

## 本地測試

在構建前，可以先本地測試：

```bash
python main_web.py
```

## 注意事項

1. **資源檔案**：確保所有圖片、音效等資源檔案都在正確位置
2. **路徑問題**：Web 版本使用相對路徑，確保資源檔案可訪問
3. **性能**：WebAssembly 版本可能比原生版本稍慢，這是正常的
4. **瀏覽器相容性**：建議使用 Chrome、Firefox、Edge 等現代瀏覽器

## 故障排除

### 構建失敗

- 檢查 Python 版本（需要 3.10+）
- 確認所有依賴都已安裝
- 檢查 `main_web.py` 是否有語法錯誤

### 遊戲無法載入

- 檢查瀏覽器控制台的錯誤訊息
- 確認所有資源檔案路徑正確
- 檢查 GitHub Pages 設定是否正確

