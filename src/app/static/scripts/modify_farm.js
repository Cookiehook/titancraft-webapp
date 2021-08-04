$(document).ready(function () {
    let item_counter = 1;
    let item_number = 1;
    let item_wrapper = $(".item-wrapper");

    // Clone the item-fieldset group to allow multiple items on a stock record
    $(".add-item-fieldset").on("click", function (event) {
        event.preventDefault();
        item_counter++;
        item_number++;

        $("select").chosen("destroy");  // Required to keep the 'chosen' select elements working
        let clone = $(".item-fieldset").first().clone();
        clone.find("select").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + item_number);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + item_number);
            }
        )
        clone.appendTo(".item-wrapper");
        $("select").chosen();
    });

    // Remove an item-fieldset group, for accidental clicks / changed mind
    item_wrapper.on("click", ".remove-item-fieldset", function (event) {
        event.preventDefault();
        if (item_counter !== 1) {
            $(this).parent().remove();
            item_counter--;
        } else {
            $('.item-select').val("").trigger("chosen:updated")
        }
    })
});

$(document).ready(function () {
    let mob_counter = 1;
    let mob_number = 1;
    let mob_wrapper = $(".mob-wrapper");

        $(".add-mob-fieldset").on("click", function (event) {
        mob_counter++;
        mob_number++;

        $("select").chosen("destroy");  // Required to keep the 'chosen' select elements working
        let clone = $(".mob-fieldset").first().clone();
        clone.find("select").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + mob_number);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + mob_number);
            }
        )
        clone.find("input").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + mob_number);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + mob_number);
            }
        )
        clone.find('.mob-xp').prop("checked", false);
        clone.appendTo(".mob-wrapper");
        $("select").chosen();
    });

    mob_wrapper.on("click", ".remove-mob-fieldset", function (event) {
        if (mob_counter !== 1) {
            $(this).parent().remove();
            mob_counter--;
        } else {
            $('.mob-select').val("").trigger("chosen:updated")
            $('.mob-xp').prop("checked", false)
        }
    })
});