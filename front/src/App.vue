<template>
<div>
<div id="app" class="my-dt">
  <v-data-table
    :headers="headers"
    :items="tabledata"
    sort-by="calories"
    class="elevation-1"
  > 
    <template v-slot:top>
       <v-toolbar flat color="white">
        <v-toolbar-title v-text="title"></v-toolbar-title>
        <v-spacer></v-spacer>
        <div v-text="hint"></div>
        <v-spacer></v-spacer>
            <v-btn color="green" >New Item</v-btn>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
   
       
  </v-data-table>
</div>
<div id="app" class="my-dialog">
        <v-app>
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        </v-app>
        </div>
</div>
</template>
<script>
  export default {
    data: () => ({
      dialog: false,
      headers: [
        {
          text: 'Dessert (100g serving)',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: 'Calories', value: 'calories' },
        { text: 'Fat (g)', value: 'fat' },
        { text: 'Carbs (g)', value: 'carbs' },
        { text: 'Protein (g)', value: 'protein' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tabledata: [],
      editedIndex: -1,
      editedItem: {
        name: '',
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
      defaultItem: {
        name: '',
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
      url:'api/campus',
      hint:'aaaaaa',
      title:"校区管理"
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
    },

    created () {
      //this.initialize()
      this.data_update();
    },

    methods: {

      editItem (item) {
        this.editedIndex = this.tabledata.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.tabledata.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.tabledata.splice(index, 1)
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.tabledata[this.editedIndex], this.editedItem)
        } else {
          this.tabledata.push(this.editedItem)
        }
        this.close()
      },
      data_update(){
          this.$http.post(this.url,{method:'FORMAT'},{emulateJSON:true}).then(function(res){
                            var x=res.json();
                            var code=x['code'];
                            
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            }
                            
                            if (code=='success'){
                              this.headers={};
                              this.editedItem={};
                              for (var i in x['format']){
                                var name =i['name']
                                  if (i['read_only']=='false'){
                                    this.editedItem[name]='';
                                  }
                                this.headers['text']=i['name'];
                                this.headers['value']=i['name'];
                                this.headers['align']='center';
                              }
                        }},function(res){
                            alert(res.status)
                        });


          this.$http.post(this.url,{method:'ALL'},{emulateJSON:true}).then(function(res){
                            var x=res.json();
                            var code=x['code'];
                            
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            } 
                            if (code=='success'){
                              this.tabledata=x['data'];
                              }
                        },function(res){
                            alert(res.status)
                        });

       
    }
  }
  }
</script>
<style>
.my-dialog {
    position:  fixed;
    display: inline;
}
.my-dt{
  position: absolute center;
}
</style>
