(function(t){function e(e){for(var r,s,o=e[0],l=e[1],c=e[2],u=0,f=[];u<o.length;u++)s=o[u],Object.prototype.hasOwnProperty.call(n,s)&&n[s]&&f.push(n[s][0]),n[s]=0;for(r in l)Object.prototype.hasOwnProperty.call(l,r)&&(t[r]=l[r]);d&&d(e);while(f.length)f.shift()();return i.push.apply(i,c||[]),a()}function a(){for(var t,e=0;e<i.length;e++){for(var a=i[e],r=!0,o=1;o<a.length;o++){var l=a[o];0!==n[l]&&(r=!1)}r&&(i.splice(e--,1),t=s(s.s=a[0]))}return t}var r={},n={class:0},i=[];function s(e){if(r[e])return r[e].exports;var a=r[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,s),a.l=!0,a.exports}s.m=t,s.c=r,s.d=function(t,e,a){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},s.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(s.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var r in t)s.d(a,r,function(e){return t[e]}.bind(null,r));return a},s.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],l=o.push.bind(o);o.push=e,o=o.slice();for(var c=0;c<o.length;c++)e(o[c]);var d=l;i.push([4,"chunk-vendors"]),a()})({0:function(t,e){},"1fdb":function(t,e,a){"use strict";var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("v-app",[a("h1",{domProps:{textContent:t._s(t.title)}}),a("div",{staticClass:"my-dt",attrs:{id:"app"}},[a("v-data-table",{staticClass:"elevation-1",attrs:{headers:t.headers,items:t.tabledata,search:t.search,"custom-filter":t.customFilter,"sort-by":"calories","show-group-by":""},scopedSlots:t._u([{key:"top",fn:function(){return[a("v-toolbar",{attrs:{flat:"",color:"white"}},[a("v-select",{attrs:{items:t.filter_c,id:"myselect",dense:""},model:{value:t.filter_value,callback:function(e){t.filter_value=e},expression:"filter_value"}}),a("v-text-field",{attrs:{"append-icon":"mdi-magnify",label:"Search","single-line":"","hide-details":""},model:{value:t.search,callback:function(e){t.search=e},expression:"search"}}),a("v-spacer"),a("div",{domProps:{textContent:t._s(t.hint)}}),a("v-spacer"),t.insert?a("v-btn",{attrs:{color:"green"},on:{click:function(e){return t.newItem()}}},[t._v("新建项")]):t._e()],1)]},proxy:!0},{key:"item.actions",fn:function(e){var r=e.item;return[t.edit?a("v-icon",{staticClass:"mr-2",attrs:{small:""},on:{click:function(e){return t.editItem(r)}}},[t._v(" mdi-pencil ")]):t._e(),t.delete1?a("v-icon",{attrs:{small:""},on:{click:function(e){return t.deleteItem(r)}}},[t._v(" mdi-delete ")]):t._e()]}}])},[a("v-icon",{staticClass:"mr-2",attrs:{small:""}},[t._v(" mdi-pencil ")])],1)],1),a("div",{staticClass:"my-dialog",attrs:{id:"app"}},[a("v-dialog",{attrs:{"max-width":"500px"},model:{value:t.dialog,callback:function(e){t.dialog=e},expression:"dialog"}},[a("v-card",[a("v-card-title",[a("span",{staticClass:"headline"},[t._v(t._s(t.formTitle))])]),a("v-card-text",[a("v-card-container",t._l(this.formdata,(function(e){return a("div",{key:e.id},[a("v-row",[t.dataalter.hasOwnProperty(e["label"])?a("v-select",{attrs:{label:e["label"],items:t.alterkeys[e["label"]]},model:{value:e["data"],callback:function(a){t.$set(e,"data",a)},expression:"item['data']"}}):a("v-text-field",{attrs:{label:e["label"]},model:{value:e["data"],callback:function(a){t.$set(e,"data",a)},expression:"item['data']"}})],1)],1)})),0)],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"blue darken-1",text:""},on:{click:t.close}},[t._v("Cancel")]),a("v-btn",{attrs:{color:"blue darken-1",text:""},on:{click:t.save}},[t._v("Save")])],1)],1)],1)],1)])],1)},n=[],i=(a("c975"),a("b0c0"),a("b85c")),s={data:function(){return{dialog:!1,headers:[],tabledata:[],search:"",mode:"",editedItem:[],defaultItem:{},formdata:[],currentid:"",hint:"",datatype:{},dataalter:{},alterkeys:{},need_update:!1,filter_value:"",filter_c:[]}},props:{url:{type:String,required:!0},title:{type:String,required:!0},delete1:{type:Boolean,default:!0},insert:{type:Boolean,default:!0},edit:{type:Boolean,default:!0}},computed:{formTitle:function(){return"insert"==this.mode?"新建":"edit"==this.mode?"修改":"unknown action"}},created:function(){this.data_update()},methods:{customFilter:function(t,e,a){if(window.console.log(JSON.stringify(t)),window.console.log(JSON.stringify(e)),window.console.log(JSON.stringify(a)),window.console.log(a),a.hasOwnProperty(this.filter_value))return-1!=a[this.filter_value].toLowerCase().indexOf(e.toLowerCase());for(var r in a)if(-1==a[r].toLowerCase().indexOf(e.toLowerCase()))return!1;return!0},newItem:function(){this.formdata=[];var t,e=Object(i["a"])(this.headers);try{for(e.s();!(t=e.n()).done;){var a=t.value;"actions"!=a["value"]&&"auto"!=this.datatype[a["value"]]&&this.formdata.push({label:a["value"],data:""})}}catch(r){e.e(r)}finally{e.f()}this.mode="insert",this.dialog=!0},editItem:function(t){for(var e in this.formdata=[],this.editedItem)this.formdata.push({label:e,data:t[e]});this.mode="edit",this.currentid=t["id"],this.dialog=!0},deleteItem:function(t){1==confirm("你真的要删除这一项吗?")&&this.$http.post(this.$props.url,JSON.stringify({method:"DELETE",id:t["id"]})).then((function(t){var e=t.body;this.hint=e["message"],this.data_update()}),(function(t){alert(t.status)}))},close:function(){this.dialog=!1},save:function(){if("edit"==this.mode||"insert"==this.mode){var t,e={},a=this.dataalter,r=Object(i["a"])(this.formdata);try{for(r.s();!(t=r.n()).done;){var n=t.value;a.hasOwnProperty(n["label"])?e[n["label"]]=a[n["label"]][n["data"]]:e[n["label"]]=n["data"]}}catch(s){r.e(s)}finally{r.f()}"edit"==this.mode&&(e["id"]=this.currentid,e["method"]="EDIT"),"insert"==this.mode&&(e["method"]="INSERT"),this.$http.post(this.$props.url,JSON.stringify(e)).then((function(t){var e=t.body;this.hint=e["message"],this.data_update()}),(function(t){alert(t.status)})),need_update=!0}this.close()},data_update:function(){this.$http.post(this.$props.url,JSON.stringify({method:"FORMAT"})).then((function(t){var e=t.body,a=e["code"];if(this.datatype={},this.dataalter={},this.filter_c=["All"],"fail"!=a){if("success"==a){this.editedItem={},this.headers=[];var r,n=Object(i["a"])(e["format"]);try{for(n.s();!(r=n.n()).done;){var s=r.value,o={},l=s["name"];if("false"==s["read_only"]&&(this.editedItem[l]=""),o["text"]=l,o["value"]=l,o["align"]="center",this.datatype[l]=s["type"],this.headers.push(o),this.filter_c.push(l),s.hasOwnProperty("alter")){var c={};for(var d in s["alter"])c[s["alter"][d]]=d;this.dataalter[l]=c;var u=[];for(var d in s["alter"])u.push(s["alter"][d]);this.alterkeys[l]=u}}}catch(f){n.e(f)}finally{n.f()}(this.$props.edit||this.$props.delete1)&&this.headers.push({text:"Actions",value:"actions",sortable:!1,align:"center"})}}else this.hint=e["message"]}),(function(t){alert(t.status)})),this.$http.post(this.$props.url,JSON.stringify({method:"ALL"})).then((function(t){var e=t.body,a=e["code"];"fail"!=a?"success"==a&&(this.tabledata=e["data"]):this.hint=e["message"]}),(function(t){alert(t.status)})),window.vue=this}}},o=s,l=(a("6224"),a("2877")),c=a("6544"),d=a.n(c),u=a("7496"),f=a("8336"),p=a("b0af"),h=a("99d9"),v=a("8fea"),m=a("169a"),b=a("132d"),y=a("0fd9"),g=a("b974"),w=a("2fa4"),_=a("8654"),x=a("71d9"),O=Object(l["a"])(o,r,n,!1,null,null,null);e["a"]=O.exports;d()(O,{VApp:u["a"],VBtn:f["a"],VCard:p["a"],VCardActions:h["a"],VCardText:h["b"],VCardTitle:h["c"],VDataTable:v["a"],VDialog:m["a"],VIcon:b["a"],VRow:y["a"],VSelect:g["a"],VSpacer:w["a"],VTextField:_["a"],VToolbar:x["a"]})},"223b":function(t,e,a){},4:function(t,e,a){t.exports=a("95edb")},"402c":function(t,e,a){"use strict";var r=a("2b0e"),n=a("f309");r["a"].use(n["a"]),e["a"]=new n["a"]({})},5974:function(t,e,a){},6224:function(t,e,a){"use strict";var r=a("5974"),n=a.n(r);n.a},"95edb":function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var r=a("2b0e"),n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("nav-bar"),a("data-table",{attrs:{url:"api/class",title:"班级管理"}})],1)},i=[],s=a("1fdb"),o=a("d000"),l={name:"Home",components:{DataTable:s["a"],NavBar:o["a"]}},c=l,d=a("2877"),u=Object(d["a"])(c,n,i,!1,null,null,null),f=u.exports,p=a("a18c"),h=a("402c"),v=a("28dd");r["a"].config.productionTip=!1,r["a"].use(v["a"]),new r["a"]({router:p["a"],vuetify:h["a"],render:function(t){return t(f)}}).$mount("#app")},a18c:function(t,e,a){"use strict";var r=a("2b0e"),n=a("8c4f"),i=a("f9f2"),s=n["a"].prototype.push;n["a"].prototype.push=function(t){return s.call(this,t).catch((function(t){return t}))},r["a"].use(n["a"]);var o=[{path:"/",component:i["a"]}],l=new n["a"]({mode:"history",base:"/",routes:o});e["a"]=l},d000:function(t,e,a){"use strict";var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("nav",[a("v-toolbar",{attrs:{color:"blue",dark:""}},[a("v-spacer"),t._l(t.items,(function(e,r){return a("v-list-item",{key:r},[a("v-list-item-content",[a("a",{attrs:{href:t.serverurl+e.route}},[a("v-list-item-title",{domProps:{textContent:t._s(e.text)}})],1)])],1)})),a("v-spacer"),a("v-btn",{attrs:{color:"blue"},on:{click:function(e){return t.logout()}}},[t._v(" 登出 ")])],2)],1)])},n=[],i={data:function(){return{drawer:!0,item:1,serverurl:"http://localhost:8000",items:[{text:"学区管理",route:"/campus"},{text:"专业管理",route:"/major"},{text:"班级管理",route:"/class"},{text:"学生管理",route:"/student"},{text:"教师管理",route:"/teacher"},{text:"学籍异动管理",route:"/unnormal_change"},{text:"课程管理",route:"/manage_course"}]}},methods:{logout:function(){window.console.log("22"),window.console.log("logout"),this.$http.post("api/logout",JSON.stringify({})).then((function(t){window.location.href="/login"}),(function(t){alert(t.status)}))}}},s=i,o=(a("d668"),a("2877")),l=a("6544"),c=a.n(l),d=a("8336"),u=a("da13"),f=a("5d23"),p=a("2fa4"),h=a("71d9"),v=Object(o["a"])(s,r,n,!1,null,"b7efed1e",null);e["a"]=v.exports;c()(v,{VBtn:d["a"],VListItem:u["a"],VListItemContent:f["a"],VListItemTitle:f["b"],VSpacer:p["a"],VToolbar:h["a"]})},d668:function(t,e,a){"use strict";var r=a("223b"),n=a.n(r);n.a},f9f2:function(t,e,a){"use strict";var r=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",[a("v-card",{staticClass:"mx-auto mt-5",attrs:{width:"400"}},[a("v-card-title",[a("h1",{staticClass:"display-1"},[t._v("Login")])]),a("v-card-text",[a("v-text-field",{attrs:{label:"用户名"},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}}),a("v-text-field",{attrs:{type:"password",label:"密码"},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}})],1),a("v-card-actions",[a("v-spacer"),a("v-btn",{attrs:{color:"success"},on:{click:t.click}},[t._v(" 登录")])],1)],1)],1)},n=[],i={name:"App",props:{},components:{},methods:{click:function(){window.console.log(this.username),this.$http.post("api/login",JSON.stringify({username:this.username,password:this.password})).then((function(t){var e=t.body;"success"==e["code"]?window.location.href=e["addr"]:alert(e["message"])}),(function(t){alert(t.status)}))}},data:function(){return{username:"",password:""}}},s=i,o=a("2877"),l=a("6544"),c=a.n(l),d=a("7496"),u=a("8336"),f=a("b0af"),p=a("99d9"),h=a("2fa4"),v=a("8654"),m=Object(o["a"])(s,r,n,!1,null,null,null);e["a"]=m.exports;c()(m,{VApp:d["a"],VBtn:u["a"],VCard:f["a"],VCardActions:p["a"],VCardText:p["b"],VCardTitle:p["c"],VSpacer:h["a"],VTextField:v["a"]})}});
//# sourceMappingURL=class.3310ad1b.js.map