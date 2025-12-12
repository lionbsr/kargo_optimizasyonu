// Harita oluştur
var map = L.map('map').setView([40.766, 29.940], 10);

// OpenStreetMap katmanı
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

// Örnek istasyonlar (İlçe merkezleri)
var stations = [
    [40.766, 29.916], // İzmit
    [40.750, 29.960], // Kartepe
    [40.770, 29.510]  // Gebze
];

// Marker ekle
stations.forEach(function(coord) {
    L.marker(coord).addTo(map);
});

// Rota çiz (kuş uçuşu DEĞİL, yol benzeri polyline)
L.polyline(stations, { color: 'blue' }).addTo(map);
