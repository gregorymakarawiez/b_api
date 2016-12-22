


/*$(document).on('dnd_start.vakata',function(event,data){
                                          alert(data); 
                                        });*/


/*$(document).ready(function() {*/
                             
				/*$(".draggable-button").draggable({
									revert: 'invalid',
									cursor:'move'
								});*/
     


  	                        /*$('#box').jstree({
                                                        'plugins':["dnd"],
                                                        'core' : {*/
                                                    
                                                                  /*'check_callback' : true; */               
                                                                        
                                                                  /*'data' : [
                                                                            {
                                                                             "text" : "Root node",
                                                                             "state" : {"opened" : true },
                                                                             "children" : [
                                                                                           {
                                                                                            "text" : "Child node 1",
                                                                                            "state" : { "selected" : true },
                                                                                            "icon" : "glyphicon glyphicon-flash"
                                                                                           },
                                                                                           { "text" : "Child node 2", "state" : { "disabled" : true } }
                                                                                          ]
                                                                            }
                                                                           ]
                                                                 }
                                                 });
                             }
                  );*/

/*$(function() {
		/*$(".draggable").draggable({
						containment:"#port-editor",
						revert: 'invalid',
						cursor:'move',
						scroll:false,
						snap:'.droppable'
						/*drag: function(){
							alert('drag done');
						}
		});



		$('.droppable').droppable({
                        accept:'.draggable',
			drop: function(){
				alert('drop done');
			}
		});*/

		/*$('#box1').jstree({
					'plugins':["dnd"],
                                        'core' : {
							'check_callback' : true,               
							'data' : [{
									"text" : "Root node",
									"state" : {"opened" : true },
									"children" :[{
											"text" : "Child node 1",
											"state" : { "selected" : true },
											"icon" : "glyphicon glyphicon-flash"
										      },
                                                                                      { "text" : "Child node 2", "state" : { "disabled" : true }
										      }
                                                                                     ]
                                                                 }]
                                                 }
                                 });*/


		
/*});*/

        webix.ready(function(){
            //plain json data, based on objects
            treea = new webix.ui({
                container:"webix-tree",
                view:"tree",
                activeTitle:true,
                data: [
                    { id:"1", open:true, value:"The Shawshank Redemption", data:[
                        { id:"1.1", value:"Part 1" },
                        { id:"1.2", value:"Part 2" },
                        { id:"1.3", value:"Part 3" }
                    ]},
                    { id:"2", value:"The Godfather", data:[
                        { id:"2.1", value:"Part 1" },
                        { id:"2.2", value:"Part 2" }
                    ]}
                ]
            });
        });



