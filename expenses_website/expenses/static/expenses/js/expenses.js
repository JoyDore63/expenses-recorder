$(document).ready(function(){
    // for each of the input fields,
    //   if value was entered
    //     set to valid and disable error message
    //   else (no value has been input)
    //     set error message to show and flag as invalid
    $('#id_category').on('input', function(){
        var input=$(this);
        var value=input.val();
        var error_element=$("span", $(this).parent());
        if (value){
            input.removeClass("invalid").addClass("valid");
            error_element.removeClass("error_show").addClass("error");
        }
        else {
            input.removeClass("valid").addClass("invalid");
            error_element.removeClass("error").addClass("error_show");
        }
    });
    $('#id_description').on('input', function(){
        var input=$(this);
        var value=input.val();
        var error_element=$("span", $(this).parent());
        if (value){
            input.removeClass("invalid").addClass("valid");
            error_element.removeClass("error_show").addClass("error");
        }
        else {
            input.removeClass("valid").addClass("invalid");
            error_element.removeClass("error").addClass("error_show");
        }
    });
    $("#id_price").on('input', function() {
        var input=$(this);
        var value=input.val();
        var error_element=$("span", $(this).parent());
        if (value){
            input.removeClass("invalid").addClass("valid");
            error_element.removeClass("error_show").addClass("error");
        }
        else {
            input.removeClass("valid").addClass("invalid");
            error_element.removeClass("error").addClass("error_show");
        }
    });
    // taken from https://formden.com/blog/validate-contact-form-jquery
    // If the form changes, check if we can enable submit button
    $("#expense").change(function(event){
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
            // Ignore csrf token, attempts at adding valid to it have failed
            if (element.selector == '#id_csrfmiddlewaretoken'){continue;}
            var valid=element.hasClass("valid");
            var error_element=$("span", element.parent());
            if (!valid){
                error_free=false;
            }
        }
        if (!error_free){
            $("#expense_submit").addClass("disabled");
        }
        else{
            $('#expense_submit').removeClass("disabled");
        }
    });
});
