document.addEventListener("DOMContentLoaded", function () {

    var map = L.map("map").setView([40.766, 29.916], 10);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19
    }).addTo(map);

    fetch("/stations")
        .then(res => res.json())
        .then(data => {
            data.forEach(s => {
                L.marker([s.lat, s.lon])
                    .addTo(map)
                    .bindPopup(s.name);
            });

            setTimeout(() => map.invalidateSize(), 200);
        });
});
