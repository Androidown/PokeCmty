
var colorMap = [
    "144,153,161", "206,64,105", "143,168,221", "171,106,200", "217,119,70", "199,183,139", 
    "144,193,44", "82,105,172", "90,142,161", "255,156,84", "77,144,213", "99,187,91", 
    "243,210,59", "249,113,118", "116,206,192", "10,109,196", "90,83,102", "236,143,230"
];

try {
    type_id = Number(document.getElementById('type_id').textContent);
} catch (TypeError) {
    type_id = 0;
}

for (var cls of document.querySelectorAll('.type-color-fill')) {
    cls.style.fill = `rgb(${colorMap[type_id]})`;
};

for (var cls of document.querySelectorAll('.type-color-bg')) {
    cls.style.backgroundColor = `rgb(${colorMap[type_id]})`;
};

for (var cls of document.querySelectorAll('.type-color')) {
    cls.style.color = `rgba(${colorMap[type_id]},.8)`;
};

for (var i=0; i<colorMap.length; i++) {
    for (var cls of document.querySelectorAll(`.type-color-bg-${i}`)) {
        cls.style.backgroundColor = `rgba(${colorMap[i]},.8)`;
        // cls.style.fill = 'red';
    };
}
