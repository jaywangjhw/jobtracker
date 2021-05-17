/* Source Citation: https://docs.djangoproject.com/en/3.2/ref/csrf/
   This is how the Django documentation recoommends acquiring a CSRF
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

	$("#existing-company-fill").click(function(e) { 
	    
	    e.stopPropagation();
	    var target_url = $(this).attr('name');
	    var app_url = $("#existing-company-app-url").val();
	    
	    if($('#existing-company-app-url')[0].checkValidity()) {
	        var csrftoken = getCookie('csrftoken');

	        $.ajax({
	            type: "GET",
	            url: target_url,
				data: { 
					company_id: $("#id_company").val(), 
					app_url: app_url 
				},
	            success : function(response) {
					if("company_message" in response) {
	        		$("#existing-company-app-url").after('<div class="alert alert-warning mt-1" role="alert">' + 
	        				response.company_message + '</div>');
	        		}
	                if("job_description" in response) {
	                	$("#id_job_description").val(response.job_description).addClass("btn-outline-success");
	                }

	                if("position_title" in response) {
	                	$("#id_position_title").val(response.position_title).addClass("btn-outline-success");
	                }      		
	        	}
	        })  	
	    }
	    else {
	    	$('#existing-company-app-url')[0].reportValidity();
	    }
	});

	$("#Non-Existing-fill").click(function(e) { 
	    
	    e.stopPropagation();
	    var target_url = $(this).attr('name');
	    var app_url = $("#non-existing-app-url").val();
	    
	    if($('#non-existing-app-url')[0].checkValidity()) {
	        var csrftoken = getCookie('csrftoken');

	        $.ajax({
	            type: "GET",
	            url: target_url,
				data: { 
					app_url: app_url 
				},
	            success : function(response) {
					if("company_message" in response) {
	        		$("#existing-company-app-url").after('<div class="alert alert-warning mt-1" role="alert">' + 
	        				response.company_message + '</div>');
	        		}
	                if("job_description" in response) {
	                	$("#id_job_description").val(response.job_description).addClass("btn-outline-success");
	                }

	                if("position_title" in response) {
	                	$("#id_position_title").val(response.position_title).addClass("btn-outline-success");
	                }      		
	        	}
	        })  	
	    }
	    else {
	    	$('#existing-company-app-url')[0].reportValidity();
	    }
	});

});

