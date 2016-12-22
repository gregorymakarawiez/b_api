from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.template import loader, Template
from django.shortcuts import render
from django.template.loader import render_to_string

class PortEditorWidget(forms.Widget):

    def render(self, name, value, attrs=None):    
        flat_attrs = flatatt(attrs) 


        left_panel_html='''

        <!--Hidden field to save port tree structure and data (json format) -->
        <textarea name=%(name)s style="display:none;"> %(value)s </textarea>

        <!--DOM element that acommodates jstree  -->
        <div class="form-group">
          <div id="%(name)s_jstree"></div>
          <span class="help-block">To edit port tree, right click on nodes</span>
        </div>

        ''' % {'name':name,'value':value}


        js='''
        
        <script type="text/javascript" charset="utf-8">  

          
          // name space

          var %(name)s={};
            

          // 1 - load / save operations with hidden textarea
          //------------------------------------------------
          
          %(name)s.DOM_to_json=function(DOM_handle){
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
                 console.dir(json);
                 return json;
          };  //DOM_to_json end



          %(name)s.json_to_DOM=function(DOM_handle,json){
                try{
                  var value=JSON.stringify(json);

                  DOM_handle.val(value);
                } catch (e) {
                  console.error("json_to_DOM error:", e);
                }
          }; //json_to_DOM end
 
        

         // 2 - jstree operations
         //----------------------
       
       
          %(name)s.jstree_onchange=function(DOM_handle, jstree_obj){

                var json=%(name)s.DOM_to_json(DOM_handle);
                json["structure"]=jstree_obj.get_json();
                %(name)s.json_to_DOM(DOM_handle,json);
          };


          %(name)s.set_nodes_data=function(DOM_handle, node, property, value){
                var json=%(name)s.DOM_to_json(DOM_handle);
                console.dir("node: "+node);
                if (property==="_all"){
                  json["data"][node]=value;
                }
                else{
                   json["data"][node][property]=value;
                }
                %(name)s.json_to_DOM(DOM_handle,json);
          };


          %(name)s.get_nodes_data=function(DOM_handle, node, property){

                var json=%(name)s.DOM_to_json(DOM_handle);
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
          };


          %(name)s.nodes_ondelete=function(DOM_handle, tree, node){

                // get port json saved in hidden textarea
                var json=%(name)s.DOM_to_json(DOM_handle);
                console.dir(json);

                // get all descendants of deleted node
                var descendants_id=[];
                 %(name)s.get_descendants_id(tree,node.id,descendants_id);

                // remove from json.data all entries relative to descendants of the delete node (delete node included)
                 %(name)s.update_data_on_node_delete(json,descendants_id)

                // save json in hidden textarea
                %(name)s.json_to_DOM(DOM_handle,json);
                console.dir(json);
          };

          %(name)s.update_data_on_node_delete=function(json,descendants_id){

                 for (i=0;i<descendants_id.length;i++){
                     delete json["data"][descendants_id[i]];
                 }
          };


          %(name)s.get_descendants_id=function(tree,node_id,nodes_id) {

                // Get the actual node
                var node = tree.get_node(node_id);

                // Add it to the results
                nodes_id.push(node_id);

                // Attempt to traverse if the node has children
                if (tree.is_parent(node)) {
                  $.each(node.children, function(index, child) {
                     %(name)s.get_descendants_id(tree,child,nodes_id);
                  });
                }
          };
         

         // 3 - listeners on forms
         //----------------------


         %(name)s.port_name_onblur=function(event){

            // update port name in left panel according to the one given in the right panel form
               
                // get jstree object
                var tree=$("#%(name)s_jstree").jstree();
                alert(tree);
               
                // get selected node in left panel jstree 
                var active_node=$("#%(name)s_jstree").jstree('get_selected');
                alert(active_node);
                console.dir(active_node);

                // get name value in right panel form 
                var new_name=$(event.target).val();
                alert(new_name);

                // rename jstree node after name provided in right panl form
                $("#%(name)s_jstree").jstree('rename_node', active_node , new_name );
            
            // save changes in hidden textarea

                // save new node name 
                %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, active_node[0], "name", new_name);

                // save tree structure 
                %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);
            
          };

          %(name)s.port_description_onblur=function(event){
            /*
            // get jstree object
            var tree=$("#%(name)s_jstree").jstree();

            // save new value 
            var active_node=$("#%(name)s_jstree").jstree('get_selected'); 
            var new_description=$(event.target).val(); 
             %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, active_node[0], "description", new_description);

            // save tree structure change in hidden field
             %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);
            */
          };

          %(name)s.port_default_onblur=function(event){

            // get jstree object
            var tree=$("#%(name)s_jstree").jstree();

            // save new value in 
            var active_node=$("#%(name)s_jstree").jstree('get_selected'); 
            var new_default=$(event.target).val(); 
             %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, active_node[0], "default", new_default);

            // save tree structure change in hidden field
             %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);
          };

          
          // 4 - initialisations
          //--------------------
          
          %(name)s.init=function(){


            // 4.1 - properties

            // get handle to DOM widget storing port tree
            %(name)s.hidden_text_DOM = $('textarea[name=%(name)s]'); // hidden textarea to save port tree structure and data
          
            // load json data from DOM widget
            %(name)s.json=%(name)s.DOM_to_json(%(name)s.hidden_text_DOM);

            
             
            // 4.2 - define jstree settings
           
              $("#%(name)s_jstree").jstree({
              "core" : {
                "animation" : 0,
                "check_callback" : true,
                "themes" : { "stripes" : false },
                'data' : %(name)s.json["structure"]
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
                            var newNode_id=$("#%(name)s_jstree").jstree().create_node(parent,newNode_data, "last");
                            console.dir(newNode_id);
                            var newNode = $("#%(name)s_jstree").jstree().get_node(newNode_id);
                            newNode_id= "%(name)s_" + newNode_id;
                            console.dir(newNode);
                            $("#%(name)s_jstree").jstree().set_id(newNode,newNode_id);


                            $("#%(name)s_jstree").jstree("open_all");

                            default_category_data={
                              type:"category",
                              name:"",
                              description:""
                            };

                            %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, newNode_id,"_all", default_category_data);

                            // save tree structure change in hidden field
                             %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);

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

                             %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, newNode,"_all", default_string_data);


                            // save tree structure change in hidden field
                             %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);

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

                             %(name)s.set_nodes_data(%(name)s.hidden_text_DOM, newNode,"_all", default_float_data);

                            // save tree structure change in hidden field
                             %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);
                          },
                        },//Float end
                      }//submenu end
                    },//Create end

                    "Delete": {
                    "label": "Delete node",
                    "icon": "glyphicon glyphicon-remove-sign",
                    "action": function (obj) {

                         // delete node data
                         %(name)s.nodes_ondelete(%(name)s.hidden_text_DOM, tree, $node);

                        $("#%(name)s_jstree").jstree('delete_node', $node);

                        // save tree structure change in hidden field
                         %(name)s.jstree_onchange(%(name)s.hidden_text_DOM, tree);

                      },
                      "_disabled": function(obj){
                        switch($node.type){
                          case 'root':
                            return true;
                          default:
                            return false;
                        }
                      }
                    }// delete end
                  };// return end
                }// items end
              }// contextmenu End
             });// jstree end
           


             // 4.3 - display edit form adapted to the port type selected in the left panel
             $("#%(name)s_jstree").bind('select_node.jstree', function(evt, data){

              
               // get selected node
               var node=data.node

               // 4.3.1 - select html template
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
               alert('port_form_html_tmpl');

               // 4.3.2 - fetch data for templating
               node_data= %(name)s.get_nodes_data(%(name)s.hidden_text_DOM, node.id, "_all")
               console.dir(node_data);

               // 4.3.3 - render right panel html
               var port_form_html=port_form_html_tmpl.render(node_data);
            
               $('#%(name)s_port-form').html(port_form_html);
    

             })
           
           };// init end


  

          // 5 - Main program
          //--------------------

          %(name)s.init(); 



        </script>''' % {'name':name}


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
                onblur=%(name)s.port_name_onblur
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='category_form_description'>Description</label> 
              <textarea
                id='%(name)s_category_form_port_description'
                class='form-control'
                required
                placeholder='ex: all geometrical data'
                onblur=%(name)s.port_description_onblur
              >{{:description}}</textarea> 
            </div>
          </div>
        </script>


        ''' % {'name':name}

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
                onblur='port_name_onblur(event)'
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='string_form_description'>Description</label> 
              <textarea
                id='%(name)s_string_form_port_description'
                class='form-control'
                required
                placeholder='ex: available values are boiler or economizer'
                onblur='%(name)s.port_description_onblur(event)'
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
                onblur='%(name)s.port_default_onblur(event)'
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
                onblur='port_name_onblur(event)'
              ></input> 
            </div> 
            <div class='form-group'> 
              <label class='control-label' for='float_form_description'>Description</label> 
              <textarea
                id='%(name)s_float_form_port_description'
                class='form-control'
                required
                placeholder='ex: gravity acceleration'
                onblur='%(name)s.port_description_onblur(event)'
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
                onblur='%(name)s.port_default_onblur(event)'
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

        ''' % {'name':name,
               'category_port_form_html_tmpl': category_port_form_html_tmpl,
               'string_port_form_html_tmpl': string_port_form_html_tmpl,
               'float_port_form_html_tmpl': float_port_form_html_tmpl,
               'else_port_form_html_tmpl': else_port_form_html_tmpl}



        html='''
        <div  class="port-editor">

  
       
          <div class="left-panel"> 
            %(left_panel_html)s
          </div>

          %(js)s 

          <div class="right-panel">
            %(right_panel_html)s
          </div>



        </div>
        ''' %{'left_panel_html':left_panel_html,
              'right_panel_html':right_panel_html,
              'js':js,
             }




        return mark_safe(html)

 




