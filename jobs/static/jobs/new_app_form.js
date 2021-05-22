/* Source Citation: https://docs.djangoproject.com/en/3.2/ref/csrf/
   This is how the Django documentation recommends acquiring a CSRF
   cookie token for AJAX calls, since it cannot be set in the same
   manner as it is within the typical templates.  
   This 'getCookie()' function is taken from the documentation. 
*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
		// When the user submits a job url, this will attempt to fill data from parsing the job
		// description url provided. 
	    $("#new-app-url").submit(function(e){ 
		    
		    e.preventDefault();
		    var target_url = $(this).attr('action');
		    var app_url = $("#app-url").val()
	        var csrftoken = getCookie('csrftoken');

	        $.ajax({
	            type: "GET",
	            url: target_url,
	            data: $(this).serialize(),
	            success : function(response) {
	            	// If there's a position_id, then this position is already being tracked (which means
	            	// the company is already being tracked as well).
	            	if("position_id" in response) {
	            		$("#new-app-url").after('<div class="alert alert-success" role="alert">' + 
	            				response.position_message + '</div>');
	            		// embed the hidden pk's for the position and company.
	            		$("#full-app-form").append('<input type="hidden" id="company_id" name="company_id" value="' + 
	            				response.company_id + '">');
	            		$("#full-app-form").append('<input type="hidden" id="position_id" name="position_id" value="' + 
	            				response.position_id + '">');
	            		// Remove extraneous fields since we already (should) have this data.
	            		$("#div_id_careers_url").remove();
	            		$("#div_id_industry").remove();
	            		$("#div_id_date_opened").remove();
	            		$("#div_id_date_closed").remove();
	            		$("#div_id_skills").remove();
	            		$("#div_id_job_description").remove();
	            	}
	            	// If there is only a company_id, then the company is tracked, but this is a new position.
	            	else if("company_id" in response) {
	            		$("#new-app-url").after('<div class="alert alert-success" role="alert">' + 
	            				response.company_message + '</div>');
	            		$("#new-app-url").after('<div class="alert alert-success" role="alert">' + 
	            				response.position_message + '</div>');
	            		$("#full-app-form").append('<input type="hidden" id="company_id" name="company_id" value="' + 
	            				response.company_id + '">');
	            		$("#div_id_careers_url").remove();
	            		$("#div_id_industry").remove();
	            	}
	            	// If we don't have either company or position id's, then either the url couldn't be
	            	// parsed, or this is a brand new company and position. 
	            	else {
	            		$("#new-app-url").after('<div class="alert alert-warning" role="alert">' + 
	            				response.company_message + '</div>');            		
	            	}

	            	// Insert any values we were able to parse from the url, into the form fields.
	            	if("company" in response) {
	            		$("#id_name").val(response.company).addClass("btn-outline-success");
	            	}

	                if("careers_url" in response) {
	                	$("#id_careers_url").val(response.careers_url).addClass("btn-outline-success");
	                }  

	                if("job_description" in response) {
	                	$("#id_job_description").val(response.job_description).addClass("btn-outline-success");
	                }

	                if("position_title" in response) {
	                	$("#id_position_title").val(response.position_title).addClass("btn-outline-success");
	                }

	                $("#id_position_url").val(app_url).addClass("btn-outline-success");
	            }
	        })
	    });
	
	console.log("Luke's code goes here")

});

