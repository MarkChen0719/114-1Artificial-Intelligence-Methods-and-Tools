/** @type {import('next').NextConfig} */
// 在 GitHub Actions 或 production 環境中使用 basePath
// 檢查環境變數，預設為 production（用於 GitHub Pages 部署）
const isDev = process.env.NODE_ENV === 'development'
// 如果不是開發環境，則使用 basePath
const basePath = isDev ? '' : '/114-1Artificial-Intelligence-Methods-and-Tools'

const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: basePath,
  assetPrefix: basePath,
}

module.exports = nextConfig
