String.prototype.contains = function(it) { return this.indexOf(it) != -1; };




var routerModule = (function(graph, letter) {
	//var graph, letter;
	
	function initialise() {
	//	graph = gr;
	//	letter = lett;

		//console.log('router init called');
		callFromUrl();




		// Do something about this.


		window.onpopstate = function(e) {
			callFromUrl();
		};

	}
	



	var url = (function() {
		
		var urlVars;
		grabBrowserUrl();

		function grabBrowserUrl() {
			var vars = {};
			var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
				vars[key] = value;
			});
			urlVars = vars;
		}

		function setBrowserUrl() {
			var string = '?'
			Object.keys(urlVars).forEach(function(key) {
    			//console.log(key, urlVars[key]);
    			string += key + '=' + urlVars[key] + '&';
			});
			string = string.slice(0, -1);
			//console.log('urlstring: ' + string);
			history.pushState(string, '', string);
		}


		function getVar(vari) {
			grabBrowserUrl();
			if (vari in urlVars) {
				return urlVars[vari];
			}
			else {
				return null;
			}
		}

		function setVar(vari, val) {
			urlVars[vari] = val;
			setBrowserUrl();
		}

		function removeVar(vari) {
			if (vari in urlVars) {
				//console.log('removing ' + vari)
				//console.log(urlVars);
				delete urlVars[vari];
				//console.log(urlVars);
				setBrowserUrl();
			}
		}

		

		return {
			vars: urlVars,
			getVar: getVar,
			setVar: setVar,
			removeVar: removeVar
			//setBrowserUrl: setBrowserUrl

		}
	})();

/*

	graph.sigma.bind('coordinatesUpdated', $.debounce(300, function() {
			url.setVar('camera', graph.camera.x + ',' + graph.camera.y + ',' + graph.camera.ratio);
		})
	);
*/

	/*
		TO DO: define some proper routes and the things calling them and all that it is etc.


		either this is going to have to be.... dunno... 

		Can it be suitably parametrised and bumped to server calls?

		Change this completely--- use query string variables and parsing function above... obvidently.
	*/
	function callFromUrl() {
		// must be set each time function is called, for obvious reasons
		

		//console.log(url);
		//url.setBrowserUrl();

		// rewrite this to pick up vars from query string.
		// also rewrite serverside routes (i.e. everything to match ''anything'' except /ajax/)


		// Checks letter is set, and is a number (loads letter first)
		
		function getLetter(urlvars) {

			//////ABSTRACT OUT THE MECHANICS OF DOING IT TO A CALLABLE FUNCTION --- i.e.
			/// LETTER VALUE can be passed in, or not...

			if ('letter' in urlvars && Number(urlvars['letter'])) {
				if ('searchTerm' in urlvars) {
					var urlToGet = 'letter/' + urlvars['letter'] + '?searchTerm=' + urlvars['searchTerm']
					//console.log('searchterm for letter call: ' + urlToGet);
					getData(urlToGet, letter.showLetterContent);
					
				}
				else {
					getData('letter/' + urlvars['letter'], letter.showLetterContent);
				}
			}
			else {
				letter.closeLetter();
			}
			
		}
		getLetter(url.vars);

		//graph.setCamera();
		


	
		var next_char = ""
		// If graph=default or no graph var, draw default graph
		if (url.vars['graph'] === 'default' || !('graph' in url.vars)) {
			//console.log('pn loads default graph');
			uri = 'defaultGraph?';
			if ('graphIncludes' in url.vars) {
				uri += next_char + 'graphIncludes=' + url.vars['graphIncludes'];
				next_char = '&';
			}
			
		}

		if ('searchTerm' in url.vars) {
			uri += next_char + 'searchTerm=' + url.vars['searchTerm'];
			next_char = '&';
		}
		getData(uri, graph.drawGraph);
		
		


	}




	function getData(dataIdentifier, callback) {
		//console.log('getData called');
		//console.log(localStorage.dataIdentifier);

		function addToCacheAndDo(data) {
			//console.log('addToCacheAndDo called');
			localStorage[dataIdentifier] = data;
			//console.log(data);
			callback(data);
		}

		if (dataIdentifier in localStorage && !testingOverride) {
			//console.log('Data loaded from cache');
			//console.log(localStorage[dataIdentifier]);
			callback(localStorage[dataIdentifier]);
		}
		else {
			//console.log('Data ajaxed in');
			//console.log("http://localhost:5000/ajax/" + dataIdentifier);
			$.ajax({
	    		url: "http://localhost:5000/ajax/" + dataIdentifier 
	    	}).done(addToCacheAndDo);
	    }
	}





	




	return {
		url: url,
		getData: getData,
		initialise: initialise,
		callFromUrl: callFromUrl
	}
});