# GitHub Pages 部署檢查清單

## 問題診斷

您訪問 `https://markchen0719.github.io/114-1/` 時看到的是 README.md 內容，而不是遊戲，這表示：

1. **GitHub Pages 可能還沒有啟用 GitHub Actions 部署**
2. **或者構建還沒有執行**
3. **或者構建路徑不正確**

## 解決步驟

### 步驟 1：確認 GitHub Pages 設定

1. 進入您的 Repository：`https://github.com/markchen0719/114-1`
2. 點擊 **Settings** → **Pages**
3. 在 **Source** 部分，選擇 **"GitHub Actions"**（不是 "Deploy from a branch"）
4. 如果沒有看到 "GitHub Actions" 選項，請確認：
   - Repository 是 Public，或
   - 您使用的是 GitHub Pro/Team 帳號

### 步驟 2：推送代碼觸發構建

```bash
# 確保所有檔案都已提交
git add .
git commit -m "Add web version deployment"
git push
```

### 步驟 3：檢查 GitHub Actions

1. 進入 Repository → **Actions** 標籤
2. 查看 "Deploy to GitHub Pages" workflow
3. 如果看到黃色圓點（進行中）或紅色 X（失敗），點擊查看詳細日誌
4. 如果看到綠色勾勾，表示構建成功

### 步驟 4：等待部署完成

- 構建通常需要 2-5 分鐘
- 部署完成後，GitHub Pages URL 會自動更新
- 可能需要等待幾分鐘讓 CDN 更新

### 步驟 5：驗證部署

訪問 `https://markchen0719.github.io/114-1/`，應該看到：
- 遊戲選單畫面（選擇 Manual/AI 模式）
- 而不是 README.md 的內容

## 常見問題

### Q: 還是看到 README.md？

**A:** 可能的原因：
1. GitHub Pages 仍設定為從 `main` 分支或 `docs/` 目錄部署
   - **解決**：改為 "GitHub Actions"
2. 構建失敗
   - **解決**：檢查 Actions 標籤中的錯誤訊息
3. 構建路徑不正確
   - **解決**：確認 `.github/workflows/deploy.yml` 中的 `path: './build/web'` 正確

### Q: Actions 顯示失敗？

**A:** 檢查錯誤訊息：
- 如果缺少依賴：確認 `requirements.txt` 包含所有必要套件
- 如果構建失敗：檢查 `build_web.py` 的輸出日誌
- 如果路徑錯誤：確認 `build/web` 目錄存在且包含 `index.html`

### Q: 如何手動觸發構建？

**A:** 
1. 進入 Repository → **Actions**
2. 選擇 "Deploy to GitHub Pages" workflow
3. 點擊 "Run workflow" 按鈕

## 驗證構建產物

構建成功後，`build/web/` 目錄應該包含：
- `index.html` - 主頁面
- `swimming_squid.data` - 遊戲資料
- `swimming_squid.wasm` - WebAssembly 檔案
- `swimming_squid.js` - JavaScript 載入器
- 其他資源檔案

## 手動部署（備用方案）

如果 GitHub Actions 有問題，可以手動部署：

```bash
# 1. 本地構建
python build_web.py

# 2. 創建 docs 目錄並複製檔案
mkdir -p docs
cp -r build/web/* docs/

# 3. 提交並推送
git add docs/
git commit -m "Manual deploy to docs"
git push

# 4. 在 GitHub Settings → Pages 中選擇 "Deploy from a branch" → "docs"
```

