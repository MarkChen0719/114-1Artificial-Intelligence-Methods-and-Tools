/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: process.env.NODE_ENV === 'production' ? '/114-1Artificial-Intelligence-Methods-and-Tools' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/114-1Artificial-Intelligence-Methods-and-Tools' : '',
}

module.exports = nextConfig

