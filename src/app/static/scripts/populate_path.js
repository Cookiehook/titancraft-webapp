$(document).ready(function () {
    let path_data = JSON.parse(document.getElementById('path-data').textContent);
    $("#name").val(path_data['name'])
    $('#region').val(path_data['region']).trigger('chosen:updated');

    let points = path_data['points']
    for (var i = 1; i < points.length + 1; i++) {
        $('#x_pos_' + i).val(points[i -1]['x_pos']);
        $('#z_pos_' + i).val(points[i -1]['z_pos']);

        if (i !== points.length) {  // Prepare the next fieldset
            $(".add-fieldset").trigger('click')
        }
    }
});
