webpackJsonp([13,15],{302:function(t,e,s){var n=s(2)(s(386),s(332),null,null);t.exports=n.exports},332:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("hs-layout_auto",[s("div",{staticClass:"main-tabs"},[s("div",[s("table",[s("thead",[s("tr",[s("td",[t._v("name-名称")]),t._v(" "),s("td",[t._v("fullname-全名")]),t._v(" "),s("td",[t._v("color")]),t._v(" "),s("td",[t._v("url")]),t._v(" "),s("td",[t._v("_class")])])]),t._v(" "),s("tbody",t._l(t.res,function(e){return s("tr",[s("td",[t._v(t._s(e.name))]),t._v(" "),s("td",[t._v(t._s(e.fullname))]),t._v(" "),s("td",[t._v(t._s(e.color))]),t._v(" "),s("td",[t._v(t._s(e.url))]),t._v(" "),s("td",[t._v(t._s(e._class))])])}))])])])])},staticRenderFns:[]}},386:function(t,e){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{res:"999"}},activated:function(){this.getCaptcha()},methods:{getCaptcha:function(){var t=this;this.$http.get(this.jks_api+"get_all_job").then(function(e){console.log("this resp",e),t.res=e.data.data}).catch(function(e){t.res="error",console.log(t.res)})}}}}});
//# sourceMappingURL=13.29af490d846fbb26f4e2.js.map