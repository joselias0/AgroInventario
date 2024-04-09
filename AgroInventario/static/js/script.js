var fechaInicioInput = document.getElementById('fecha_inicio');
var fechaFinInput = document.getElementById('fecha_fin');
if (localStorage.getItem('fecha_inicio')) {
    fechaInicioInput.value = localStorage.getItem('fecha_inicio');
}
if (localStorage.getItem('fecha_fin')) {
    fechaFinInput.value = localStorage.getItem('fecha_fin');
}

document.getElementById('btn2').addEventListener('click', function () {
    localStorage.setItem('fecha_inicio', fechaInicioInput.value);
    localStorage.setItem('fecha_fin', fechaFinInput.value);
});


function botonEliminar(id_per) {
    if (confirm('¿Estás seguro de que deseas eliminar este objeto?')) {
        window.location.href = `/borrar/${id_per}`;
    }
}
