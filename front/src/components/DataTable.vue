<template>
<div>
<v-app>
<div v-text="title">
</div>
<div id="app" class="my-dt">
  <v-data-table
    :headers="headers"
    :items="tabledata"
    :search="search"
    :custom-filter="customFilter"
    sort-by="calories"
    class="elevation-1"
    show-group-by
  > 

      
    <template v-slot:top>
        
      <v-toolbar flat color="white">
        <v-select  
        v-model="filter_value"  
        :items="filter_c" id="myselect" dense></v-select>
        
        <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
        <v-spacer></v-spacer>
        <div v-text="hint"></div>
        <v-spacer></v-spacer>
        <v-btn color="green" @click="newItem()" v-if="insert">新建项</v-btn>
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
        v-if="edit"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
        v-if="delete1"
      >
        mdi-delete
      </v-icon>
    </template>
       
  </v-data-table>
</div>
<div id="app" class="my-dialog">
        
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">{{formTitle}}</span>
            </v-card-title>
            <v-card-text>
              <v-card-container>
                  <div v-for=" item in this.formdata" :key="item.id">
                  <v-row>
                   <v-select :label="item['label']" 
                    v-model="item['data']" 
                    v-if="dataalter.hasOwnProperty(item['label'])" 
                    :items="alterkeys[item['label']]"></v-select>
                    <v-text-field :label="item['label']" v-model="item['data']" v-else ></v-text-field>
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
   </div>
   </v-app>
</div>


</template>
<script>
  export default {
    data: () => ({
     dialog: false,
      headers: [
      ],
      tabledata: [],
      search:'',
      mode:'',
      editedItem: [],
      defaultItem: {
      },
      formdata:[],
      currentid:'',
      hint:'',
      datatype:{},
      dataalter:{},
      alterkeys:{},
      need_update:false,
      filter_value:'',
      filter_c:[],
    }),
    props:{
      url: {
        type: String,
        required: true
      },
      title:{
        type: String,
        required: true
      },
      delete1:{
        type: Boolean,
        default: true
      },
      insert:{
        type: Boolean,
        default: true
      },
      edit:{
        type: Boolean,
        default: true
      },
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
      //window.console.log("created")
      this.data_update();
    },
    methods: {
      customFilter(value, search,item) {
        window.console.log(JSON.stringify(value));
        window.console.log(JSON.stringify(search));
        window.console.log(JSON.stringify(item));
        window.console.log(item);
        if (item.hasOwnProperty(this.filter_value)){
          if (item[this.filter_value].toLowerCase().indexOf(search.toLowerCase()) != -1)
            return true;
          else return false;
        }
        else {
          for (var i in item){
            if (item[i].toLowerCase().indexOf(search.toLowerCase()) == -1)
            return false;
          }
          return true;
        }
      },
      newItem(){
        this.formdata=[];
        for (var head of this.headers){
          if (head['value']!='actions' && this.datatype[head['value']]!='auto' )
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
            ////window.console.log(JSON.stringify(alter));
            var alter=this.dataalter;
            for (var value of this.formdata){
              if (alter.hasOwnProperty(value['label'])){
                datadict[value['label']]=alter[value['label']][value['data']];
              }
              else{
                datadict[value['label']]=value['data'];
              }
            }
            ////window.console.log(JSON.stringify(datadict));

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
            need_update=true;
        }

        this.close()
      },
      data_update(){
        //let self = this;
        //window.console.log(this.url)
        //window.console.log(this.$props.url)
          this.$http.post(this.$props.url,JSON.stringify({method:'FORMAT'})).then(function(res){
                            var x= res.body;
                            //window.console.log(x);
                            var code=x['code'];
                            this.datatype={};
                            this.dataalter={};
                            this.filter_c=['All'];
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            }
                            
                            if (code=='success'){
                              this.editedItem={};
                              this.headers=[];
                              //window.console.log(this.headers);
                              for (var i of x['format']){
                                var item={};
                                var name =i['name']
                                //window.console.log(name);
                                  if (i['read_only']=='false'){
                                    this.editedItem[name]='';
                                  }
                                item['text']=name;
                                item['value']=name;
                                item['align']='center';
                                this.datatype[name]=i['type'];
                                this.headers.push(item);
                                this.filter_c.push(name);
                                if (i.hasOwnProperty('alter')){
                                  var tep={};
                                  for (var index in i['alter']){
                                    tep[i['alter'][index]]=index;
                                  }
                                  this.dataalter[name]=tep;
                                  var tlist=[];
                                  for (var index in i['alter']){
                                    tlist.push(i['alter'][index]);
                                  }
                                  this.alterkeys[name]=tlist;
                                }
                              }
                              if (this.$props.edit||this.$props.delete1)
                              this.headers.push({ text: 'Actions', value: 'actions', sortable: false,align:'center' });
                              ////window.console.log(this.headers);
                        }},function(res){
                            alert(res.status)
                        });
          this.$http.post(this.$props.url,JSON.stringify({method:'ALL'})).then(function(res){
                            var x= res.body;
                            var code=x['code'];
                            //window.console.log(x);
                            if (code=='fail'){
                              this.hint=x['message']
                              return;
                            } 
                            if (code=='success'){
                               //window.console.log(x['data']);
                              this.tabledata=x['data'];
                               //window.console.log(this.tabledata);
                              }
                        },function(res){
                            alert(res.status)
                        });
      
       
       //window.console.log(this.headers);
       window.vue=this;
    }
  }
  }
</script>
<style>
.my-dialog {
    position:  fixed;
    z-index: 100;
}
.my-dt{
  position: absolute center;
}
#myselect{
  position: absolute;
  width:15px;
}
.v-list{
  z-index: 100;
}
.v-application--wrap{
  min-height:0vh ;
}


</style>
