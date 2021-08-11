function locationSpawnOffset(region, location) {
    let scale_factor = 1.77
    let x_pos = (location['x_pos'] - region['x_pos']) * scale_factor
    let z_pos = (location['z_pos'] - region['z_pos']) * scale_factor
    return {
        "x_pos": x_pos,
        "z_pos": z_pos,
    }
}


$(document).ready(function () {
    let region_data = JSON.parse(document.getElementById('region-data').textContent);
    let location_data = JSON.parse(document.getElementById('location-data').textContent);
    let map_width = 631
    let map_height = 948
    let x_origin = map_width * 0.542789
    let z_origin = map_height * 0.56698

    let svg = SVG().addTo('.content').viewbox(0, 0, map_width, map_height)

    for (let i = 0; i < location_data.length; i++) {
        let position = locationSpawnOffset(region_data, location_data[i])
        let loc = svg.circle(6).center(position['x_pos']  + x_origin, position['z_pos'] + z_origin)
        loc.attr({"name": location_data[i]["name"]})

        loc.mouseenter(function () {
            this.radius(6)
            console.log(this.attr('name'))
        })

        loc.mouseout(function () {
            this.radius(3)
        })
        locations.push(loc)
    }
})