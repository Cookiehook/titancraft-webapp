function locationSpawnOffset(region, location) {
    return {
        "x_pos": location['x_pos'] - region['x_pos'],
        "z_pos": location['z_pos'] - region['z_pos'],
    }
}

function polylineSpawnOffset(region, points) {
    var points_corrected = []
    for (let i = 0; i < points.length; i++) {
        points_corrected.push(points[i]['x_pos'] - region.x_pos)
        points_corrected.push(points[i]['z_pos'] - region.z_pos)
    }
    return points_corrected
}


$(document).ready(function () {
    let map_width = 250
    let paths = JSON.parse(document.getElementById('paths-data').textContent);
    let region = JSON.parse(document.getElementById('region-data').textContent);
    let locations = JSON.parse(document.getElementById('location-data').textContent);

    // TODO - Make this dependent on map size. Maybe allow zoom / pan?
    let svg = SVG().addTo('#map').viewbox(0, 0, map_width*2, map_width*2);

    // Draw paths relative to region centre, then move into map
    for (let i = 0; i < paths.length; i++) {
        let path = svg.polyline(polylineSpawnOffset(region, paths[i]['points']))
        path.center(map_width + path.cx(), map_width + path.cy())
        path.attr("name", paths[i]["name"])
    }

    // Draw location dots relative to region centre, then move into map
    for (let i = 0; i < locations.length; i++) {
        let position = locationSpawnOffset(region, locations[i])
        let loc = svg.circle(3).center(map_width + position['x_pos'], map_width + position['z_pos'])
        loc.attr({"name": locations[i]["name"]})

        // Hover-over details
        loc.mouseenter(function() {
            this.radius(3)
            console.log(this.attr('name'))
        })

        // destroy hover-over element
        loc.mouseout(function() {
            this.radius(1.5)
        })
    }
})