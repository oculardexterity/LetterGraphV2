	
var graphLoaded = false;

//var cameraEvent = $.debounce(500, function() {
//	if (graphLoaded) {
//		router.url.setVar('camera', graph.camera.x + ',' + graph.camera.y + ',' + graph.camera.ratio);
//	}
//});

var graphManager = (function(config) {
	function merge_objects(obj1,obj2){
    var obj3 = {};
    for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
    for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
    return obj3;
	}




	var return_data;
	var highlight_to_keep = {};

	//console.log(config);
	
	var container = document.getElementById(config.container);
	




	var sigmaWebgl = new sigma({
			
			renderer: {
			    container: container, 
			    type: 'webgl'

			},
			settings: {
					drawLabels: true,
			    nodesPowRatio: 0.001,
			    rescaleIgnoreSize: false,
			    autoResize: false,
			    zoomMax: 3000,
			    minNodeSize: 5,
			    maxNodeSize: 6,
			    maxEdgeSize: 1,
			    labelThreshold: 10,
			   // nodeActiveLevel: 5,
			    zoomMin: 0.01,
			    shortLabelsOnHover: true

			}
	});

	var camera = sigmaWebgl.camera;





	var tooltipConfig = {
	    	node: {
		    	show: 'clickNode',
		        cssClass: 'sigma-tooltip',
		    	position: 'top',
		        autoadjust: true,
		        //template: letterLabelTemplate,
	 
		    	renderer: function(node, template) {
		        	// The function context is s.graph
		        	//node.degree = this.degree(node.id);
		      
		        	//console.log(node, 'hi')
		        	if (!isPressed) {
				    if (node.data.type === 'Letter') {
			        // Returns an HTML string:
			     		//console.log(node.data.search_kwic);
			        if ('search_kwic' in node.data && node.data.search_kwic != '') {
			        	return Mustache.render(letterLabelSearchTermTemplate(), node);
			        }
				    	return Mustache.render(letterLabelTemplate(), node);
		    		}
		      		else {
		        		return Mustache.render(personLabelTemplate(), node)
		        	}
			}
		        	// Returns a DOM Element:
		        	//var el = document.createElement('div');
		        	//return el.innerHTML = Mustache.render(template, node);
			    }
			}
		};

	var tooltipsWebgl = sigma.plugins.tooltips(sigmaWebgl, sigmaWebgl.renderers[0], tooltipConfig);
  
	var isPressed;
	$(document).keydown(function(e) {
			 	
			 	//console.log(e);
		      if (e.which == 91 || e.metaKey || e.ctrlKey || e.metaKey) {
		      	//console.log('pressed');
		      	isPressed = true;
		      	//console.log(isPressed);
		      }
		    });

			 $(document).keyup(function(e) {
			 	isPressed = false;
			 	//console.log(isPressed);
			 });




	sigmaWebgl.bind('clickNode', function(e) {
			
				if (isPressed) {
					var nodeId = e.data.node.id;
	        highlightNode(nodeId);

	      }
	      
  });

  function highlightNode(nodeId) {
  				/// CHECK nodeId is not ALREADY in selectedNode!!!!
  				
  				if (router.url.getVar('selectedNode')) {
	  				  var currentSelectedNodes = router.url.getVar('selectedNode');
	  				  if (currentSelectedNodes.indexOf(nodeId) == -1) {
			  				router.url.setVar('selectedNode',  currentSelectedNodes + ';' + nodeId);
			  			}
	  			}
	  			else {
	  				
	  				router.url.setVar('selectedNode', nodeId);
	  			}
	  			
  				// Looks up all the adjacent nodes to node with id=nodeId
	        highlight_to_keep = merge_objects(sigmaWebgl.graph.neighbors(nodeId), highlight_to_keep);
	        
	        
	        // Adds nodeId data to toKeep list
	        highlight_to_keep[nodeId] = sigmaWebgl.graph.nodes(nodeId);
	        

	        sigmaWebgl.graph.nodes().forEach(function(n) {
	          if (highlight_to_keep[n.id])
	            n.color = n.originalColor;
	          else

	            n.color = n.lighten_color || '#eee';
	        });

	        sigmaWebgl.graph.edges().forEach(function(e) {
	          if (highlight_to_keep[e.source] && highlight_to_keep[e.target])
	            e.color = e.originalColor;
	          else
	            e.color = '#eee';
	        });

	        // Since the data has been modified, we need to
	        // call the refresh method to make the colors
	        // update effective.
	        sigmaWebgl.refresh();
  }

		sigmaWebgl.bind('clickStage', function(e) {
				if (isPressed) {
	        sigmaWebgl.graph.nodes().forEach(function(n) {
	          n.color = n.originalColor;
	        });

	        sigmaWebgl.graph.edges().forEach(function(e) {
	          e.color = e.originalColor;
	        });
	        router.url.setVar('selectedNode', '');
	        router.url.removeVar('selectedNode');
	        //console.log('var after remove', router.url.vars['selectedNode']);
	        highlight_to_keep = {};
	        // Same as in the previous event:
	        sigmaWebgl.refresh();
	      }
      });



	camera.bind('coordinatesUpdated', $.debounce(300, function() {
	   		router.url.setVar('camera', camera.x + ',' + camera.y + ',' + camera.ratio);  	
		})
	);




	function drawGraphWithData(data) {
		//console.log(data);
		

		var g = JSON.parse(data);
		console.log(g);

		var nodeIds = getCurrentNodeIds();
		//console.log(nodeIds);
		console.log("nodes length", g.nodes.length);

		// For some reason crashing on automatic import -- add manually
		for (var i = 0, j = g.nodes.length; i < j; i++) {
			
			if (sigmaWebgl.graph.nodes(g.nodes[i].id)) {
				
				var existingNode = sigmaWebgl.graph.nodes(g.nodes[i].id);
				//console.log(existingNode);
				existingNode.x = g.nodes[i].x;
				existingNode.y = g.nodes[i].y;

				// Here going to have to add in additional info:: to wit, search Kwic
			}
			else {
				//console.log(g.nodes[i]);
				sigmaWebgl.graph.addNode(g.nodes[i]);
			}


		}

		var newNodesIds = g.nodes.map(function(i) {return i.id});
		nodeIds = nodeIds.filter(function(el) {
			if (newNodesIds.indexOf(el) < 0) {
				sigmaWebgl.graph.dropNode(el);
			}
		});


		var edgeIds = getCurrentEdgeIds();

		for (var i = 0, j = g.edges.length; i < j; i ++) {
			//console.log(g.edges[i]);
			if (sigmaWebgl.graph.edges(g.edges[i].id)) {
				// Do nothing, edge already there
			}
			else {
				sigmaWebgl.graph.addEdge(g.edges[i]);
			}
		}


		

		// Fire off all the graph options on data complete
		sigmaWebgl.refresh();
		bindTooltips();
		setCamera();

		if ('selectedNode' in router.url.vars) {
			var nodes = router.url.vars['selectedNode'].split(';');
			for (var i = 0, j = nodes.length; i < j; i++) {
				highlightNode(nodes[i]);
			}
		}
	

		
	}







	// Set camera position from URL
	function setCamera() {
		
		if ('camera' in router.url.vars) {
			var coords = router.url.getVar('camera').split(",");
			camera.goTo({ x: parseFloat(coords[0]), y: parseFloat(coords[1]), ratio: parseFloat(coords[2]) });	
		}
		else {
			camera.goTo({x: 0, y: 0, ratio: 1});
		}
		
		
		return 'set camera complete';
	}

	function getCurrentNodeIds() {
		var allNodes = sigmaWebgl.graph.nodes();
		nodeIds = allNodes.map(function(node) {
			return node.id;
		});
		return nodeIds;
	}

	function getCurrentEdgeIds() {
		var allEdges = sigmaWebgl.graph.edges();
		edgeIds = allEdges.map(function(edge) {
			return edge.id;
		})
		return edgeIds;
	}


	function bindTooltips() {

		tooltipsWebgl.bind('shown', function(event) {
			//console.log(router);
		    $(".showLetterLink").click(function(e){
			    e.preventDefault();
			    var url = $(this).attr('href');
			    console.log(url);
			    if (router.url.getVar('searchTerm')) {
			    	urlST = url + '?searchTerm=' + router.url.getVar('searchTerm');
			    	router.getData('letter/' + urlST, letter.showLetterContent);
			    }
			    else {
			    	router.getData('letter/' + url, letter.showLetterContent);
			    }
			    console.log(url);
			    router.url.setVar('letter', url);
			    
			    
		    });
		});

		tooltipsWebgl.bind('hidden', function(event) {
		  //console.log('tooltip hidden', event);
		});
		console.log('bindTooltips called');
	}

	return {
		// Expose a default drawGraph method (takes JSON)
		drawGraph: drawGraphWithData,

		// Expose the sigma instance...
		sigma: sigmaWebgl,
		camera: camera,
		setCamera: setCamera

	}
});