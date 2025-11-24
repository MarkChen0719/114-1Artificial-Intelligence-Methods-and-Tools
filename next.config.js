/** @type {import('next').NextConfig} */
// 在 GitHub Actions 或 production 環境中使用 basePath
const isProd = process.env.NODE_ENV === 'production' || process.env.GITHUB_ACTIONS === 'true'
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
