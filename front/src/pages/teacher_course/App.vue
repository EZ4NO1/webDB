<template>
<div>
  <log-out></log-out>
    <data-table  url="api/course" title="所有已开设的课程" :delete1="false" ref="table1"/>
    <data-table  url="api/course_sign_up" title="你所开设的课的选课情况" :insert="false"  :delete1="false" ref="table2"/>
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
    LogOut
  },
  mounted() {
    this.$watch(
      "$refs.table1.need_update",
      (new_value, old_value) => {
         if (new_value){
           this.$refs.table2.data_update();
           this.$refs.table1.need_update=false;
         }
      }
    );
  }
}
</script>