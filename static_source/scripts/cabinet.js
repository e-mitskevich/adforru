
$(document).ready(function() {

    $(".confirm").on("click", function(e) {
        return confirm("Вы уверены?");
    });

    setTimeout(function() {
        $("#messages").hide();
    }, 3000);

});
