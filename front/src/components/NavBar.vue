<template>
<div>
<nav>
    <v-toolbar color="blue" dark>
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
      <v-btn color="blue" @click="logout()">
      登出
      </v-btn>     
    </v-toolbar>
  </nav>

</div>
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
        { text: '学籍异动管理',route: '/unnormal_change' },
        { text: '课程管理',route: '/manage_course' },
      ],
    }),
      methods: {
      logout() {
        window.console.log('22');
         window.console.log("logout");
         this.$http.post('api/logout',JSON.stringify({})).then(function(res){
                          window.location.href='/login';
                        },function(res){
                            alert(res.status)
                        });       
      }
      }
  }
</script>