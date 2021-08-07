$(document).ready(function () {
    /*
        item_counter is used to track the number of item boxes on screen, so we don't delete the last one
        item_number is used to create unique name/IDs on each record. This is never decremented, to ensure
        the value is always unique. Eg: A user could create 4 items, then delete #2, leaving us with 1,3,4.
        If we used decremented item_counter for the ID, the next created item would be #4, conflicting with
        the existing #4, making the form unusable server-side
     */
    let item_counter = 1;
    let item_number = 1;

    // Clone the item-fieldset group to allow multiple items on a stock record
    $(".add-fieldset").click(function (event) {
        item_counter++;
        item_number++;
        event.preventDefault();
        $("select").chosen("destroy");  // Required to keep the 'chosen' select elements working
        let clone = $(".item-fieldset").first().clone();
        clone.find("input").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + item_number);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + item_number);
            }
        )
        clone.find("select").each(function () {
                $(this).attr('name', $(this).attr("name").slice(0, -1) + item_number);
                $(this).attr('id', $(this).attr("id").slice(0, -1) + item_number);
            }
        )
        clone.appendTo(".item-wrapper");
        $("select").chosen();
    });

    // Remove an item-fieldset group, for accidental clicks / changed mind
    $(".item-wrapper").on("click", ".remove-fieldset", function (event) {
        if (item_counter !== 1) {
            event.preventDefault();
            $(this).parent().remove();
            item_counter--;
        }
    })
});