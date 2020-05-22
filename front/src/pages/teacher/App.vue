<template>
  <div>
    <data-table  url="api/teacher" title="校区管理"/>
  </div>
</template>

<script>
// @ is an alias to /src
import DataTable from '@/components/DataTable.vue'

export default {
  name: 'Home',
  components: {
    DataTable
  }
}
</script>