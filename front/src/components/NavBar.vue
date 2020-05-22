<template>
  <nav>
    <v-toolbar flat app color="blue" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-uppercase grey--text">
      </v-toolbar-title>
      <v-spacer>
      </v-spacer>
      <v-btn flat color="blue" @click="logout()">
        <span>Sign Out</span>
      </v-btn>
    </v-toolbar>

    <v-navigation-drawer v-model="drawer" app>
    <v-list shaped>
      <v-subheader>Web-db</v-subheader>
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
        { text: 'Dashboard' , route: '/'},
        { text: 'Campus' , route: '/campus'},
      ]
    }),
    methods: {
        logout () {
            this.$http.post('/api/logout')
        }
      }
  }
</script>
