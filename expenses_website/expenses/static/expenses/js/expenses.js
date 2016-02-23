$(document).ready(function(){
    // want to detect when might have entered some data
    $("input, select").on({
        focusout: function(){
            $(this).css("background-color", "yellow");
            // TODO make this conditional on validation
            // also needs to only apply to the Create button,
            // not other submit buttons on other pages
            $("input[type=submit]").removeAttr('disabled');
        }
    });
});
