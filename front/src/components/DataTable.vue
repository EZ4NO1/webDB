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
        <v-btn color="green" @click="newItem()">新建项</v-btn>
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
                  <div v-for=" item in this.formdata" :key="item.id">
                  <v-row>
                    <v-text-field :label="item['label']" v-model="item['data']" ></v-text-field>
                  </v-row>
                  </div>
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
      mode:'',
      editedItem: [],
      defaultItem: {
      },
      formdata:[],
      currentid:'',
      hint:''
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
        if (this.mode=="insert")
        return '新建';

        if (this.mode=="edit") 
        return '修改';
        return 'unknown action';
      },
    },
    created () {
      //this.initialize()
      window.console.log("created")
      this.data_update();
    },
    methods: {
      newItem(){
        this.formdata=[];
        for (var head of this.headers){
          if (head['value']!='actions')
          this.formdata.push({label:head['value'],data:''});
        }
        this.mode='insert';
        this.dialog = true;

      },
      editItem (item) {
        this.formdata=[];
        for (var str1 in this.editedItem){
          this.formdata.push({label:str1,data:item[str1]});
        }
        this.mode='edit';
        this.currentid=item['id'];
        this.dialog = true;
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
      },
      save () {
        if (this.mode=='edit' || this.mode=='insert'){

            var datadict={};
            for (var value of this.formdata){
              datadict[value['label']]=value['data'];
            }
            window.console.log(JSON.stringify(datadict));

              if (this.mode=='edit') {
              datadict['id']=this.currentid;
              datadict['method']='EDIT';
              }
              if (this.mode=='insert') {
              datadict['method']='INSERT';
              }
              this.$http.post(this.$props.url,JSON.stringify(datadict)).then(function(res){
              var x = res.body;
              this.hint=x['message'];
              this.data_update();
            },function(res){
              alert(res.status)
            });
        }

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
