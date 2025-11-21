/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: process.env.NODE_ENV === 'production' ? '/swimming_squid' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/swimming_squid' : '',
}

module.exports = nextConfig

