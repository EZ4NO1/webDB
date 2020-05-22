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
        <v-btn color="green" @click="newItem(item)">New Item</v-btn>
        </template>
    <v-icon
    small
        class="mr-2"
      >
        mdi-pencil
      </v-icon>
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

<div id="app" class="my-dialog-edit">
        <v-app>
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">{{formTitle}}</span>
            </v-card-title>
            <v-card-text>
              <v-card-container>
                <v-row>
                  <div v-for="(value,key)in this.headers" :key="key">
                    <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model=this.headers[key] label="campus id"  >{{editedItem[this.headers[key]]}}</v-text-field>
                  </v-col>
                  </div>
                </v-row>
                
                </v-card-container>
            </v-card-text>
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
      ],
      tabledata: [],
      editedIndex: -1,
      editedItem: {
      },

      defaultItem: {
        id:'',
        name: '',
        address: '',
      },
      hint:'aaaaaa'
    }),
    props:{
      url: {
        type: String,
        required: true
      },
      title:{
        type: String,
        required: true
      }
    },
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    created () {
      //this.initialize()
      window.console.log("created")
      this.data_update();
    },
    methods: {
      newItem(item){
        this.editedIndex = this.tabledata.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
        
      },
      editItem (item) {
        this.editedIndex = this.tabledata.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
        
      },
      deleteItem (item) {
        //const index = this.tabledata.indexOf(item)
        if (confirm('你真的要删除这一项吗?')==true){
          this.$http.post(this.$props.url,JSON.stringify({method:'DELETE',id:item['id']})).then(function(res){
                              var x= res.body;
                              this.hint=x['message'];
                            this.data_update();
                        },function(res){
                            alert(res.status)
                        });
                        
        }
      },
      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
      save () {
        this.json=this.editedItem
        if (this.editedIndex > -1) {
          Object.assign(this.tabledata[this.editedIndex], this.editedItem)
        } else {
          this.tabledata.push(this.editedItem)
        }
        this.json["method"] = 'INSERT'
        this.$http.post(this.$props.url,JSON.stringify(this.json)).then(function(res){
          var x = res.body;
          this.hint=x['message'];
          this.data_update();
        },function(res){
          alert(res.status)
        });
        this.close()
      },
      data_update(){
        //let self = this;
        window.console.log(this.url)
        window.console.log(this.$props.url)
          this.$http.post(this.$props.url,JSON.stringify({method:'FORMAT'})).then(function(res){
                           
                            
                            //window.console.log(res.body);
                            
                            var x= res.body;
                            window.console.log(x);
                            var code=x['code'];
                            
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            }
                            
                            if (code=='success'){
                              this.editedItem={};
                              this.headers=[];
                              window.console.log(this.headers);
                              for (var i of x['format']){
                                var item={};
                                var name =i['name']
                                window.console.log(name);
                                  if (i['read_only']=='false'){
                                    this.editedItem[name]='';
                                  }
                                item['text']=name;
                                item['value']=name;
                                item['align']='center';
                                this.headers.push(item);
                              }
                              this.headers.push({ text: 'Actions', value: 'actions', sortable: false,align:'center' });
                              //window.console.log(this.headers);
                        }},function(res){
                            alert(res.status)
                        });
          this.$http.post(this.$props.url,JSON.stringify({method:'ALL'})).then(function(res){
                            var x= res.body;
                            var code=x['code'];
                            window.console.log(x);
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            } 
                            if (code=='success'){
                               window.console.log(x['data']);
                              this.tabledata=x['data'];
                               window.console.log(this.tabledata);
                              }
                        },function(res){
                            alert(res.status)
                        });
      
       
       window.console.log(this.headers);
       window.vue=this;
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
