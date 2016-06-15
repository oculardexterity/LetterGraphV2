	



var graphManager = (function(config) {
	var return_data;

	console.log(config);
	
	var container = document.getElementById(config.container);
	




	var sigmaWebgl = new sigma({
			
			renderer: {
			    container: container, 
			    type: 'webgl'

			},
			settings: {
		
			}
	});


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

		        	// Returns a DOM Element:
		        	//var el = document.createElement('div');
		        	//return el.innerHTML = Mustache.render(template, node);
			    }
			}
		};

	//var tooltipsWebgl = sigma.plugins.tooltips(sigmaWebgl, sigmaWebgl.renderers[0], tooltipConfig);
  
	sigmaWebgl.bind('clickNode', function(e) {
        var nodeId = e.data.node.id,
            toKeep = sigmaWebgl.graph.neighbors(nodeId);

        toKeep[nodeId] = e.data.node;

        sigmaWebgl.graph.nodes().forEach(function(n) {
          if (toKeep[n.id])
            n.color = n.originalColor;
          else
            n.color = '#eee';
        });

        sigmaWebgl.graph.edges().forEach(function(e) {
          if (toKeep[e.source] && toKeep[e.target])
            e.color = e.originalColor;
          else
            e.color = '#eee';
        });

        // Since the data has been modified, we need to
        // call the refresh method to make the colors
        // update effective.
        sigmaWebgl.refresh();
      });


	var cam = sigmaWebgl.camera;

	


	function drawGraphWithData(data) {
		//console.log(data);

		var g = JSON.parse(data);


		var nodeIds = getCurrentNodeIds();
		console.log(nodeIds);

/*
		// For some reason crashing on automatic import -- add manually
		for (var i = 0, j = g.vertices.length; i < j; i++) {
			
			if (sigmaWebgl.graph.nodes(g.vertices[i].id)) {
				
				var existingNode = sigmaWebgl.graph.nodes(g.vertices[i].id);
				existingNode.x = g.vertices[i].x;
				existingNode.y = g.vertices[i].y;

				// Here going to have to add in additional info:: to wit, search Kwic
			}
			else {
				sigmaWebgl.graph.addNode(g.vertices[i]);
			}


		}

		var newNodesIds = g.vertices.map(function(i) {return i.id});
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
*/

sigmaWebgl.graph.read(g);


		sigmaWebgl.refresh();
		setCamera();
		//bindTooltips();

	}




	// Bind graph scrolling event to update of camera variable 
	/*
	sigmaWebgl.bind('coordinatesUpdated', $.debounce(300, function() {
			router.url.setVar('camera', graph.camera.x + ',' + graph.camera.y + ',' + graph.camera.ratio);
		})
	);*/

	// Set camera position from URL
	function setCamera() {
		if ('camera' in router.url.vars) {
			var coords = router.url.getVar('camera').split(",");

			sigma.misc.animation.camera(sigmaWebgl.camera, 
				{ x: parseFloat(coords[0]), y: parseFloat(coords[1]), ratio: parseFloat(coords[2]) });	
		}
		else {
			sigma.misc.animation.camera(sigmaWebgl.camera, 
				{ x:0, y: 0, ratio: 1 });	
		}
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
			    
			    /// THIS NEEDS TO BE A FUNCTION IN LETTERMANAGER!!!
			    router.getData('letter/' + url, letter.showLetterContent);
			    router.url.setVar('letter', url);
		    });
		});

		tooltipsWebgl.bind('hidden', function(event) {
		  //console.log('tooltip hidden', event);
		});
	
	}

	return {
		// Expose a default drawGraph method (takes JSON)
		drawGraph: drawGraphWithData,

		// Expose the sigma instance...
		sigma: sigmaWebgl,
		camera: cam,
		setCamera: setCamera

	}
});