import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '魷魚遊戲 - Swimming Squid',
  description: '這是一個基於機器學習與 SDGs14 製作的破關小遊戲',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body>{children}</body>
    </html>
  )
}

