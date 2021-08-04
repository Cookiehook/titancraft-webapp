$(document).ready(function () {
    let farm_records = JSON.parse(document.getElementById('farm-data').textContent);
    let mob_counter = 1;
    let item_counter = 1;
    let total_mobs = 0;
    let total_items = 0;
    for (let i = 0; i < farm_records.length; i++) {
        if (farm_records[i]['label_type'] === "mob") {
            total_mobs ++;
        } else {
            total_items++;
        }
    }
    for (let i = 0; i < farm_records.length; i++) {
        if (farm_records[i]['label_type'] === "mob") {
            $('#mob_' + mob_counter).val(farm_records[i]['label']).trigger('chosen:updated');
            $('#xp_' + mob_counter).prop("checked", farm_records[i]['xp']);
            if (mob_counter < total_mobs) {
                $(".add-mob-fieldset").first().trigger('click');
                mob_counter++;
            }

        } else {
            $('#item_' + item_counter).val(farm_records[i]['label']).trigger('chosen:updated');
            if (item_counter < total_items) {
                $(".add-item-fieldset").first().trigger('click');
                item_counter++;
            }
        }
    }
});