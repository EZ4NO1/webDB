(function(t){function e(e){for(var n,i,s=e[0],l=e[1],c=e[2],u=0,f=[];u<s.length;u++)i=s[u],Object.prototype.hasOwnProperty.call(r,i)&&r[i]&&f.push(r[i][0]),r[i]=0;for(n in l)Object.prototype.hasOwnProperty.call(l,n)&&(t[n]=l[n]);d&&d(e);while(f.length)f.shift()();return o.push.apply(o,c||[]),a()}function a(){for(var t,e=0;e<o.length;e++){for(var a=o[e],n=!0,s=1;s<a.length;s++){var l=a[s];0!==r[l]&&(n=!1)}n&&(o.splice(e--,1),t=i(i.s=a[0]))}return t}var n={},r={class:0},o=[];function i(e){if(n[e])return n[e].exports;var a=n[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,i),a.l=!0,a.exports}i.m=t,i.c=n,i.d=function(t,e,a){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},i.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(i.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)i.d(a,n,function(e){return t[e]}.bind(null,n));return a},i.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="/";var s=window["webpackJsonp"]=window["webpackJsonp"]||[],l=s.push.bind(s);s.push=e,s=s.slice();for(var c=0;c<s.length;c++)e(s[c]);var d=l;o.push([4,"chunk-vendors"]),a()})({0:function(t,e){},"1fdb":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"my-dt",attrs:{id:"app"}},[a("v-data-table",{staticClass:"elevation-1",attrs:{headers:t.headers,items:t.tabledata,"sort-by":"calories"},scopedSlots:t._u([{key:"top",fn:function(){return[a("v-toolbar",{attrs:{flat:"",color:"white"}},[a("v-toolbar-title",{domProps:{textContent:t._s(t.title)}}),a("v-spacer"),a("div",{domProps:{textContent:t._s(t.hint)}}),a("v-spacer"),a("v-btn",{attrs:{color:"green"},on:{click:function(e){return t.newItem()}}},[t._v("新建项")])],1)]},proxy:!0},{key:"item.actions",fn:function(e){var n=e.item;return[a("v-icon",{staticClass:"mr-2",attrs:{small:""},on:{click:function(e){return t.editItem(n)}}},[t._v(" mdi-pencil ")]),a("v-icon",{attrs:{small:""},on:{click:function(e){return t.deleteItem(n)}}},[t._v(" mdi-delete ")])]}},{key:"no-data",fn:function(){return[a("v-btn",{attrs:{color:"primary"},on:{click:t.initialize}},[t._v("Reset")])]},proxy:!0}])},[a("v-icon",{staticClass:"mr-2",attrs:{small:""}},[t._v(" mdi-pencil ")])],1)],1),a("div",{staticClass:"my-dialog-edit",attrs:{id:"app"}},[a("v-app",[a("v-dialog",{attrs:{"max-width":"500px"},model:{value:t.dialog,callback:function(e){t.dialog=e},expression:"dialog"}},[a("v-card",[a("v-card-title",[a("span",{staticClass:"headline"},[t._v(t._s(t.formTitle))])]),a("v-card-text",[a("v-card-container",t._l(this.formdata,(function(e){return a("div",{key:e.id},[a("v-row",[t.dataalter.hasOwnProperty(e["label"])?a("v-select",{attrs:{label:e["label"],items:t.alterkeys[e["label"]]},model:{value:e["data"],callback:function(a){t.$set(e,"data",a)},expression:"item['data']"}}):a("v-text-field",{attrs:{label:e["label"]},model:{value:e["data"],callback:function(a){t.$set(e,"data",a)},expression:"item['data']"}})],1)],1)})),0)],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"blue darken-1",text:""},on:{click:t.close}},[t._v("Cancel")]),a("v-btn",{attrs:{color:"blue darken-1",text:""},on:{click:t.save}},[t._v("Save")])],1)],1)],1)],1)],1)])},r=[],o=(a("b0c0"),a("b85c")),i={data:function(){return{dialog:!1,headers:[],tabledata:[],mode:"",editedItem:[],defaultItem:{},formdata:[],currentid:"",hint:"",datatype:{},dataalter:{},alterkeys:{}}},props:{url:{type:String,required:!0},title:{type:String,required:!0}},computed:{formTitle:function(){return"insert"==this.mode?"新建":"edit"==this.mode?"修改":"unknown action"}},created:function(){window.console.log("created"),this.data_update()},methods:{newItem:function(){this.formdata=[];var t,e=Object(o["a"])(this.headers);try{for(e.s();!(t=e.n()).done;){var a=t.value;"actions"!=a["value"]&&"auto"!=this.datatype[a["value"]]&&this.formdata.push({label:a["value"],data:""})}}catch(n){e.e(n)}finally{e.f()}this.mode="insert",this.dialog=!0},editItem:function(t){for(var e in this.formdata=[],this.editedItem)this.formdata.push({label:e,data:t[e]});this.mode="edit",this.currentid=t["id"],this.dialog=!0},deleteItem:function(t){1==confirm("你真的要删除这一项吗?")&&this.$http.post(this.$props.url,JSON.stringify({method:"DELETE",id:t["id"]})).then((function(t){var e=t.body;this.hint=e["message"],this.data_update()}),(function(t){alert(t.status)}))},close:function(){this.dialog=!1},save:function(){if("edit"==this.mode||"insert"==this.mode){var t={};window.console.log(JSON.stringify(a));var e,a=this.dataalter,n=Object(o["a"])(this.formdata);try{for(n.s();!(e=n.n()).done;){var r=e.value;a.hasOwnProperty(r["label"])?t[r["label"]]=a[r["label"]][r["data"]]:t[r["label"]]=r["data"]}}catch(i){n.e(i)}finally{n.f()}window.console.log(JSON.stringify(t)),"edit"==this.mode&&(t["id"]=this.currentid,t["method"]="EDIT"),"insert"==this.mode&&(t["method"]="INSERT"),this.$http.post(this.$props.url,JSON.stringify(t)).then((function(t){var e=t.body;this.hint=e["message"],this.data_update()}),(function(t){alert(t.status)}))}this.close()},data_update:function(){window.console.log(this.url),window.console.log(this.$props.url),this.$http.post(this.$props.url,JSON.stringify({method:"FORMAT"})).then((function(t){var e=t.body;window.console.log(e);var a=e["code"];if(this.datatype={},this.dataalter={},"fail"!=a){if("success"==a){this.editedItem={},this.headers=[],window.console.log(this.headers);var n,r=Object(o["a"])(e["format"]);try{for(r.s();!(n=r.n()).done;){var i=n.value,s={},l=i["name"];if(window.console.log(l),"false"==i["read_only"]&&(this.editedItem[l]=""),s["text"]=l,s["value"]=l,s["align"]="center",this.datatype[l]=i["type"],this.headers.push(s),i.hasOwnProperty("alter")){var c={};for(var d in i["alter"])c[i["alter"][d]]=d;this.dataalter[l]=c;var u=[];for(var d in i["alter"])u.push(i["alter"][d]);this.alterkeys[l]=u}}}catch(f){r.e(f)}finally{r.f()}this.headers.push({text:"Actions",value:"actions",sortable:!1,align:"center"})}}else this.hint=e["message"]}),(function(t){alert(t.status)})),this.$http.post(this.$props.url,JSON.stringify({method:"ALL"})).then((function(t){var e=t.body,a=e["code"];window.console.log(e),"fail"!=a?"success"==a&&(window.console.log(e["data"]),this.tabledata=e["data"],window.console.log(this.tabledata)):this.hint=e["message"]}),(function(t){alert(t.status)})),window.console.log(this.headers),window.vue=this}}},s=i,l=(a("6224"),a("2877")),c=a("6544"),d=a.n(c),u=a("7496"),f=a("8336"),p=a("b0af"),h=a("99d9"),v=a("8fea"),m=a("169a"),b=a("132d"),y=a("0fd9"),w=a("b974"),g=a("2fa4"),x=a("8654"),_=a("71d9"),O=a("2a7f"),k=Object(l["a"])(s,n,r,!1,null,null,null);e["a"]=k.exports;d()(k,{VApp:u["a"],VBtn:f["a"],VCard:p["a"],VCardActions:h["a"],VCardText:h["b"],VCardTitle:h["c"],VDataTable:v["a"],VDialog:m["a"],VIcon:b["a"],VRow:y["a"],VSelect:w["a"],VSpacer:g["a"],VTextField:x["a"],VToolbar:_["a"],VToolbarTitle:O["a"]})},4:function(t,e,a){t.exports=a("95edb")},"402c":function(t,e,a){"use strict";var n=a("2b0e"),r=a("f309");n["a"].use(r["a"]),e["a"]=new r["a"]({})},5974:function(t,e,a){},6224:function(t,e,a){"use strict";var n=a("5974"),r=a.n(n);r.a},"95edb":function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var n=a("2b0e"),r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("data-table",{attrs:{url:"api/class",title:"校区管理"}})],1)},o=[],i=a("1fdb"),s={name:"Home",components:{DataTable:i["a"]}},l=s,c=a("2877"),d=Object(c["a"])(l,r,o,!1,null,null,null),u=d.exports,f=a("a18c"),p=a("402c"),h=a("28dd");n["a"].config.productionTip=!1,n["a"].use(h["a"]),new n["a"]({router:f["a"],vuetify:p["a"],render:function(t){return t(u)}}).$mount("#app")},a18c:function(t,e,a){"use strict";var n=a("2b0e"),r=a("8c4f"),o=a("f9f2"),i=r["a"].prototype.push;r["a"].prototype.push=function(t){return i.call(this,t).catch((function(t){return t}))},n["a"].use(r["a"]);var s=[{path:"/",component:o["a"]}],l=new r["a"]({mode:"history",base:"/",routes:s});e["a"]=l},f9f2:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-card",{staticClass:"mx-auto mt-5",attrs:{width:"400"}},[a("v-card-title",[a("h1",{staticClass:"display-1"},[t._v("Login")])]),a("v-card-text",[a("v-text-field",{attrs:{label:"用户名"},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}}),a("v-text-field",{attrs:{type:"password",label:"密码"},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}})],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"success"},on:{click:t.click}},[t._v(" 登录")])],1)],1)],1)},r=[],o={name:"App",props:{},components:{},methods:{click:function(){window.console.log(this.username),this.$http.post("/api/login",{username:this.username,password:this.password},{emulateJSON:!0}).then((function(t){alert(t.data)}),(function(t){alert(t.status)}))}},data:function(){return{username:"",password:""}}},i=o,s=a("2877"),l=a("6544"),c=a.n(l),d=a("7496"),u=a("8336"),f=a("b0af"),p=a("99d9"),h=a("2fa4"),v=a("8654"),m=Object(s["a"])(i,n,r,!1,null,null,null);e["a"]=m.exports;c()(m,{VApp:d["a"],VBtn:u["a"],VCard:f["a"],VCardActions:p["a"],VCardText:p["b"],VCardTitle:p["c"],VSpacer:h["a"],VTextField:v["a"]})}});
//# sourceMappingURL=class.58c5bf0d.js.map