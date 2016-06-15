// TO DO --- parse window.location.pathname and trigger appropriate functions...


// true reloads data
var testingOverride = true;





sigma.classes.graph.addMethod('neighbors', function(nodeId) {

		console.log(this.allNeighborsIndex);
    var k,
        neighbors = {},
        index = this.allNeighborsIndex[nodeId] || {};

    for (k in index)
      neighbors[k] = this.nodesIndex[k];

    return neighbors;
 });



	



/*
	On document ready::
*/
var graph, router, letter;


$(document).ready(function() {


	letter = letterManager({
		container: '.closeLetter',
		closeLetterDiv: '.closeLetter'
	});


	// Initialise some shit:
	graph = graphManager({
		container: 'graphContainer',
		initialGraph: 'defaultGraph'
	});

	
	router = routerModule(graph, letter);
	router.initialise();

	/// DOES this query need to be pushed into some graphManager func?


	$('#showConsole').click(function() {
		$('.console').toggleClass('show');
	});
      
});







