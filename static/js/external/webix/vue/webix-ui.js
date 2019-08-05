function data_handler(value){
  var view = $$(this.webixId);

  if (typeof value === "object"){
    if (view.setValues)
      view.setValues(value);
    else if (view.parse){
      view.clearAll();
      view.parse(value)
    }
  } else if (view.setValue)
    view.setValue(value);

  webix.ui.each(view, function(sub){
    if (sub.hasEvent && sub.hasEvent("onValue"))
      sub.callEvent("onValue", [value]);
  }, this, true);
}

Vue.component("webix-ui", {
  props: ['config', 'value'],
  watch:{
    value:{
      handler:data_handler
    }
  },

  template:"<div></div>",
    
  mounted:function(){
    var config = webix.copy(this.config);
    config.$scope = this;

    this.webixId = webix.ui(config, this.$el);
    if (this.value)
      data_handler.call(this, this.value);
  },
  destroyed:function(){
    webix.$$(this.webixId).destructor();
  }
});