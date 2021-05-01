// Search for company in the list of all companies
$(document).ready(function(){
	$("#companySearch").keyup(function() {
		// make the search case insensitive
		var searchStr = $(this).val().toLowerCase();
		// hide any rows in the company table that do not match this search
		$("#companyTable tr").filter(function() {
	  	$(this).toggle($(this).text().toLowerCase().indexOf(searchStr) > -1)
		});
	});

	// Allows each row in the company list to become clickable
	//$(".make-row-clickable").click(function() {
	//	window.location.href = $(this).data("link");
	//});


	$('.make-row-clickable').click(function () {
	    $.ajax({
	        url: $(this).closest('tr').data('link'),
	        success: function (response) {
	            console.log(response.name)
	            $( "h2.company-name" ).replaceWith( "<h2 class='company-name'>" + response.name + "</h2>" );
	            $( "p.company-url" ).replaceWith( "<p class='company-url'>Careers Link: " 
	            	+ response.careers_url + "</p>" );
	            $( "p.company-industry" ).replaceWith( "<p class='company-industry'>Industry: "
	            	 + response.industry + "</p>" );
	            $( "a" ).removeClass( "invisible" ).addClass( "visible" );
	            $("a.edit-company").attr("href", "/companies/edit/" + response.id);
	            $("a.delete-company").attr("href", "/companies/delete/" + response.id);
	        },
	        error: function (response) {
	            console.log(response.responseJSON.errors)
	        }
	    });

	    return false;
	});
});
