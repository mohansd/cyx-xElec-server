(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-162a5930"],{"12eb":function(t,e,n){},"1ae4":function(t,e,n){},"20d6":function(t,e,n){"use strict";var r=n("5ca1"),a=n("0a49")(6),i="findIndex",s=!0;i in[]&&Array(1)[i]((function(){s=!1})),r(r.P+r.F*s,"Array",{findIndex:function(t){return a(this,t,arguments.length>1?arguments[1]:void 0)}}),n("9c6c")(i)},"21f9":function(t,e,n){},"59a6":function(t,e,n){"use strict";var r=n("21f9"),a=n.n(r);a.a},"61d9":function(t,e,n){"use strict";n.r(e);var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticStyle:{height:"100%"}},[n("el-container",[n("el-header",{staticClass:"header"},[n("NavBar")],1),n("el-container",[n("el-aside",{staticClass:"aside",attrs:{width:t.sidebarWidth}},[n("SideBar")],1),n("div",{staticClass:"icon-font side-btn",style:{left:t.sidebarWidth},on:{click:t.toggleSlidebarState}},[n("i",{staticClass:"el-icon-caret-left",class:{rotate:t.foldState}})]),n("el-main",{staticClass:"main"},[t.isVisible?n("HistoryTag"):t._e(),n("AppMain")],1)],1)],1)],1)},a=[],i=(n("8e6e"),n("ac6a"),n("456d"),n("bd86")),s=n("2f62"),o=n("b61b"),c=n("f121"),l=n("2158"),u=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("section",{staticClass:"wrapper"},[n("div",{staticClass:"container"},[n("transition",{attrs:{name:"fade",mode:"out-in"}},[n("keep-alive",[n("router-view")],1)],1)],1)])},f=[],d=n("53fb"),p={name:"AppMain",components:{LayoutSetting:d["a"]},data:function(){return{drawer:!0}},computed:{},methods:{}},h=p,m=(n("59a6"),n("2877")),b=Object(m["a"])(h,u,f,!1,null,"1370e445",null),g=b.exports,v=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("nav",{staticClass:"nav-bar"},[r("div",{staticClass:"left-menu"},[r("router-link",{staticClass:"logo",attrs:{to:"/"}},[r("img",{staticClass:"icon",attrs:{src:n("bbd0"),alt:""}}),r("img",{staticClass:"name",attrs:{src:n("2a3b"),alt:""}})])],1),r("div",{staticClass:"right-menu"},[r("Screenfull",{staticStyle:{"margin-right":"15px"}}),r("UserCard",{staticStyle:{"margin-right":"10px"}})],1)])},O=[],y=n("19ba"),j=n("f27a");function w(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,r)}return n}function S(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?w(Object(n),!0).forEach((function(e){Object(i["a"])(t,e,n[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):w(Object(n)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))}))}return t}var C={name:"NavBar",components:{Screenfull:y["a"],UserCard:j["a"]},data:function(){return{}},computed:S({},Object(s["c"])(["sidebar"]),{foldState:function(){return this.sidebar.closed}}),created:function(){},mounted:function(){},methods:{toggleSlidebarState:function(){this.$store.commit("app/TOGGLE_SIDEBAR")}}},_=C,P=(n("983e"),Object(m["a"])(_,v,O,!1,null,"7d9a60b8",null)),x=P.exports,k=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"sidebar"},[n("el-menu",{staticStyle:{"margin-bottom":"50px"},attrs:{"default-active":t.defaultActive,collapse:t.isCollapse},on:{open:t.handleOpen,close:t.handleClose}},[t._l(t.routes,(function(e){return[t.canUnflod(e)?n("el-submenu",{key:e.name,attrs:{index:e.name}},[n("template",{slot:"title"},[n("i",{class:e.meta.icon}),n("span",[t._v(t._s(e.meta.title))])]),t._l(e.children,(function(e){return[e.children?n("el-submenu",{key:e.name,attrs:{index:e.name}},[n("template",{slot:"title"},[n("i",{class:e.meta.icon}),n("span",[t._v(t._s(e.meta.title))])]),t._l(e.children,(function(e){return n("router-link",{key:e.name,staticClass:"icon-menu",attrs:{to:e.path}},[n("el-menu-item",{attrs:{index:e.name}},[n("span",[t._v(t._s(e.meta.title))])])],1)}))],2):n("router-link",{key:e.name,staticClass:"icon-menu",attrs:{to:e.path}},[n("el-menu-item",{attrs:{index:e.name}},[n("span",[t._v(t._s(e.meta.title))])])],1)]}))],2):n("router-link",{key:e.name,attrs:{to:t.defaultRoute(e).path}},[n("el-menu-item",{attrs:{index:t.defaultRoute(e).name}},[n("i",{class:e.meta.icon}),n("span",{attrs:{slot:"title"},slot:"title"},[t._v(t._s(e.meta.title))])])],1)]}))],2)],1)},$=[],D=(n("7f7f"),n("2ef0"));function T(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,r)}return n}function E(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?T(Object(n),!0).forEach((function(e){Object(i["a"])(t,e,n[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):T(Object(n)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))}))}return t}var A={name:"SideBar",components:{},data:function(){return{}},computed:E({},Object(s["c"])(["sidebar"]),{routes:function(){var t=this.$router.options.routes,e=t.filter((function(t){return!0!==t.hidden}));return Object(D["flatten"])(e)},isCollapse:function(){return this.sidebar.closed},defaultActive:function(){return this.$route.name}}),created:function(){},mounted:function(){},methods:{defaultRoute:function(t){return t.children[0]},canUnflod:function(t){return!(t.children&&1===t.children.length&&!t.children.children)},handleOpen:function(t,e){},handleClose:function(t,e){},_testRouterAttrs:function(){console.log("$router:",this.$router),console.log("所有路由(含嵌套子路由):",this.$router.options.routes),console.log("$route:",this.$route),console.log("当前页面的name:",this.$route.name)}}},B=A,I=(n("e656"),Object(m["a"])(B,k,$,!1,null,"5ada4986",null)),W=I.exports;function L(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,r)}return n}function R(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?L(Object(n),!0).forEach((function(e){Object(i["a"])(t,e,n[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):L(Object(n)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))}))}return t}var G={name:"TTypeLayout",components:{AppMain:g,SideBar:W,NavBar:x,HistoryTag:o["a"]},mixins:[l["a"]],computed:R({},Object(s["c"])(["sidebar"]),{},Object(s["c"])({isVisible:"app/historyTagState"}),{foldState:function(){return this.sidebar.closed},isCollapse:function(){return this.sidebar.closed},sidebarWidth:function(){var t=c["a"].layout.sidebar,e=t.minWidth,n=t.maxWidth;return!1===this.isCollapse?n:e}}),mounted:function(){},methods:{toggleSlidebarState:function(){this.$store.commit("app/TOGGLE_SIDEBAR")}}},U=G,H=(n("d224"),Object(m["a"])(U,r,a,!1,null,"8425f11c",null));e["default"]=H.exports},7979:function(t,e,n){"use strict";var r=n("1ae4"),a=n.n(r);a.a},"8e88":function(t,e,n){},"983e":function(t,e,n){"use strict";var r=n("8e88"),a=n.n(r);a.a},b61b:function(t,e,n){"use strict";var r=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{ref:"scrollContainer",staticClass:"history-tag",on:{wheel:function(e){return e.preventDefault(),t.handleScroll(e)}}},[n("div",{staticClass:"router-box",style:{width:130*t.tags.length+"px"}},t._l(t.tags,(function(e){return n("router-link",{key:e.path,staticClass:"tag-item",class:t.isActive(e)?"active":"",attrs:{to:e.path},nativeOn:{click:function(e){return t.checkoutTag(e)}}},[n("span",{staticClass:"name"},[t._v(t._s(e.name))]),e.affix?t._e():n("span",{staticClass:"el-icon-close icon",on:{click:function(n){return n.preventDefault(),n.stopPropagation(),t.closeSelectedTag(e)}}})])})),1)])},a=[],i=(n("7f7f"),n("20d6"),{name:"HistoryTag",components:{},data:function(){return{tags:[]}},computed:{scrollWrapper:function(){return this.$refs.scrollContainer}},watch:{$route:function(t,e){this.tags;this.addTag()}},created:function(){},mounted:function(){this.addTag()},methods:{handleScroll:function(t){var e=t.wheelDelta||40*-t.deltaY,n=this.scrollWrapper;n.scrollLeft+=e/4},isActive:function(t){return t.path===this.$route.path},isInTags:function(t){var e=this.tags.findIndex((function(e){return e.path===t.path}));if(e<0)return!1;var n=this.scrollWrapper;return n.scrollLeft=100*e,!0},addTag:function(){var t=this.isInTags,e=this.tags,n=this.$route,r=(n.name,n.meta),a=r.title,i=r.affix,s=n.path,o={name:a,path:s,affix:i};t(o)||e.push(o)},closeSelectedTag:function(t){var e=this.tags,n=e.findIndex((function(e){return e.path===t.path}));if(e.splice(n,1),n===e.length&&this.isActive(t)||this.isActive(t)){var r=this.tags[n-1].path;this.$router.push(r)}},checkoutTag:function(){}}}),s=i,o=(n("7979"),n("2877")),c=Object(o["a"])(s,r,a,!1,null,"3c685302",null);e["a"]=c.exports},d224:function(t,e,n){"use strict";var r=n("f9e2"),a=n.n(r);a.a},e656:function(t,e,n){"use strict";var r=n("12eb"),a=n.n(r);a.a},f9e2:function(t,e,n){}}]);
//# sourceMappingURL=chunk-162a5930.c7d92189.js.map