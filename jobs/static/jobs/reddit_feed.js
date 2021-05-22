// Get the parameters for Reddit feed for GET request
$(document).ready(function(){
 
	
	$("#submit_search").click(function() {

		// $('.accordion-item').remove();

		// Get current parameters from Reddit feed
		var subreddit = $('#input_subreddit').val();
		var query = $('#input_query').val();
		var sort = $('#select_sort').val();
		var results = $('#select_result').val();
		
		var params = {
			subreddit: subreddit,
			query: query,
			sort: sort,
			results: results
		}

		var target_url = ""

		$.ajax({
			type: "GET",
			url: target_url,
			data: params,
			success : function(response) {
				$('.accordion-item').remove();
				console.log(response);
				
				var count = 0;

				for (item in response){

					console.log(item)
					$("#accordionReddit").after('<div class="accordion-item">' +
					'<h2 class="accordion-header">' +
					'<button class="btn btn-secondary btn-lg btn-block" type="button" data-bs-toggle="collapse" data-bs-target="#collapse' + String(count) 
					+ '"aria-expanded="true" aria-controls="collapseOne">' 
					+ response[item].title + '</button>' + '</h2>'
					+ '<div id="collapse' + String(count) + '"class="accordion-collapse collapse" aria-labelledby="heading{{ forloop.counter }}" data-bs-parent="#accordionReddit">'
					+ '<div class="accordion-body">'
					+ response[item].body + '</br>'
					+ response[item].url + '/div'
					+ '</div>' + '</div>');
					
					count++;
				}
			}
		});

	});

});
