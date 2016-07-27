var panelManager = (function(router) {
	var panel = $('.panel');
	

	$('#showPanel').click(function() {
		panel.toggleClass('show');
	});


	$('#graphIncludeSubmit').click(function() {
		var repoIncluded = $('#graphIncludeRepo').is(':checked');
		if (repoIncluded) {
			router.url.setVar('graphIncludes', 'repo');
		}
		else {
			router.url.removeVar('graphIncludes');
		}
		router.getGraph(router.url.vars);
	});

	return {
		panel: panel
	}
});