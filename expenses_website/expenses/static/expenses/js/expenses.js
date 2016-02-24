$(document).ready(function(){
    $('#id_category').on('change', function(){
        var input=$(this);
        var value=input.val();
        if (value){
            input.removeClass("invalid").addClass("valid");
        }
        else {
            input.removeClass("valid").addClass("invalid");
        }
    });
    $('#id_description').on('input', function(){
        var input=$(this);
        var value=input.val();
        if (value){
            input.removeClass("invalid").addClass("valid");
        }
        else {
            input.removeClass("valid").addClass("invalid");
        }
    });
    $("#id_price").on('input', function() {
        var input=$(this);
        var value=input.val();
        if (value){
            input.removeClass("invalid").addClass("valid");
        }
        else {
            input.removeClass("valid").addClass("invalid");
        }
    });
    // taken from https://formden.com/blog/validate-contact-form-jquery
    $("#expense_submit").click(function(event){
        // Don't need to validate the date fields, they have defaults
        $("#id_purchase_date_month").addClass("valid");
        $("#id_purchase_date_day").addClass("valid");
        $("#id_purchase_date_year").addClass("valid");
        // Likewise CSRF token and all hidden fields should be valid
        // This doesn't actually work for csrf token !! :-(
        $("input:hidden").addClass("valid");

        var form_data=$("#expense").serializeArray();
        var error_free=true;
        for (var input in form_data){
            var element=$("#id_"+form_data[input]['name']);
            // Ignore csrf token, all attempts at adding valid to it have failed
            if (element.selector == '#id_csrfmiddlewaretoken'){continue;}
            var valid=element.hasClass("valid");
            var error_element=$("span", element.parent());
            if (!valid){
                error_element.removeClass("error").addClass("error_show");
                error_free=false;
            }
            else{error_element.removeClass("error_show").addClass("error");}
        }
        if (!error_free){
            event.preventDefault();
            alert("Errors: Form will not be submitted")
        }
        else{
            alert('No errors: Form will be submitted');
        }
    });
});
