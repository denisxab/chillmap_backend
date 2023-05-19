(function(){"use strict";var e={9014:function(e,t,a){var o=a(9242),i=a(3396);function n(e,t,a,o,n,s){const r=(0,i.up)("router-view");return(0,i.wg)(),(0,i.j4)(r)}var s={},r=a(89);const l=(0,r.Z)(s,[["render",n]]);var c,d,_,p,m,u,h=l,v=a(65);a(7658);function g(e){return e.replace("@/",ENV_default_host_to_src)}function w(e){return e.replace("@/",ENV_default_host_to_backend)}async function k(e){const t=await fetch(e,{method:"GET"});return{data:await t.json(),ok:t.ok,status:t.status}}async function y(e,t){const a=await fetch(e,{method:"POST",body:JSON.stringify(t),headers:{"Content-Type":"application/json; charset=utf-8",Accept:"application/json"}});return{data:await a.text(),ok:a.ok,status:a.status}}function f(e){if(Array.isArray(e))return e.map(f);if(e&&"object"===typeof e){const t={};for(const a in e)t[a]=f(e[a]);return t}return e}function C(e){let t=[];return e.what_todo_obj.forEach((e=>{t.push(e.todo)})),t}async function M(e,t){const a=await k(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${e}&lon=${t}`);if(a.ok)return a.data.display_name;console.error(`Ошибка при получении адреса по координатам: ${e} ${t}`)}(function(e){e["main_map"]="mm"})(c||(c={})),function(e){e["latitude"]="x",e["longitude"]="y",e["zoom"]="z",e["type_view"]="v",e["channel"]="c",e["mark"]="m"}(d||(d={})),function(e){e["StaticWorkSchedule"]="Постоянный график работы",e["OneTimeTemporaryEvent"]="Одноразовое временно событие",e["PeriodicPlace"]="Переодическое место"}(_||(_={})),function(e){e["UncomfortableFrequentCrowding"]="Дискомфортная частая людность",e["UncomfortableFrequentCrowdingExceptWeekends"]="Дискомфортная людность по выходным и праздникам, но в рабочие дни комфортная",e["ComfortableCrowd"]="Комфортная людность",e["Privacy"]="Уединение",e["Loneliness"]="Одиночество"}(p||(p={})),function(e){e["Monday"]="понедельник",e["Tuesday"]="вторник",e["Wednesday"]="среда",e["Thursday"]="четверг",e["Friday"]="пятница",e["Saturday"]="суббота",e["Sunday"]="воскресенье"}(m||(m={})),function(e){e["RUB"]="руб",e["USD"]="доллар",e["EUR"]="евро",e["CNY"]="юань"}(u||(u={}));const b={state(){return{geomap_json:{},settings_type_place:{},select_PropertiesMark:void 0,coordinat_click:{},select_zoom:16,type_view:c.main_map,select_channel_geomap:void 0,url_geomap:void 0,RefMapContainer:void 0}},mutations:{AUpdate_select_channel(e,t){e.select_channel_geomap=t},Update_select_zoom(e,t){e.select_zoom=t},AUpdate_coordinat_click(e,t){e.coordinat_click=t},AUpdate_type_view(e,t){e.type_view=t},Update_geomap_json(e,t){e.geomap_json=t},Update_settings_type_place(e,t){e.settings_type_place=t},AUpdate_select_PropertiesMark(e,t){e.select_PropertiesMark=t},Update_url_geomap(e,t){e.url_geomap=g(t)},Update_RefMapContainer(e,t){e.RefMapContainer=t}},getters:{coordinat_click_cord:e=>{const t=e.coordinat_click;return t?[t.latitude,t.longitude]:[]}},actions:{Update_coordinat_click({state:e,commit:t},{coord:a,router:o,route:i}){t("AUpdate_coordinat_click",a);let n=f(i.query);n[d.latitude]=a.latitude,n[d.longitude]=a.longitude,n[d.zoom]=e.select_zoom,n[d.type_view]=c.main_map,e.select_PropertiesMark&&(n[d.mark]=e.select_PropertiesMark.id),o.push({query:n})},Update_type_view({commit:e},{type_view:t,router:a,route:o}){e("AUpdate_type_view",t);let i=f(o.query);i[d.type_view]=t,a.push({query:i})},Update_select_channel({commit:e},{channel:t,router:a,route:o}){e("AUpdate_select_channel",t);let i=f(o.query);i[d.channel]=t,a.push({query:i})},Update_select_PropertiesMark({commit:e},{mark:t,router:a,route:o}){e("AUpdate_select_PropertiesMark",t);let i=f(o.query);i[d.mark]=t.id,a.push({query:i})}},namespaced:!0};var x=a(2483);const P={id:"main_box"},U={class:"over_box"},F={class:"up_box"},$={class:"down_box"},O={ref:"d_show_map_detail",class:"d_show_map_detail"},D={class:"map_coord_click"},z=["value"],S={class:"map_facile_div"};function Z(e,t,a,n,s,r){const l=(0,i.up)("OverBox"),c=(0,i.up)("MapContainer"),d=(0,i.up)("FacileFromMarker");return(0,i.wg)(),(0,i.iD)("div",P,[(0,i.wy)((0,i._)("div",U,[(0,i.Wm)(l,{onHidden_over_box:r.hidden_over_box,view_component:s.view_component},null,8,["onHidden_over_box","view_component"])],512),[[o.F8,s.view_component]]),(0,i._)("div",F,[(0,i.Wm)(c,{ref:"MapContainer",onOnMarkerClick:r.HandleMarkerClick,onOnEmptyMapClick:r.HandleEmptyMapClick},null,8,["onOnMarkerClick","onOnEmptyMapClick"])]),(0,i._)("div",$,[(0,i._)("div",O,[(0,i.wy)((0,i._)("input",{class:"show_map_detail",type:"image",ref:"show_map_detail",onClick:t[0]||(t[0]=(...e)=>r.ShowExtraFeaturesWindow&&r.ShowExtraFeaturesWindow(...e))},null,512),[[o.F8,s.is_show_map_detail]]),(0,i.wy)((0,i._)("input",{class:"show_map_detail",type:"image",ref:"show_map_detail_place",onClick:t[1]||(t[1]=(...e)=>r.ShowPlaceDetailsInfo&&r.ShowPlaceDetailsInfo(...e))},null,512),[[o.F8,!s.is_show_map_detail]])],512),(0,i._)("div",D,[(0,i._)("input",{type:"text",value:e.coordinat_click_cord,id:"map_coord_click_input",placeholder:"широта,долгота",readonly:""},null,8,z)]),(0,i.wy)((0,i._)("div",S,[(0,i.Wm)(d,{ref:"map_facile"},null,512)],512),[[o.F8,s.is_show_FacileFromMarker]])])])}const I={style:{width:"100%",height:"100%"}},H={ref:"map-root",style:{width:"100%",height:"100%"}};function j(e,t,a,o,n,s){return(0,i.wg)(),(0,i.iD)("div",I,[(0,i._)("div",H,null,512)])}var E=a(7793),A=a(3725),B=a(4109),L=a(7253),q=a(9177),W=(a(1827),a(2949)),V=a(3292),N=a(9513),R=a(1508),T=a(4693),G=a(7983),Y=a(6205),K=a(2093),J=a(9966);const Q=g("@/img/default_point.png"),X=g("@/img/select.png");var ee={emits:["onMarkerClick","onEmptyMapClick"],data(){return{map:void 0,mainLayer:new B.Z({className:"mainLayer",source:new L.Z,preload:4,visible:!0}),selectLayer:new N.Z({className:"selectLayer",source:new V.Z,style:new T.ZP({image:new Y.Z({src:X,scale:(0,K.Pq)([.4,.4])})}),visible:!0}),markersLayer:new N.Z({className:"markersLayer",source:new V.Z,style:new T.ZP({image:new Y.Z({src:Q,scale:(0,K.Pq)([.3,.3])})}),visible:!0}),coordinat_click_obj_mark:void 0}},methods:{...(0,v.OI)("geomap",["Update_select_zoom","Update_geomap_json","Update_settings_type_place"]),...(0,v.nv)("geomap",["Update_coordinat_click","Update_select_PropertiesMark","Update_coordinat_click"]),_initMap(e,t,a){this.map=new A.Z({target:this.$refs["map-root"],layers:[this.mainLayer,this.selectLayer],view:new E.ZP({zoom:t,center:(0,q.mi)([e.longitude,e.latitude]),constrainResolution:!0,projection:"EPSG:3857"})}),this.setSelectMarker(e),this.map.addLayer(this.markersLayer),this.map.on("click",this.HandleClickMap),this.map.on("pointermove",this.HandlePointermove),this.map.on("moveend",this.HandleZoom),this.updateSelectGeomap(a)},ZoomMap(){this.Update_select_zoom(this.select_zoom+1)},UnZoomMap(){this.Update_select_zoom(this.select_zoom-1)},setCoordinates(e,t=!1){e&&(this.view_select.setCenter((0,q.mi)([e.longitude,e.latitude])),t&&this.setSelectMarker(e))},setMarkers(e,t=void 0,{imgUrl:a,imgSize:o=[1,1],labelText:i="12:Пивная"}={}){if(e){let n=new R.Z({geometry:new W.Z((0,q.mi)([e.longitude,e.latitude]))});a&&n.setStyle(new T.ZP({image:new Y.Z({src:a,scale:(0,K.Pq)(o)}),text:new G.Z({text:i,scale:[1.3,1.3],offsetY:28,stroke:new J.Z({color:"#fff",width:3}),placement:"line"})})),t&&n.setProperties(t),this.markersLayer.getSource().addFeature(n)}},_setMarkersFromGeomap(e){const t=this.settings_type_place,a=t[e.type_place],o={imgUrl:g(a.img_url),imgSize:[a.img_size_w,a.img_size_h]};o["labelText"]=`${e.rating%13}:${e.simpl_name.substring(0,16)}`;const i=this.RefMapContainer._parseCoordFromOpenstreetmap(`${e.cord_x},${e.cord_y}`);let n=e;n["name_marker"]=a.name,n["coord"]=[i.latitude,i.longitude],this.setMarkers(i,n,o)},setSelectMarker(e){if(e){this.selectLayer.getSource().removeFeature(this.coordinat_click_obj_mark);var t=new R.Z(new W.Z((0,q.mi)([e.longitude,e.latitude])));this.coordinat_click_obj_mark=t,this.selectLayer.getSource().addFeature(t)}},async updateSelectGeomap(e){const t=await k(e);if(t.ok){const e=t.data;this.ClearMarkers(this.markersLayer),this.Update_geomap_json(e),this.ShowPlaceFromExternal(this.markersLayer,this.geomap_json)}else console.error("Ошибка: Ответ geomap пустой")},ClearMarkers(e){e.getSource().clear()},ShowPlaceFromExternal(e,t){e.setVisible(!0);const a=t.places.settings;this.Update_settings_type_place(a);
//! Перебрать места и отобразить их на месте
for(let o in t.places.place)t.places.place[o].forEach((e=>{this._setMarkersFromGeomap(e)}))},_CheckIntersectionsMarker(e){let t=!1;return this.map.forEachFeatureAtPixel(e.pixel,((a,o)=>{"markersLayer"==o.getClassName()&&(this.HandleMarkerHover(e,a),t=!0)})),t},HandleClickMap(e){if(this._CheckIntersectionsMarker(e))return null;const t=(0,q.vs)(e.coordinate,"EPSG:3857","EPSG:4326").reverse();this.Update_coordinat_click({coord:{latitude:t[0],longitude:t[1]},router:this.$router,route:this.$route}),t&&this.setSelectMarker(this._parseCoordFromOpenstreetmap(t.toString())),console.log("Нажатие по карте, в координаты: ",t),this.$emit("onEmptyMapClick",e)},HandlePointermove(e){this._CheckIntersectionsMarker(e)},HandleMarkerHover(e,t){"pointermove"==e.type&&console.debug("Наведение на маркер"),"click"==e.type&&this.HandleMarkerClick(t)},HandleMarkerClick(e){const t=e.getProperties();this.Update_select_PropertiesMark({mark:t,router:this.$router,route:this.$route}),this.Update_coordinat_click({coord:{latitude:t.coord[0],longitude:t.coord[1]},router:this.$router,route:this.$route}),console.log("Нажатие на маркер",t),this.$emit("onMarkerClick",t)},HandleZoom(e){this.Update_select_zoom(this.view_select.values_.zoom)},_parseCoordFromOpenstreetmap(e){if(""!=e){const t=e.split(",").reverse();if(2==t.length)return{longitude:parseFloat(t[0]),latitude:parseFloat(t[1])}}else console.warn("Вы не указали координаты")}},computed:{view_select(){return this.map.getView()},layers_select(){return this.map.getLayers()},...(0,v.rn)("geomap",["select_zoom","settings_type_place","RefMapContainer","geomap_json"]),...(0,v.Se)("geomap",["coordinat_click_cord"])}};const te=(0,r.Z)(ee,[["render",j]]);var ae=te,oe=a(7139);const ie={class:"map_facile"},ne={class:"cel name_marker"},se={class:"img"},re={ref:"img_name_marker"},le={class:"text"},ce={class:"cel simpl_name"},de={class:"img"},_e={ref:"img_simpl_name"},pe={class:"text"},me={class:"cel rating"},ue={class:"img"},he={ref:"img_rating"},ve={class:"text"},ge={class:"cel address"},we={class:"img"},ke={ref:"img_address"},ye={class:"text"},fe={class:"cel"};function Ce(e,t,a,o,n,s){const r=(0,i.up)("ParamsList");return(0,i.wg)(),(0,i.iD)("div",ie,[(0,i._)("div",ne,[(0,i._)("div",se,[(0,i._)("img",re,null,512)]),(0,i._)("div",le,(0,oe.zw)(n.name_marker),1)]),(0,i._)("div",ce,[(0,i._)("div",de,[(0,i._)("img",_e,null,512)]),(0,i._)("div",pe,(0,oe.zw)(n.simpl_name),1)]),(0,i._)("div",me,[(0,i._)("div",ue,[(0,i._)("img",he,null,512)]),(0,i._)("div",ve,(0,oe.zw)(n.rating),1)]),(0,i._)("div",ge,[(0,i._)("div",we,[(0,i._)("img",ke,null,512)]),(0,i._)("div",ye,(0,oe.zw)(n.address),1)]),(0,i._)("div",fe,[n.whattodo&&n.whattodo.length>0?((0,i.wg)(),(0,i.j4)(r,{key:0,params_list:n.whattodo},null,8,["params_list"])):(0,i.kq)("",!0)])])}const Me={class:"params_list"},be=["href"],xe={key:1};function Pe(e,t,a,o,n,s){return(0,i.wg)(),(0,i.iD)("div",Me,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(a.params_list,((e,t)=>((0,i.wg)(),(0,i.iD)("div",{class:"li_h",key:t},["string"==typeof e&&e.includes("://")?((0,i.wg)(),(0,i.iD)("a",{key:0,target:"_blank",href:e},(0,oe.zw)(e),9,be)):((0,i.wg)(),(0,i.iD)("span",xe,(0,oe.zw)(e),1))])))),128))])}var Ue={props:{params_list:{type:Object}}};const Fe=(0,r.Z)(Ue,[["render",Pe],["__scopeId","data-v-98fb6cce"]]);var $e=Fe;const Oe=g("@/img/name_marker.svg"),De=g("@/img/simpl_name.svg"),ze=g("@/img/rating.svg"),Se=g("@/img/address.svg");var Ze={components:{ParamsList:$e},data(){return{name_marker:void 0,simpl_name:void 0,rating:void 0,address:void 0,whattodo:void 0}},mounted(){this.$refs["img_name_marker"].src=Oe,this.$refs["img_simpl_name"].src=De,this.$refs["img_rating"].src=ze,this.$refs["img_address"].src=Se},watch:{props_component:{async handler(e){this.name_marker=this.settings_type_place[e.type_place].name,this.simpl_name=e.simpl_name,this.rating=e.rating,this.address=e.address,this.whattodo=C(e),this.address=await M(e.cord_x,e.cord_y)},deep:!0}},computed:{...(0,v.rn)("geomap",["settings_type_place","select_PropertiesMark"]),props_component(){return this.select_PropertiesMark}}};const Ie=(0,r.Z)(Ze,[["render",Ce],["__scopeId","data-v-00c3661d"]]);var He=Ie;const je=e=>((0,i.dD)("data-v-4566017d"),e=e(),(0,i.Cn)(),e),Ee={class:"over_box_body"},Ae=je((()=>(0,i._)("div",{class:"empty"},null,-1)));function Be(e,t,a,n,s,r){const l=(0,i.up)("DetailFromPlace"),c=(0,i.up)("ExtraFeaturesWindow");return(0,i.wg)(),(0,i.iD)("div",{class:"over_box_comp",onKeyup:t[1]||(t[1]=(0,o.D2)(((...e)=>r.hiddenOverBox&&r.hiddenOverBox(...e)),["esc"])),tabindex:"0"},[(0,i._)("div",Ee,[(0,i.wy)((0,i.Wm)(l,null,null,512),[[o.F8,"DetailFromPlace"===a.view_component]]),(0,i.wy)((0,i.Wm)(c,{onHiddenOverBox:r.hiddenOverBox},null,8,["onHiddenOverBox"]),[[o.F8,"ExtraFeaturesWindow"===a.view_component]])]),Ae,(0,i._)("input",{ref:"hidden_over_box",class:"hidden_over_box",type:"image",onClick:t[0]||(t[0]=(...e)=>r.hiddenOverBox&&r.hiddenOverBox(...e))},null,512)],32)}const Le={class:"box"},qe={class:"title"},We={key:0,class:"name"},Ve={class:"value"},Ne={key:0,class:"list"},Re=["href"],Te={key:2},Ge={class:"box_edit_geomap"};function Ye(e,t,a,o,n,s){const r=(0,i.up)("ParamsList");return(0,i.wg)(),(0,i.iD)("div",Le,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(s.view_list,((e,t)=>((0,i.wg)(),(0,i.iD)("div",{class:"row",key:t},[(0,i._)("div",qe,(0,oe.zw)(e.title),1),((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(e.data,((e,t)=>((0,i.wg)(),(0,i.iD)("div",{class:"view_list_data",key:t},[e.name?((0,i.wg)(),(0,i.iD)("div",We,(0,oe.zw)(e.name),1)):(0,i.kq)("",!0),(0,i._)("div",Ve,["object"==typeof e.value?((0,i.wg)(),(0,i.iD)("div",Ne,[(0,i.Wm)(r,{params_list:e.value},null,8,["params_list"])])):"string"==typeof e.value&&e.value.includes("://")?((0,i.wg)(),(0,i.iD)("a",{key:1,target:"_blank",href:e.value},(0,oe.zw)(e.value),9,Re)):((0,i.wg)(),(0,i.iD)("span",Te,(0,oe.zw)(e.value),1))])])))),128))])))),128)),(0,i._)("div",Ge,[(0,i._)("input",{onClick:t[0]||(t[0]=(...e)=>s.clickUpdateGeomap&&s.clickUpdateGeomap(...e)),class:"edit_geomap",type:"image",ref:"edit_geomap"},null,512)])])}const Ke=g("@/img/edit_geomap.png");function Je(){return{phones:void 0,website:void 0,tg:void 0,vk:void 0,any_social:void 0,yandex_map:void 0,any_link:void 0}}var Qe={components:{ParamsList:$e},data(){return{name_marker:void 0,rating:void 0,simpl_name:void 0,whattodo:void 0,address:void 0,AveragePopulation:void 0,AverageCostVisit:void 0,FavoritesCountMore:void 0,"InternetСontacts":Je()}},mounted(){this.$refs["edit_geomap"].src=Ke},methods:{async updateData(e){this.clear_ppd()},parse_ppd(e){this.AveragePopulation=p[e.AveragePopulation],this.AverageCostVisit=`${e.AverageCostVisit.value} ${u[e.AverageCostVisit.currency]}`,this.InternetСontacts=e.InternetСontacts,this.FavoritesCountMore=`более ${e.FavoritesCountMore}`},clear_ppd(){this.AveragePopulation=void 0,this.AverageCostVisit=void 0,this.InternetСontacts=Je(),this.FavoritesCountMore=void 0},clickUpdateGeomap(){}},watch:{props_component:{handler(e){this.name_marker=this.settings_type_place[e.type_place].name,this.rating=e.rating,this.simpl_name=e.simpl_name,this.address=e.address,this.whattodo=C(e),this.updateData(e)},deep:!0}},computed:{...(0,v.rn)("geomap",["settings_type_place","select_PropertiesMark"]),props_component(){return this.select_PropertiesMark},view_list(){return[{title:"Общая информация",data:[{name:"Тип маркера",value:this.name_marker},{name:"Рейтинг",value:this.rating},{name:"Название",value:this.simpl_name},{name:"Адрес",value:this.address},{name:"Средняя людность",value:this.AveragePopulation},{name:"Средняя стоимость посещения",value:this.AverageCostVisit},{name:"В избранных",value:this.FavoritesCountMore}]},{title:"Чем тут можно заняться",data:[{value:this.whattodo}]},{title:"Это место в интернете",data:[{name:"phones",value:this.InternetСontacts.phones},{name:"website",value:this.InternetСontacts.website},{name:"tg",value:this.InternetСontacts.tg},{name:"vk",value:this.InternetСontacts.vk},{name:"any_social",value:this.InternetСontacts.any_social},{name:"yandex_map",value:this.InternetСontacts.yandex_map},{name:"any_link",value:this.InternetСontacts.any_link}]}]}}};const Xe=(0,r.Z)(Qe,[["render",Ye],["__scopeId","data-v-61dabad4"]]);var et=Xe;const tt={class:"container"},at={class:"box_extra"},ot={class:"box_select_elm"};function it(e,t,a,n,s,r){const l=(0,i.up)("AddPlace");return(0,i.wg)(),(0,i.iD)("div",tt,[(0,i.wy)((0,i._)("div",at,[(0,i._)("div",{class:"row",onClick:t[0]||(t[0]=e=>r.handleClick("add_place"))}," Создать новое место в выбранной точки "),(0,i._)("div",{class:"row",onClick:t[1]||(t[1]=(...e)=>r.channel_list&&r.channel_list(...e))}," Список каналов "),(0,i._)("div",{class:"row",onClick:t[2]||(t[2]=e=>r.handleClick("login"))},"Вход"),(0,i._)("div",{class:"row",onClick:t[3]||(t[3]=e=>r.handleClick("registration"))}," Регистрация "),(0,i._)("div",{class:"row",onClick:t[4]||(t[4]=e=>r.handleClick("about"))},"О проекте")],512),[[o.F8,void 0==s.select_elm]]),(0,i._)("div",ot,[(0,i.wy)((0,i.Wm)(l,{ref:"add_place",onHidden_elm:r.hidden_elm,onHiddenOverBox:r.hiddenOverBox},null,8,["onHidden_elm","onHiddenOverBox"]),[[o.F8,"add_place"===s.select_elm]])])])}const nt=e=>((0,i.dD)("data-v-7571a6cd"),e=e(),(0,i.Cn)(),e),st={class:"box_extra"},rt={class:"row"},lt=nt((()=>(0,i._)("div",{class:"label"},"* Короткое имя:",-1))),ct={class:"row"},dt=nt((()=>(0,i._)("div",{class:"label"},"* Рейтинг места:",-1))),_t={class:"row"},pt=nt((()=>(0,i._)("div",{class:"label"},"* What to do:",-1))),mt=["value"],ut={class:"row"},ht=nt((()=>(0,i._)("div",{class:"label"},"* Type place:",-1))),vt=["value"];function gt(e,t,a,n,s,r){const l=(0,i.up)("VButton");return(0,i.wg)(),(0,i.iD)("div",st,[(0,i._)("label",rt,[lt,(0,i.wy)((0,i._)("input",{"onUpdate:modelValue":t[0]||(t[0]=e=>s.shortName=e)},null,512),[[o.nr,s.shortName]])]),(0,i._)("label",ct,[dt,(0,i.wy)((0,i._)("input",{"onUpdate:modelValue":t[1]||(t[1]=e=>s.rating=e),type:"number",min:"1",max:"5"},null,512),[[o.nr,s.rating]])]),(0,i._)("label",_t,[pt,(0,i.wy)((0,i._)("select",{"onUpdate:modelValue":t[2]||(t[2]=e=>s.todo=e),multiple:"",class:"todo"},[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(s.todoOptions,(e=>((0,i.wg)(),(0,i.iD)("option",{value:e},(0,oe.zw)(e.todo),9,mt)))),256))],512),[[o.bM,s.todo]])]),(0,i._)("label",ut,[ht,(0,i.wy)((0,i._)("select",{"onUpdate:modelValue":t[3]||(t[3]=e=>s.typePlace=e)},[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(s.typePlaceOptions,(e=>((0,i.wg)(),(0,i.iD)("option",{value:e},(0,oe.zw)(e.name),9,vt)))),256))],512),[[o.bM,s.typePlace]])]),(0,i.Wm)(l,{class:"send_bt",value:"Отправить",onClickBt:r.create_geomap},null,8,["onClickBt"]),(0,i._)("input",{ref:"hidden_elm",class:"hidden_elm",type:"image",onClick:t[4]||(t[4]=(...e)=>r.hidden_elm&&r.hidden_elm(...e))},null,512)])}function wt(e,t,a,o,n,s){return(0,i.wg)(),(0,i.iD)("button",{class:"custom-button",onClick:t[0]||(t[0]=(...e)=>s.handleClick&&s.handleClick(...e))},(0,oe.zw)(a.value),1)}var kt={props:{value:{type:[String,Number],required:!0}},methods:{handleClick(){this.$emit("clickBt",this.value)}}};const yt=(0,r.Z)(kt,[["render",wt],["__scopeId","data-v-e3fc72d0"]]);var ft=yt,Ct={emits:["hidden_elm","hiddenOverBox"],components:{VButton:ft},mounted(){this.$refs["hidden_elm"].src=Dt,this.show()},data(){return{shortName:"",rating:1,todo:[],typePlace:{},todoOptions:[],typePlaceOptions:[]}},computed:{...(0,v.rn)("geomap",["select_channel_geomap","coordinat_click","RefMapContainer"])},methods:{hidden_elm(){this.$emit("hidden_elm")},async create_geomap(){console.log("Отправка: создание нового места");const e=this.coordinat_click;console.log(this.$refs);const t={cord_x:e.latitude,cord_y:e.longitude,simpl_name:this.shortName,rating:this.rating,address:"",channel_geomap:this.select_channel_geomap.id,what_todo:this.todo.map((e=>e.id)),type_place:this.typePlace.id},a=await y(Ht,t);a.ok?(alert("Успешное создание нового места"),this.hidden_elm(),this.$emit("hiddenOverBox"),this.RefMapContainer._setMarkersFromGeomap(JSON.parse(a.data)),this.$router.push({name:"main_map",query:this.$route.query})):alert(`Ошибка создания нового места: ${a.data}`)},async show(){const[e,t]=await Promise.all([k(Zt),k(It)]);e.ok&&(this.todoOptions=e.data),t.ok&&(this.typePlaceOptions=t.data),this.typePlace=this.typePlaceOptions[0]}}};const Mt=(0,r.Z)(Ct,[["render",gt],["__scopeId","data-v-7571a6cd"]]);var bt=Mt,xt={components:{AddPlace:bt},data(){return{select_elm:void 0}},methods:{async handleClick(e){await this.$refs[e].show(),this.select_elm=e},channel_list(){this.$router.push({name:"list_channels"})},hidden_elm(){this.select_elm=void 0},hiddenOverBox(){this.$emit("hiddenOverBox")}}};const Pt=(0,r.Z)(xt,[["render",it],["__scopeId","data-v-0a0b0e6a"]]);var Ut=Pt,Ft={emits:["hidden_over_box"],components:{DetailFromPlace:et,ExtraFeaturesWindow:Ut},props:{view_component:{type:Object}},mounted(){this.$refs["hidden_over_box"].src=Dt},methods:{hiddenOverBox(){this.$emit("hidden_over_box")}}};const $t=(0,r.Z)(Ft,[["render",Be],["__scopeId","data-v-4566017d"]]);var Ot=$t;const Dt=g("@/img/arrow_up.svg"),zt=g("@/img/info_from_place.svg"),St=w("@/api/v1/channel_geomap_place/"),Zt=w("@/api/v1/what_todo/"),It=w("@/api/v1/type_place/"),Ht=w("@/api/v1/place/"),jt=w("@/api/v1/channel_geomap/");var Et={name:"MapApp",components:{MapContainer:ae,FacileFromMarker:He,OverBox:Ot},data(){return{view_component:void 0,is_show_FacileFromMarker:!1,is_show_map_detail:!0}},async mounted(){this.$refs["show_map_detail"].src=Dt,this.$refs["show_map_detail_place"].src=zt,await this.Mounted_ParseUrl(),this.Update_url_geomap(g(St)+this.select_channel_geomap.id),this.Update_RefMapContainer(this.$refs["MapContainer"]),this.RefMapContainer._initMap(this.coordinat_click,this.select_zoom,this.url_geomap)},computed:{...(0,v.rn)("geomap",["select_channel_geomap","coordinat_click","select_zoom","url_geomap","RefMapContainer"]),...(0,v.Se)("geomap",["coordinat_click_cord"])},methods:{...(0,v.OI)("geomap",["Update_select_zoom","Update_url_geomap","Update_RefMapContainer"]),...(0,v.nv)("geomap",["Update_coordinat_click","Update_select_channel","Update_type_view"]),setCoordinates(e,t=!1){this.$refs["MapContainer"].setCoordinates(this.$refs["MapContainer"]._parseCoordFromOpenstreetmap(e),t)},HandleMarkerClick(e){this.ShowPlaceFacileInfo()},HandleEmptyMapClick(e){this.is_show_map_detail=!0,this.is_show_FacileFromMarker=!1},ShowPlaceFacileInfo(){this.is_show_map_detail=!1,this.is_show_FacileFromMarker=!0},ShowPlaceDetailsInfo(){this.view_component="DetailFromPlace"},ShowExtraFeaturesWindow(){this.view_component="ExtraFeaturesWindow"},hidden_over_box(){this.view_component=void 0},async Mounted_ParseUrl(){let e=f(this.$route.query);const t=parseInt(e["c"]);if(isNaN(t))return console.log("Не указан ID канала"),void this.$router.push({name:"list_channels"});{const e=await k(jt+t);if(e.ok){const t=e.data;this.Update_select_channel({channel:t,router:this.$router,route:this.$route})}else console.error("Не удалось получить список каналов")}let a=parseInt(e["z"]);a||(a=16),this.Update_select_zoom(a),this.Update_coordinat_click({coord:e[d.latitude]&&e[d.longitude]?{latitude:e[d.latitude],longitude:e[d.longitude]}:{latitude:this.select_channel_geomap.default_coord_x,longitude:this.select_channel_geomap.default_coord_y},router:this.$router,route:this.$route}),this.Update_type_view({type_view:e[d.type_view]?e[d.type_view]:c.main_map,router:this.$router,route:this.$route}),this.$router.push({query:e})}}};const At=(0,r.Z)(Et,[["render",Z]]);var Bt=At;const Lt=e=>((0,i.dD)("data-v-5ad126f2"),e=e(),(0,i.Cn)(),e),qt={class:"container"},Wt=Lt((()=>(0,i._)("h1",null,"Список каналов",-1))),Vt={class:"box_extra"};function Nt(e,t,a,n,s,r){const l=(0,i.up)("VButton");return(0,i.wg)(),(0,i.iD)("div",qt,[Wt,(0,i.wy)((0,i._)("div",Vt,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(s.channels,(e=>((0,i.wg)(),(0,i.j4)(l,{class:"row",key:e.id,value:e.name,onClick:t=>r.selectChannel(e)},null,8,["value","onClick"])))),128))],512),[[o.F8,void 0==e.select_elm]])])}var Rt={components:{VButton:ft},data(){return{channels:[]}},async mounted(){await this.fetchChannels()},methods:{...(0,v.nv)("geomap",["Update_select_channel"]),async fetchChannels(){const e=await k(jt);e.ok?this.channels=e.data:console.error("Не удалось получить список каналов")},selectChannel(e){this.Update_select_channel({channel:e,router:this.$router,route:this.$route});d.channel;this.$router.push({name:"main_map",query:{c:e.id}})}}};const Tt=(0,r.Z)(Rt,[["render",Nt],["__scopeId","data-v-5ad126f2"]]);var Gt=Tt;const Yt=[{path:"/",name:"main_map",component:Bt},{path:"/channels",name:"list_channels",component:Gt}],Kt=(0,x.p7)({routes:Yt,history:(0,x.PO)()});var Jt=(0,v.MT)({state:{},getters:{},mutations:{},actions:{},modules:{geomap:b}});let Qt=(0,o.ri)(h);Qt.use(Kt).use(Jt).mount("#app")}},t={};function a(o){var i=t[o];if(void 0!==i)return i.exports;var n=t[o]={exports:{}};return e[o].call(n.exports,n,n.exports,a),n.exports}a.m=e,function(){var e=[];a.O=function(t,o,i,n){if(!o){var s=1/0;for(d=0;d<e.length;d++){o=e[d][0],i=e[d][1],n=e[d][2];for(var r=!0,l=0;l<o.length;l++)(!1&n||s>=n)&&Object.keys(a.O).every((function(e){return a.O[e](o[l])}))?o.splice(l--,1):(r=!1,n<s&&(s=n));if(r){e.splice(d--,1);var c=i();void 0!==c&&(t=c)}}return t}n=n||0;for(var d=e.length;d>0&&e[d-1][2]>n;d--)e[d]=e[d-1];e[d]=[o,i,n]}}(),function(){a.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return a.d(t,{a:t}),t}}(),function(){a.d=function(e,t){for(var o in t)a.o(t,o)&&!a.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){a.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={143:0};a.O.j=function(t){return 0===e[t]};var t=function(t,o){var i,n,s=o[0],r=o[1],l=o[2],c=0;if(s.some((function(t){return 0!==e[t]}))){for(i in r)a.o(r,i)&&(a.m[i]=r[i]);if(l)var d=l(a)}for(t&&t(o);c<s.length;c++)n=s[c],a.o(e,n)&&e[n]&&e[n][0](),e[n]=0;return a.O(d)},o=self["webpackChunkweb_chillmap"]=self["webpackChunkweb_chillmap"]||[];o.forEach(t.bind(null,0)),o.push=t.bind(null,o.push.bind(o))}();var o=a.O(void 0,[998],(function(){return a(9014)}));o=a.O(o)})();
//# sourceMappingURL=app.287aff54.js.map