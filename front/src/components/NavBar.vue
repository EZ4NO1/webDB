<template>
  <nav>
    <v-toolbar flat app color="blue" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-uppercase grey--text">
        <span class="font-weight-light">导航</span>
      </v-toolbar-title>
      <v-spacer>
      </v-spacer>
      <v-btn color="blue" @click="logout">
        登出
      </v-btn>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer" app expand-on-hover="true">  
    <v-list shaped>
      <v-list-item-group v-model="item" color="primary">
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          router :to="item.route"
        >
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    </v-navigation-drawer>
  </nav>
  
</template>  

<script>
  export default {
    data: () => ({
      drawer: true,
      item: 1,
      items: [
        { text: '学区管理' ,route: '/campus'},
        { text: '专业管理',route: '/major'},
        { text: '班级管理',route: '/class'},
        { text: '学生管理',route: '/student' },
        { text: '教师管理',route: '/teacher' },
        { text: '课程管理',route: '/course' },
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