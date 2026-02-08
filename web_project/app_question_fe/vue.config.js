
const { defineConfig } = require('@vue/cli-service')

const fs = require("fs")
const path = require("path")

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // 모든 네트워크 인터페이스에서 접속 허용 (LAN 접속용)
    host: '0.0.0.0',
    // Vue 개발 서버 포트
    port: 8080,
    // https
    https: {
      key: fs.readFileSync(path.resolve(__dirname, "../cert/localhost-key.pem")),
      cert: fs.readFileSync(path.resolve(__dirname, "../cert/localhost.pem"))
    },
    proxy: {
      '/api': {
        // Flask API 서버 주소
        target: 'https://localhost:5000',
        // 호스트 헤더를 대상 서버 기준으로 변경
        changeOrigin: true,
        // self-signed 인증서 허용
        secure: false,
      }
    }
},
})
