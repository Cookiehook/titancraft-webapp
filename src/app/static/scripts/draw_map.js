function relativeToSpawn(region, points) {
    console.log(points)
    let map_centre = 250
    var points_corrected = []
    console.log(region)
    for (let i = 0; i < points.length; i++) {
        console.log(points[i])
        points_corrected.push(points[i]['x_pos'] - region.x_pos + map_centre)
        points_corrected.push(points[i]['z_pos'] - region.z_pos + map_centre)
    }
    return points_corrected
}

$(document).ready(function () {
    let paths = JSON.parse(document.getElementById('paths-data').textContent);
    let region = JSON.parse(document.getElementById('region-data').textContent);

    let draw = SVG().addTo('#map').viewbox(0, 0, 500, 500);
    for (let i = 0; i < paths.length; i++) {
        draw.polyline(relativeToSpawn(region, paths[i]['points']))
    }

})