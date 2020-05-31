module.exports = {
    devServer: {
        proxy: {
          '/analyze': {
            target: 'http://localhost:5000/',
            changeOrigin: true,
          },
        },
      },
      outputDir: '../app/dist',
      assetsDir: 'static',
  }