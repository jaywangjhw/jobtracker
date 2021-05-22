// Get the parameters for Reddit feed for GET request
$(document).ready(function(){
	$("#submit_search").click(function() {

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

		var url = jQuery.param(params); 

		$.get("?" + url, function(data){
			console.log(url)
		}); 
	});
});
