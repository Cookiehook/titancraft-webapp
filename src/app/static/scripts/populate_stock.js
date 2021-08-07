$(document).ready(function () {
    let itemstacks = JSON.parse(document.getElementById('itemstack-data').textContent);
    for (var i = 1; i < itemstacks.length + 1; i++) {
        $('#stock_item_' + i).val(itemstacks[i - 1]['item']).trigger('chosen:updated');
        $('#stock_stack_size_' + i).val(itemstacks[i - 1]['stack_size']);
        $('#stock_description_' + i).val(itemstacks[i - 1]['description']);

        if (itemstacks[i - 1]['label_type'] === "enchantment") {
            $('#enchantments_' + i).val(itemstacks[i - 1]['labels']).trigger('chosen:updated');
        } else if (itemstacks[i - 1]['label_type'] === "potion") {
            $('#potions_' + i).val(itemstacks[i - 1]['labels']).trigger('chosen:updated');
        }

        if (i !== itemstacks.length) {  // Prepare the next fieldset
            $(".add-fieldset").trigger('click')
        }
    }
});