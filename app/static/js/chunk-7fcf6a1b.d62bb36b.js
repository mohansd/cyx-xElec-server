(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-7fcf6a1b"],{9318:function(e,t,r){},"9d15":function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"container"},[r("div",{staticClass:"header"},[r("div",{staticClass:"title"},[e._v("编辑用户")]),r("div",{staticClass:"back",on:{click:e.hanleHide}},[r("fa-icon",{attrs:{"icon-name":"undo"}}),e._v("\n      返回\n    ")],1)]),r("el-divider"),r("div",{staticClass:"wrap"},[r("el-row",[r("el-col",{attrs:{lg:16,md:20,sm:24,xs:24}},[r("el-form",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"editForm",attrs:{model:e.form,"status-icon":"","label-width":"100px"},nativeOn:{submit:function(e){e.preventDefault()}}},[r("el-form-item",{attrs:{label:"用户权限",prop:"auth"}},[r("el-select",{attrs:{placeholder:"请选择"},model:{value:e.form.auth,callback:function(t){e.$set(e.form,"auth",t)},expression:"form.auth"}},e._l(4,(function(e){return r("el-option",{key:e,attrs:{label:e,value:e}})})),1)],1),r("el-form-item",{attrs:{label:"用户名",prop:"username"}},[r("el-input",{attrs:{size:"medium",placeholder:"请填写用户名"},model:{value:e.form.username,callback:function(t){e.$set(e.form,"username",t)},expression:"form.username"}})],1),r("el-form-item",{attrs:{label:"密码",prop:"password"}},[r("el-input",{attrs:{size:"medium",placeholder:"请填写密码"},model:{value:e.form.password,callback:function(t){e.$set(e.form,"password",t)},expression:"form.password"}})],1),r("el-form-item",{attrs:{label:"真实姓名",prop:"realname"}},[r("el-input",{attrs:{size:"medium",placeholder:"请填写真实姓名"},model:{value:e.form.realname,callback:function(t){e.$set(e.form,"realname",t)},expression:"form.realname"}})],1),r("el-form-item",{attrs:{label:"手机号",prop:"mobile"}},[r("el-input",{attrs:{size:"medium",placeholder:"请填写手机号"},model:{value:e.form.mobile,callback:function(t){e.$set(e.form,"mobile",t)},expression:"form.mobile"}})],1),r("el-form-item",{attrs:{label:"邮箱",prop:"email"}},[r("el-input",{attrs:{size:"medium",placeholder:"请填写邮箱"},model:{value:e.form.email,callback:function(t){e.$set(e.form,"email",t)},expression:"form.email"}})],1),r("el-form-item",{staticClass:"submit"},[r("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.submitForm("editForm")}}},[e._v("保 存")]),r("el-button",{on:{click:function(t){return e.resetForm("editForm")}}},[e._v("重 置")])],1)],1)],1)],1)],1)],1)},n=[],i=(r("96cf"),r("3b8d")),o=r("8654"),s={name:"UserAdd",components:{},props:{editID:{type:String,default:""}},data:function(){return{loading:!1,form:{auth:1,username:"",realname:"",mobile:"",email:"",company_id:"",password:""}}},computed:{},created:function(){},mounted:function(){this.getUserInfo()},methods:{getUserInfo:function(){var e=Object(i["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,o["a"].getUserInfo(this.editID);case 2:this.form=e.sent;case 3:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),hanleHide:function(){this.$emit("hanleHide",!1)},submitForm:function(){var e=Object(i["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,o["a"].editOne(this.editID,this.form);case 2:this.$message.success("修改用户信息成功"),this.hanleHide();case 4:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),resetForm:function(e){this.getUserInfo()}}},l=s,m=(r("fd79"),r("2877")),u=Object(m["a"])(l,a,n,!1,null,"e0364b18",null);t["default"]=u.exports},fd79:function(e,t,r){"use strict";var a=r("9318"),n=r.n(a);n.a}}]);
//# sourceMappingURL=chunk-7fcf6a1b.d62bb36b.js.map