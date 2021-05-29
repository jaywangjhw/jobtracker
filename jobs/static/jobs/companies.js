// Search for company in the list of all companies
$(document).ready(function(){
	$("#listSearch").keyup(function() {
	    // make the search case insensitive
	    var searchStr = $(this).val().toLowerCase();
	    // hide any rows in the company table that do not match this search
	    $(".searchable").each(function() {
	        if ($(this).text().toLowerCase().indexOf(searchStr) != -1) {
	            $(this).show();
	        }
	        else {
	            $(this).hide();  
	        }
	    });	    
	});
});
