<template>
<nav >
      <div>
      <v-btn color="blue" @click="logout()">
      登出
      </v-btn>
      </div>     
  </nav>
</template>  
<script>
  export default {
    data: () => ({
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
<style scoped>
  v-btn {
    float:right;
}