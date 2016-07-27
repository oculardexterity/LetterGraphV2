var letterManager = (function(config) {



    console.log(config);



  
    $(config['closeLetterDiv']).click(function(e) {
    	if (e.target !== this) {
    		return;
    	}
    	closeLetter();
    });



	function showLetterContent(data) {
		var container = '.letterContainer';
		$(config['closeLetterDiv']).show();

		$(config['closeLetterDiv']).html(data).show();
		$('.console').hide();

		$(window).resize(function() {
			var windowHeight = $(window).height();
			var containerHeight = $(container).outerHeight();
			var leftPos = ($(window).width() - $(container).outerWidth())/2;
			if (containerHeight > windowHeight) {
				$(container).css({
					position: 'absolute',
					height: windowHeight - 120,
					top: 15,
					left: leftPos
				});
			}	
			else {		
			
				$(container).css({
					position:'absolute',
					left: leftPos,
					top: (windowHeight - containerHeight)/2

				});
			}
			
			if ($('.personBubble.sent').length) {
				$('.personBubble.sent').css({
					position: 'absolute',
					left: (leftPos / 2) - ($('.personBubble.sent').outerWidth()/2),
					top: windowHeight/2 - ($('.personBubble.sent').outerWidth()/2) - 60,
					zIndex: 6,
					height: $('.personBubble.sent').outerWidth()
				});
				$('.personBubble.sent .inner').css({
					top: $('.personBubble.sent').outerWidth()/2 - $('.personBubble.sent .inner').height()/2
				});
				$('.personBubble.sent .arrow').css({
					left: $('.personBubble.sent').innerWidth(),
					width: leftPos - ($('.personBubble.sent').outerWidth() + $('.personBubble.sent').offset().left) - 5
				});
			}
	
			if ($('.personBubble.received').length) {
				$('.personBubble.received').css({
					position: 'absolute',
					left: leftPos + $(container).innerWidth() + (leftPos / 2) - ($('.personBubble.sent').outerWidth()/2),
					top: windowHeight/2 - ($('.personBubble.received').outerWidth()/2) - 60,
					height: $('.personBubble.received').outerWidth()
				});
				$('.personBubble.received .inner').css({
					top: $('.personBubble.received').outerWidth()/2 - $('.personBubble.received .inner').height()/2
				});
				$('.personBubble.received .arrow').css({
					width: $('.personBubble.received').offset().left - (leftPos + $(container).outerWidth()) -6,
					left: - ($('.personBubble.received').offset().left - (leftPos + $(container).outerWidth()) +1)
				});
			}

		});

		$('#graphContainer').addClass('blur');
		$('#panel').addClass('blur');
		$('.letterContainer').removeClass('blur');

		// To initially run the function:
		$(window).resize();
	}


	function closeLetter() {
		//console.log('closeletterclicked');
		$(config['closeLetterDiv']).hide();
		$(config['container']).hide();
		$('#graphContainer').removeClass('blur');
		$('#panel').removeClass('blur');
		$('.letterContainer').addClass('blur');
		$('.console').show();
		router.url.removeVar('letter');
	};
 
 	return {
 		showLetterContent: showLetterContent,
 		closeLetter: closeLetter
 	}
  
});