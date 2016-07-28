var panelManager = (function() {
	var panel = $('.panel');
	var repoIncludedCheckbox = $('#graphIncludeRepo');

	// Setup from URL:

	if (router.url.getVar('graphIncludes')=='repo') {
		repoIncludedCheckbox.prop('checked', true);
	}


	if (router.url.getVar('searchTerm')) {
		var searchTerms = router.url.getVar('searchTerm').split('|');
		var searchBoxesString = '';
		for (var i in searchTerms) {
			searchBoxesString += '<p><input type="text" name="searchTerm" class="searchTermInput" value="'+searchTerms[i]+'"/> <button class="removeSearchField">-</button></p>'
		}
		$('#searchFields').html(searchBoxesString);
		bindRemoveButtonListener();
	}
	

	$('#showPanel').click(function() {
		panel.toggleClass('show');
	});

	$('#searchTermAdd').click(function() {
		$('#searchFields').append('<p><input type="text" name="searchTerm" class="searchTermInput"/> <button class="removeSearchField">-</button></p>')
		bindRemoveButtonListener();
	});

	function bindRemoveButtonListener() {
		$('.removeSearchField').click(function(){
			$(this).parent('p').remove();
		});
	}

	$('#graphIncludeSubmit').click(function() {
		//console.log(router);
		var repoIncluded = $('#graphIncludeRepo').is(':checked');
		//console.log("repo included", repoIncluded);
		if (repoIncluded) {
			//console.log('setting urlvar');
			router.url.setVar('graphIncludes', 'repo');
			
		}
		else {
			router.url.removeVar('graphIncludes');
			//console.log('panel remove var', router.url.vars);
		}
		//console.log('panel getvar (before getgraph)', router.url.getVar('graphIncludes'));
		router.getGraph();
	});

	$('#searchTermSubmit').click(function() {
		var searchFields = $('.searchTermInput');
		var searchTermsString = '';
		searchFields.each(function(field) {
			if ($(this).val() != '') {
				searchTermsString += $(this).val() + '|';
			}
		});
		searchTermsString = searchTermsString.slice(0, -1);

		router.url.setVar('searchTerm', searchTermsString);
		router.getGraph();


	});

	return {
		
	}
});