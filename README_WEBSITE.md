# 魷魚遊戲介紹網站

這是「魷魚遊戲 (Swimming Squid)」的介紹網站，基於 Next.js 建置。

## 本地開發

1. 安裝依賴：
```bash
npm install
```

2. 啟動開發伺服器：
```bash
npm run dev
```

3. 在瀏覽器中打開 [http://localhost:3000](http://localhost:3000)

## 建置與部署到 GitHub Pages

### 方法一：使用 GitHub Actions（推薦）

1. 在 GitHub 倉庫中創建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./out
      - id: deployment
        uses: actions/deploy-pages@v4
```

2. 在 GitHub 倉庫設定中：
   - 前往 Settings > Pages
   - Source 選擇 "GitHub Actions"
   - 儲存設定

3. 推送程式碼到 main 分支，GitHub Actions 會自動建置並部署。

### 方法二：手動部署

1. 建置網站：
```bash
npm run build
```

2. 建置完成後，`out` 資料夾會包含所有靜態檔案。

3. 將 `out` 資料夾的內容上傳到 GitHub Pages：
   - 如果倉庫名稱是 `username.github.io`，推送到 `main` 分支的根目錄
   - 如果倉庫名稱是其他名稱，推送到 `gh-pages` 分支，或使用 GitHub Actions

### 注意事項

- 如果網站部署在子路徑（例如 `/swimming_squid`），請確保 `next.config.js` 中的 `basePath` 設定正確。
- 如果部署在根路徑（`username.github.io`），請將 `next.config.js` 中的 `basePath` 設為空字串。

## 專案結構

```
.
├── app/
│   ├── layout.tsx      # 根布局
│   ├── page.tsx        # 首頁
│   └── globals.css     # 全域樣式
├── next.config.js      # Next.js 設定
├── package.json        # 專案依賴
└── tsconfig.json       # TypeScript 設定
```

## 修改內容

網站包含以下區塊：
- **Hero**: 主標題與介紹
- **About**: 關於遊戲的說明
- **Education**: 作者資訊
- **用到的技術**: 技術棧說明
- **Contact**: 聯絡資訊

所有內容都在 `app/page.tsx` 中，可以直接修改。

