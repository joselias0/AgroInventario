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

function botonEliminar1(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este objeto?')) {
    window.location.href = `/borrar_tamano/${id}`;
    }
}

function abrir_modal_edicion(url){
  $('#edit_tamaño').load(url, function(){
    $(this).modal('show');
  });
}

function abrir_modal_tamano(url){
  $('#add_tamano').load(url, function(){
    $(this).modal('show');
  });
}

function abrir_modal_inventario(url){
  $('#add_inventario').load(url, function(){
    $(this).modal('show');
  });
}

function abrir_modal_edit_lote(url){
  $('#edit_lote').load(url, function(){
    $(this).modal('show');
  });
}

function abrir_modal_add_venta(url){
  $('#add_venta').load(url, function(){
    $(this).modal('show');
  });
}
realizar_cambio
function abrir_modal_r_cambio(url){
  $('#realizar_cambio').load(url, function(){
    $(this).modal('show');
  });
}

function borrar_modal(url){
  $('#borrar').load(url, function(){
    $(this).modal('show');
  });
}

  