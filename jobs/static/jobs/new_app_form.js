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
	            data: $(this).serialize(), //{'csrfmiddlewaretoken': csrftoken, 'app-url': app_url},
	            success : function(response) {
	                $("#id_name").val(response.company);
	                $("#id_position_title").val(response.position_title);
	                $("#id_job_description").val(response.job_description);
	                $("#id_position_url").val(app_url);
	            }
	        })
	    });
});

