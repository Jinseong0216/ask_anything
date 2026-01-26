
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // 모든 네트워크 인터페이스에서 접속 허용 (LAN 접속용)
    host: '0.0.0.0',
    // Vue 개발 서버 포트
    port: 8080,
    proxy: {
      '/api': {
        // Flask API 서버 주소
        target: 'http://localhost:5000',

        // 호스트 헤더를 대상 서버 기준으로 변경
        changeOrigin: true
      }
    }
},
})
