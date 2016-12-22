


/*$(document).on('dnd_start.vakata',function(event,data){
                                          alert(data); 
                                        });*/

$(function() {

				$(".draggable-button").draggable({
									revert: 'invalid',
									cursor:'move', 
                                                                        snap:true
								});
  	                        $('#box').jstree({
                                                        'plugins':["dnd","types"],
                                                        'core' : {
                                                    
                                                                  'check_callback' : true;                
                                                                        
                                                                  'data' : [
                                                                            {
                                                                             "text" : "Root node",
                                                                             "state" : {"opened" : true },
									     "type":"root",
                                                                             "children" : [
                                                                                           {
                                                                                            "text" : "Child node 1",
                                                                                            "state" : { "selected" : true },
											    "type": "category"
                                                                                           },
                                                                                           { "text" : "Child node 2",
										             "state" : { "disabled" : true },
											     "type": "string"
											   }
                                                                                           { "text" : "Child node 3",
										             "state" : { "disabled" : true },
											     "type": "float"
											   }
                                                                                           { "text" : "Child node 4",
										             "state" : { "disabled" : true },
											     "type": "else"
											   }
                                                                                          ]
                                                                            }
                                                                           ]
								  'types':{
                  							"root":	{
											"valid_children": ["category","string","float","else"]
										}
                  							"category":	{
											"valid_children": ["category","string","float","else"]
										}
                  							"string":	{
											"valid_children": [],
											"icon": "glyphicon glyphicon-file"
										}
                  							"float":	{
											"valid_children": [],
											"icon" : "glyphicon glyphicon-file"
										}
                  							"else":	{
											"valid_children": [],
											"icon" : "glyphicon glyphicon-file"
										}
								  }
                                                                 }
                                                 });
                             }
                  );

