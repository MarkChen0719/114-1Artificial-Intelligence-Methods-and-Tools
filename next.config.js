/** @type {import('next').NextConfig} */
// 在 GitHub Actions 或 production 環境中使用 basePath
// GitHub Actions 會自動設定 GITHUB_ACTIONS 環境變數
const isGitHubActions = !!process.env.GITHUB_ACTIONS || !!process.env.CI
const isProduction = process.env.NODE_ENV === 'production'
const isProd = isGitHubActions || isProduction

// 如果是在 GitHub Actions 環境中，強制使用 basePath
const basePath = isProd ? '/114-1Artificial-Intelligence-Methods-and-Tools' : ''

const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: basePath,
  assetPrefix: basePath,
}

module.exports = nextConfig
