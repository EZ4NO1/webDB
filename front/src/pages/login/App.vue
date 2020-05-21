<template>
  <v-app>
  <v-card width="400" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">Login</h1>
    </v-card-title>
    <v-card-text>
          <v-text-field  label="用户名" v-model="username" />

          <v-text-field  
          :type="'password'" 
          label="密码"           
           v-model="password" />
    </v-card-text>
    <v-card-actions>
    <v-spacer></v-spacer>
      <v-btn color="success" v-on:click="click"> 登录</v-btn>
    </v-card-actions>
    </v-card>
 </v-app>

</template>

<script>


export default {
  name: 'App',

  props: {
  },
  components: {
   
  },
  methods: {
    click: function () {
      window.console.log(this.username)
      this.$http.post('/api/login',{
                            username:this.username,
                            password:this.password
                        },{
                            emulateJSON:true
                        }).then(function(res){
                            alert(res.data);
                            
                        },function(res){
                            alert(res.status)
                        })
  
    
  },
  },
  data: () => ({
    username:'',
    password:''
  }),

  }
</script>
