var panelManager = (function() {
	var panel = $('.panel');
	var repoIncludedCheckbox = $('#graphIncludeRepo');

	// Setup from URL:

	if (router.url.getVar('graphIncludes')=='repo') {
		repoIncludedCheckbox.prop('checked', true);
	}
	

	$('#showPanel').click(function() {
		panel.toggleClass('show');
	});


	$('#graphIncludeSubmit').click(function() {
		console.log(router);
		var repoIncluded = $('#graphIncludeRepo').is(':checked');
		console.log("repo included", repoIncluded);
		if (repoIncluded) {
			console.log('setting urlvar');
			router.url.setVar('graphIncludes', 'repo');
			
		}
		else {
			router.url.removeVar('graphIncludes');
			console.log('panel remove var', router.url.vars);
		}
		console.log('panel getvar (before getgraph)', router.url.getVar('graphIncludes'));
		router.getGraph();
	});

	return {
		
	}
});