module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  pages: {
    login: {
      // entry for the page
      entry: 'src/pages/login/main.js',
      // output as dist/index.html
      filename: 'login.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '登入-学校综合管理系统'
    }
  },
  assetsDir: 'static',
  //publicPath: '/',
}
