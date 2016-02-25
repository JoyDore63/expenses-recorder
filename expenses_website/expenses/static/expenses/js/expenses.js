$(document).ready(function(){
    function setErrorStatus(field, error_element){
        field.removeClass("valid").addClass("invalid");
        error_element.removeClass("error").addClass("error_show");
    }
    function clearErrorStatus(field, error_element){
        field.removeClass("invalid").addClass("valid");
        error_element.removeClass("error_show").addClass("error");
    }
    function checkValueWasEntered(field){
        var input=$(field);
        var value=input.val();
        // error element is a span with the same parent as input field
        var error_element=$("span", input.parent());
        if (value){
            clearErrorStatus(input, error_element);
            return true;
        }
        else {
            setErrorStatus(input, error_element);
            return false;
        }
    }
    // for each of the input fields,
    //   if value was entered
    //     set to valid and disable error message
    //   else (no value has been input)
    //     set error message to show and flag as invalid
    $('#id_category').on('change', function(){
        checkValueWasEntered(this);
    });
    $('#id_description').on('input', function(){
        checkValueWasEntered(this);
    });
    $("#id_price").on('input', function() {
        entered=checkValueWasEntered(this);
        // Price must also be numeric and within accepted range
        if (entered) {
            var input=$(this)
            var value=input.val();
            var error_element=$("span", input.parent());
            if ($.isNumeric(value) && value > 0 && value < 100){
                clearErrorStatus(input, error_element);
            }
            else {
                setErrorStatus(input, error_element);
            }    
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
