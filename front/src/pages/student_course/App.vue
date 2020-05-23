<template>
    <div>
    <log-out></log-out>
    <data-table  url="api/course" title="所有已开设的课程" :delete1="false" :insert="false" :edit="false"/>
    <data-table  url="api/course_sign_up" title="学生选课"  :edit="false"/>
  </div>
</template>

<script>
// @ is an alias to /src
import DataTable from '@/components/DataTable.vue'
import LogOut from '@/components/LogOut.vue'

export default {
  name: 'Home',
  components: {
    DataTable,
   LogOut,
  }
}
</script>