<template>
  <div>
  <nav-bar> </nav-bar>
     <data-table  url="api/unnormal" title="学籍异动管理"/>
  </div>
</template>

<script>
// @ is an alias to /src
import DataTable from '@/components/DataTable.vue'
import NavBar from '@/components/NavBar.vue'
export default {
  name: 'Home',
  components: {
    DataTable,
    NavBar
  }
 
}
</script>