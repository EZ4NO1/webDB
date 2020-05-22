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
    },
    campus: {
      // entry for the page
      entry: 'src/pages/campus/main.js',
      // output as dist/index.html
      filename: 'campus.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '校区管理'
    },
    major: {
      // entry for the page
      entry: 'src/pages/major/main.js',
      // output as dist/index.html
      filename: 'major.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '专业管理'
    },
    class: {
      // entry for the page
      entry: 'src/pages/class/main.js',
      // output as dist/index.html
      filename: 'class.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '班级管理'
    },
    student: {
      // entry for the page
      entry: 'src/pages/student/main.js',
      // output as dist/index.html
      filename: 'student.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '学生管理'
    },
    teacher: {
      // entry for the page
      entry: 'src/pages/teacher/main.js',
      // output as dist/index.html
      filename: 'teacher.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '教师管理'
    },
    mange_course: {
      // entry for the page
      entry: 'src/pages/manage_course/main.js',
      // output as dist/index.html
      filename: 'manage_course.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '课程管理',
    },
    student_course: {
      // entry for the page
      entry: 'src/pages/student_course/main.js',
      // output as dist/index.html
      filename: 'student_course.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: '学生选课',
    },


  },
  assetsDir: 'static',
  //publicPath: '/',
}
