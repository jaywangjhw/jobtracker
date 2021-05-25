// Search for company in the list of all companies
$(document).ready(function(){
	$("#listSearch").keyup(function() {
		// make the search case insensitive
		var searchStr = $(this).val().toLowerCase();
		// hide any rows in the company table that do not match this search
		$("#itemTable tr").filter(function() {
	  	$(this).toggle($(this).text().toLowerCase().indexOf(searchStr) > -1)
		});
	});

	$('.make-row-clickable').click(function () {
	    $.ajax({
	        url: $(this).closest('tr').data('link'),
	        success: function (response) {
	            console.log(response.name)
	            $( "h2.company-name" ).replaceWith( "<h2 class='company-name'>" + response.name + "</h2>" );
	            
	            if(response.careers_url) {
		            $( "p.company-url" ).replaceWith( "<p class='company-url'>Careers Link: " 
		            	+ response.careers_url + "</p>" );	            	
	            } 
	            else {
		            $( "p.company-url" ).replaceWith( "<p class='company-url'>Update this Company to add a Careers Link</p>" );	
	            }

	            if(response.industry) {
	            	$( "p.company-industry" ).replaceWith( "<p class='company-industry'>Industry: "
	            	 	+ response.industry + "</p>" );	            	
	            }
	            else {
	            	$( "p.company-industry" ).replaceWith( "<p class='company-industry'>Update this Company to add an Industry</p>" );	 	            	
	            }

	            $( "a" ).removeClass( "invisible" ).addClass( "visible" );
	            $("a.edit-company").attr("href", "/companies/edit/" + response.id);
	            $("a.delete-company").attr("href", "/companies/delete/" + response.id);
	           	$("a.positions-company").attr("href", "/companies/" + response.id);
	            $("a.add-position").attr("href", "/positions/new?company=" + response.id);
	        },
	        error: function (response) {
	            console.log(response.responseJSON.errors)
	        }
	    });

	    return false;
	});
});
