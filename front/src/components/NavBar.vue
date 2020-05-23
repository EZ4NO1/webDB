<template>
 <nav>
    <v-toolbar flat app color="blue" dark>
      <v-app-bar-nav-icon ></v-app-bar-nav-icon>
      <v-spacer>
      </v-spacer>
      <v-list-item v-for="(item, i) in items" :key="i">         
          <v-list-item-content>
            <a :href=serverurl+item.route>
            <v-list-item-title v-text="item.text"></v-list-item-title>
            </a>
          </v-list-item-content>
        </v-list-item>
      <v-spacer>
      </v-spacer>
      <v-btn flat color="blue">
        <span>登出</span>
      </v-btn>
    </v-toolbar>
  </nav>
</template>  

 
<style scoped>
  a:hover, a:visited, a:link, a:active {
    text-decoration: none;
    color: white;
}
</style>

<script>
  export default {
    data: () => ({
      drawer: true,
      item: 1,
      serverurl :'http://localhost:8000',
      items: [
        { text: '学区管理',route: '/campus'},
        { text: '专业管理',route: '/major'},
        { text: '班级管理',route: '/class'},
        { text: '学生管理',route: '/student' },
        { text: '教师管理',route: '/teacher' },
        { text: '课程管理',route: '/manage_course' },
        { text: '学籍异动管理',route: '/unnormal_change' },
      ],
    }),
    methos:{
      logout(){
         this.$http.post('api/logout',JSON.stringify({})).then(function(res){
                          window.location.href('/login')
                        },function(res){
                            alert(res.status)
                        });       
      }
    }
  }
</script>
