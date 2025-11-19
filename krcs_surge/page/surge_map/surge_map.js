frappe.pages['surge-map'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({ parent: wrapper, title: 'Operational Surge Map', single_column: true });
    $(page.body).html('<div id="map" style="height: 80vh; width: 100%;"></div>');
    
    var map = L.map('map').setView([0.0236, 37.9062], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map);

    frappe.call({
        method: "krcs_surge.page.surge_map.surge_map.get_county_data",
        callback: function(r) {
            var data = r.message;
            $.getJSON("/assets/krcs_surge/js/kenya_counties.json", function(geoJson) {
                L.geoJson(geoJson, {
                    style: function(feature) {
                        var count = data[feature.properties.COUNTY_NAM] || 0;
                        return { fillColor: count > 100 ? '#800026' : '#FFEDA0', weight: 1, fillOpacity: 0.7 };
                    },
                    onEachFeature: function(feature, layer) {
                        layer.bindPopup(feature.properties.COUNTY_NAM + ": " + (data[feature.properties.COUNTY_NAM] || 0));
                    }
                }).addTo(map);
            });
        }
    });
}