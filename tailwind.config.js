/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/web/templates/**/*.html',
    './src/web/static/js/**/*.js'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Inter','ui-sans-serif','system-ui','-apple-system','Segoe UI','Roboto','Ubuntu','Cantarell','Noto Sans','Helvetica Neue','Arial','sans-serif'
        ],
        mono: [
          'JetBrains Mono','ui-monospace','SFMono-Regular','Menlo','Monaco','Consolas','Liberation Mono','Courier New','monospace'
        ]
      }
    },
  },
  plugins: [],
}
