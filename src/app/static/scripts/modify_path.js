$(document).ready(function () {
    let point_counter = 1;
    $(function () {
        $("#sortable").sortable();
        $("#sortable").disableSelection();
    });

    // Clone the fieldset group to allow multiple points on a path
    $(".add-fieldset").click(function (event) {
        point_counter++;
        event.preventDefault();
        let clone = $(".point-fieldset").first().clone();
        clone.find("input").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + point_counter);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + point_counter);
            }
        )
        clone.appendTo(".point-wrapper");
    });

    // Remove an fieldset group, for accidental clicks / changed mind
    $(".point-wrapper").on("click", ".remove-fieldset", function (event) {
        if (point_counter !== 1) {
            event.preventDefault();
            $(this).parent().remove();
            point_counter--;
        }
    })
});


$(document).ready(function () {
    $("form").on("submit", function (event) {
        let counter = 1;

        let fieldsets = $(".point-fieldset");
        fieldsets.each(function () {
            $(this).find("#x_pos").first().attr('name', 'x_pos_' + counter);
            $(this).find("#z_pos").first().attr('name', 'z_pos_' + counter);
            counter++;
        })
    })
})