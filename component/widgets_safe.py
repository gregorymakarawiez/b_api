from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.template import loader, Template
from django.shortcuts import render
from django.template.loader import render_to_string

class PortEditorWidget(forms.Widget):

    def render(self, name, value, attrs=None):    
        flat_attrs = flatatt(attrs) 


        #left_panel_html_tmpl=loader.get_template("component/ports/left_panel.html")
        #left_panel_html_context={'name':name,'value':value}
        #left_panel_html=left_panel_html_tmpl.render(left_panel_html_context)

        left_panel_html='''

        <!--Hidden fields to save port tree structure and data (json format) -->
        <textarea name=%(name)s style="display:none;"> %(value)s </textarea>

        <div class="form-group">
          <div id="%(name)s_jstree"></div>
          <span class="help-block">To edit port tree, right click on nodes</span>
        </div>
        
        <script type="text/javascript" charset="utf-8">

          // get handle to DOM widget storing port tree
          var %(name)s_hidden_text_DOM = $('textarea[name=%(name)s]'); // hidden textarea to save port tree structure and data

          // load json data from DOM widget
          var json=DOM_to_json(%(name)s_hidden_text_DOM);
           
 
          // define jstree settings
          $("#%(name)s_jstree").jstree({
          "core" : {
            "animation" : 0,
            "check_callback" : true,
            "themes" : { "stripes" : false },
            'data' : json["structure"]
          },
          "types" : {

            "root" : {
               "icon" : "glyphicon glyphicon-circle-arrow-right",
               "valid_children" : ["category","string","float"],
               "default":{draggable:false}
            },
            "category" : {
               "icon" : "glyphicon glyphicon-folder-open",
               "valid_children" : ["category","string","float"],
               "default":{draggable:false}
            },
            "string" : {
               "icon" : "glyphicon glyphicon-font",
               "valid_children" : [],
               "default":{draggable:false}
            },
            "float" : {
               "icon" : "glyphicon glyphicon-sound-5-1",
               "valid_children" : [],
               "default":{draggable:false}
            }
          },
          "plugins" : ["state","contextmenu", "types"],

          "contextmenu": {
            
            "items": function($node){
              var tree=$("#%(name)s_jstree").jstree(true);

              return {
                "Create": {
                  "label": "Create node",
                  "icon": "glyphicon glyphicon-plus",
                  "_disabled": function(obj){
                    switch($node.type){
                      case "root":
                        return false;
                      case "category":
                        return false;
                      default:
                        return true;
                    }
                  },
                  "submenu":{
                    "Category": {
                      "label": "Create category",
                      "icon": "glyphicon glyphicon-folder-open",
                      "action": function(obj){
                        var position = 'inside';
                        var parent = $node;
                        var newNode_data = { state: "open",  text: " ", type: "category" };
                        var newNode=$("#%(name)s_jstree").jstree().create_node(parent,newNode_data, "last");
                        $("#%(name)s_jstree").jstree("open_all");

                        default_category_data={
                          type:"category",
                          name:"",
                          description:"",
                        };

                        set_nodes_data(%(name)s_hidden_text_DOM, newNode,"_all", default_category_data);

                        console.dir($(this))
                        // save tree structure change in hidden field
                        jstree_onchange(%(name)s_hidden_text_DOM, tree);

                      },
                    },//Category end
                    "String": {
                      "label": "Create string",
                      "icon": "glyphicon glyphicon-font",
                      "action": function(obj){
                        var position = 'inside';
                        var parent = $node;
                        var newNode_data = { state: "open", text: " ", type: "string" };
                        var newNode=$("#%(name)s_jstree").jstree().create_node(parent,newNode_data, "last");
                        $("#%(name)s_jstree").jstree("open_all");
                        default_string_data={
                          type:"string",
                          name:"",
                          description:"",
                          default:""
                        };

                        set_nodes_data(%(name)s_hidden_text_DOM, newNode,"_all", default_string_data);


                        // save tree structure change in hidden field
                        jstree_onchange(%(name)s_hidden_text_DOM, tree);

                      },
                    },//String end

                    "Float": {
                      "label": "Create float",
                      "icon": "glyphicon glyphicon-sound-5-1",
                      "action": function(obj){
                        var position = 'inside';
                        var parent = $node;
                        var newNode_data = { state: "open", text: " ", type: "float" };
                        var newNode=$("#%(name)s_jstree").jstree().create_node(parent,newNode_data, "last");
                        $("#%(name)s_jstree").jstree("open_all");

                        default_float_data={
                          type:"float",
                          name:"",
                          description:"",
                          default:""
                        };

                        set_nodes_data(%(name)s_hidden_text_DOM, newNode,"_all", default_float_data);

                        // save tree structure change in hidden field
                        jstree_onchange(%(name)s_hidden_text_DOM, tree);
                      },
                    },//Float end
                  }//submenu end
                },//Create end     

                "Delete": {
                "label": "Delete node",
                "icon": "glyphicon glyphicon-remove-sign",
                "action": function (obj) {

                     // delete node data
                    nodes_ondelete(%(name)s_hidden_text_DOM, tree, $node);

                    $("#%(name)s_jstree").jstree('delete_node', $node);

                    // save tree structure change in hidden field
                    jstree_onchange(%(name)s_hidden_text_DOM, tree);                   

                  },
                  "_disabled": function(obj){
                    switch($node.type){
                      case 'root':
                        return true;
                      default:
                        return false;
                    }
                  }
                }// Delete End*/
              };// return end             
            }// items End
          }// contextmenu End
       
         });



          function DOM_to_json(DOM_handle){
            // get data saved in hidden field
            var DOM_val=DOM_handle.val();

            var json={};
            try {
              // import port tree structure and data from hidden textarea
              json=JSON.parse(DOM_val); 
            } catch (e) {

              // for new port tree, give default values
              json["structure"]=[{ "text" : "%(name)s", "type": "root", "children" : []}];
              json["data"]={};              
            }
             return json;
          }

          function json_to_DOM(DOM_handle,json){
            try{
              var value=JSON.stringify(json);

              DOM_handle.val(value);
            } catch (e) {
              console.error("json_to_DOM error:", e);
            }
          }

          function jstree_onchange(DOM_handle, jstree_obj){
            var json=DOM_to_json(DOM_handle);
            console.dir("jstree_onchange - old structure");
            console.dir(DOM_handle);
            console.dir(jstree_obj);
            json["structure"]=jstree_obj.get_json();
            json_to_DOM(DOM_handle,json);
            console.dir("jstree_onchange - new structure");
            console.dir(DOM_handle.val());
          }

          function set_nodes_data(DOM_handle, node, property, value){
            var json=DOM_to_json(DOM_handle);

            if (property==="_all"){
              json["data"][node]=value;             
            }
            else{
               json["data"][node][property]=value;         
            }
            json_to_DOM(DOM_handle,json);
          }
 
          function get_nodes_data(DOM_handle, node, property){

            var json=DOM_to_json(DOM_handle);
            var node_data=json["data"][node];
     
            if (node in json["data"]){
              var node_data=json["data"][node]; 
            }
            else{           
              return {};
            }
              
            if (property in node_data){
              value=node_data[property];             
            }
            else if(property==="_all"){
              value=node_data
            }
            else{
              value={};           
            }
            return value;
          }
         

          function nodes_ondelete(DOM_handle, tree, node){
            // get port json saved in hidden textarea 
            var json=DOM_to_json(DOM_handle);
            console.dir(json);

            // get all descendants of deleted node
            var descendants_id=[];
            get_descendants_id(tree,node.id,descendants_id);

            // remove from json.data all entries relative to descendants of the delete node (delete node included)
            update_data_on_node_delete(json,descendants_id)

            // save json in hidden textarea
            json_to_DOM(DOM_handle,json);
            console.dir(json);            
          }

          function update_data_on_node_delete(json,descendants_id){

             for (i=0;i<descendants_id.length;i++){
                 delete json["data"][descendants_id[i]];
             }
          }


          function get_descendants_id(tree,node_id,nodes_id) {

            // Get the actual node
            var node = tree.get_node(node_id);

            // Add it to the results
            nodes_id.push(node_id);

            // Attempt to traverse if the node has children
            if (tree.is_parent(node)) {
              $.each(node.children, function(index, child) {
                get_descendants_id(tree,child,nodes_id);
              });
            }
          };

        </script>''' % {'name':name,'value':value}


        category_port_form_html_tmpl='''
        <script id="category_port_form_html_tmpl" type="text/x-jsrender">
          <div class='panel panel-primary'> 
            <div class='panel-heading'> 
              {{:type}} port 
            </div> 
          </div> 
          <div class='panel-body'> 
            <div class='form-group'> 
              <label class='control-label' for='category_form_port_name'>Name</label>  
              <input type='text' 
                id='%(name)s_category_form_port_name'
                class='form-control'
                required
                placeholder='ex: Geometry'
                value='{{:name}}'
                onblur='%(name)s_port_name_onblur(event)'
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='category_form_description'>Description</label> 
              <textarea
                id='%(name)s_category_form_port_description'
                class='form-control'
                required
                placeholder='ex: all geometrical data'
                onblur='%(name)s_port_description_onblur(event)'
              >{{:description}}</textarea> 
            </div>
          </div>
        </script>''' % {'name':name}

        string_port_form_html_tmpl='''
        <script id="string_port_form_html_tmpl" type="text/x-jsrender">
          <div class='panel panel-primary'> 
            <div class='panel-heading'> 
              {{:type}} port 
            </div> 
          </div> 
          <div class='panel-body'> 
            <div class='form-group'> 
              <label class='control-label' for='string_form_port_name'>Name</label>  
              <input type='text' 
                id='%(name)s_string_form_port_name'
                class='form-control'
                required
                placeholder='ex: SG type'
                value='{{:name}}'
                onblur='%(name)s_port_name_onblur(event)'
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='string_form_description'>Description</label> 
              <textarea
                id='%(name)s_string_form_port_description'
                class='form-control'
                required
                placeholder='ex: available values are boiler or economizer'
                onblur='%(name)s_port_description_onblur(event)'
              >{{:description}}</textarea> 
            </div>
            <div class='form-group'> 
              <label class='control-label' for='string_form_port_default'>Default value</label>  
              <input type='text' 
                id='%(name)s_string_form_port_default'
                class='form-control'
                required
                placeholder='ex: boiler'
                value='{{:default}}'
                onblur='%(name)s_port_default_onblur(event)'
              ></input> 
            </div> 
          </div>
        </script>''' % {'name': name}

        float_port_form_html_tmpl='''
        <script id="float_port_form_html_tmpl" type="text/x-jsrender">
          <div class='panel panel-primary'> 
            <div class='panel-heading'> 
              {{:type}} port 
            </div> 
          </div> 
          <div class='panel-body'> 
            <div class='form-group'> 
              <label class='control-label' for='float_form_port_name'>Name</label>  
              <input type='text' 
                id='%(name)s_float_form_port_name'
                class='form-control'
                required
                placeholder='ex: g'
                value='{{:name}}'
                onblur='%(name)s_port_name_onblur(event)'
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='float_form_description'>Description</label> 
              <textarea
                id='%(name)s_float_form_port_description'
                class='form-control'
                required
                placeholder='ex: gravity acceleration'
                onblur='%(name)s_port_description_onblur(event)'
              >{{:description}}</textarea> 
            </div>
            <div class='form-group'> 
              <label class='control-label' for='float_form_port_default'>Default value</label>  
              <input type='text' 
                id='%(name)s_float_form_port_default'
                class='form-control'
                required
                placeholder='ex: 9.81'
                value='{{:default}}'
                onblur='%(name)s_port_default_onblur(event)'
              ></input> 
            </div> 
          </div> 
        </script>''' % {'name':name}

        else_port_form_html_tmpl='''
        <script id="else_port_form_html_tmpl" type="text/x-jsrender">
          <!--<div class='panel panel-primary'> 
            <div class='panel-heading'> 
              ({{:type}}) port
            </div> 
          </div> -->
          <div class='panel-body'>  
          </div>
        </script>'''

        right_panel_html='''
        <div id="%(name)s_port-form" class="container"></div>

        %(category_port_form_html_tmpl)s
        %(string_port_form_html_tmpl)s
        %(float_port_form_html_tmpl)s
        %(else_port_form_html_tmpl)s

        <script type="text/javascript" charset="utf-8">

          // 1 - display edit form adapted to the port type selected in the left panel
          $("#%(name)s_jstree").bind("select_node.jstree", function(evt, data){

            // get selected node
            var node=data.node

            // 1.1 - select html template
            switch(node.type){

              case "category":   
                var port_form_html_tmpl=$.templates('#category_port_form_html_tmpl');
                break;
              case "string":   
                var port_form_html_tmpl=$.templates('#string_port_form_html_tmpl');
                break;
              case "float":   
                var port_form_html_tmpl=$.templates('#float_port_form_html_tmpl');
                break;
              default: 
                var port_form_html_tmpl=$.templates('#else_port_form_html_tmpl');
            }

            // 1.2 - fetch data for templating
            node_data=get_nodes_data(%(name)s_hidden_text_DOM, node.id, "_all")

            // 1.3 - render right panel html
            var port_form_html=port_form_html_tmpl.render(node_data);
            
            $('#%(name)s_port-form').html(port_form_html);

          })

          function %(name)s_port_name_onblur(event){

            // update port name in left panel according to the one given in the right panel form
            
                // get jstree object
                var tree=$("#%(name)s_jstree").jstree();
               
                // get selected node in left panel jstree 
                var active_node=$("#%(name)s_jstree").jstree('get_selected');
 
                // get name value in right panel form 
                var new_name=$(event.target).val();

                // rename jstree node after name provided in right panl form
                $("#%(name)s_jstree").jstree('rename_node', active_node , new_name );
            
            // save changes in hidden textarea

                // save new node name 
                set_nodes_data(%(name)s_hidden_text_DOM, active_node[0], "name", new_name);

                // save tree structure 
                jstree_onchange(%(name)s_hidden_text_DOM, tree);
          }

          function %(name)s_port_description_onblur(event){
            // save new value 
            var active_node=$("#%(name)s_jstree").jstree('get_selected'); 
            var new_description=$(event.target).val(); 
            set_nodes_data(%(name)s_hidden_text_DOM, active_node[0], "description", new_description);

            // save tree structure change in hidden field
            var tree=$("#%(name)s_jstree").jstree();
            jstree_onchange(%(name)s_hidden_text_DOM, tree);
          }

          function %(name)s_port_default_onblur(event){
            // save new value in 
            var active_node=$("#%(name)s_jstree").jstree('get_selected'); 
            var new_default=$(event.target).val(); 
            set_nodes_data(%(name)s_hidden_text_DOM, active_node[0], "default", new_default);

            // save tree structure change in hidden field
            var tree=$("#%(name)s_jstree").jstree();
            jstree_onchange(%(name)s_hidden_text_DOM, tree);
          }

 

        </script>''' % {'name':name, 
                        'category_port_form_html_tmpl': category_port_form_html_tmpl,
                        'string_port_form_html_tmpl': string_port_form_html_tmpl,
                        'float_port_form_html_tmpl': float_port_form_html_tmpl,
                        'else_port_form_html_tmpl': else_port_form_html_tmpl}



        html='''
        <div  class="port-editor">

          <div class="left-panel"> 
            %(left_panel)s

          </div>

          <div class="right-panel">
            %(right_panel)s
          </div>

        </div>''' %{'left_panel':left_panel_html, 'right_panel':right_panel_html}

        #left_panel_tmpl=loader.get_template("component/port_editor/left_panel.html")
        #left_panel_context={'name':name,'value':value}
        #left_panel_html=left_panel_tmpl.render(left_panel_context)

        #port_editor_tmpl=loader.get_template("component/port_editor.html")
        #port_editor_context={'name':name,'value':value}
        #html=port_editor_tmpl.render(port_editor_context)
        #html=render_to_string([port_editor_tmpl],port_editor_context)
        print(html)
        return mark_safe(html)

 




