document.addEventListener('DOMContentLoaded', function () {
    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('archivo_excel');
    let draggedFile = null;

    // Evento de clic en el cuadro de carga para activar el input file
    uploadBox.addEventListener('click', function () {
        fileInput.click();
    });

    // Añadir eventos para arrastrar y soltar
    uploadBox.addEventListener('dragover', function (event) {
        event.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', function () {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', function (event) {
        event.preventDefault();
        uploadBox.classList.remove('dragover');
        draggedFile = event.dataTransfer.files[0];
        handleFile(draggedFile);
    });

    // Manejar el cambio de archivo seleccionado
    fileInput.addEventListener('change', function (event) {
        draggedFile = null;  // Resetea el archivo arrastrado cuando se selecciona uno nuevo
        const file = event.target.files[0];
        console.log('File selected via click:', file);  // Depuración
        handleFile(file);
    });

    function handleFile(file) {
        if (file) {
            const allowedExtensions = /(\.xlsx|\.xls)$/i;
            if (!allowedExtensions.exec(file.name)) {
                Swal.fire('Error', 'El archivo seleccionado no es un archivo Excel.', 'warning');
                fileInput.value = '';  // Limpiar el input file
                return;
            }
            uploadBox.querySelector('p').innerText = file.name;

            const formData = new FormData();
            formData.append('archivo', file);

            // Enviar archivo al servidor para procesamiento
            fetch("/Prediccion/procesar_excel/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response data:', data);  // Depuración
                if (data.success) {
                    document.getElementById('fecha_inicio').value = new Date(data.fecha_inicio).toISOString().split('T')[0];
                    document.getElementById('fecha_fin').value = new Date(data.fecha_fin).toISOString().split('T')[0];
                    document.getElementById('periodo_academico').value = data.periodo_academico_id;

                    const historicoTableBody = document.getElementById('historico-table-body');
                    historicoTableBody.innerHTML = ''; // Limpiar tabla antes de agregar nuevos datos

                    data.historico.forEach(row => {
                        const newRow = `
                            <tr>
                                <td>${row.ciclo}</td>
                                <td>${row.matriculados}</td>
                                <td>${row.aprobados}</td>
                                <td>${row.reprobados}</td>
                                <td>${row.abandonaron}</td>
                                <td>${row.desertores}</td>
                            </tr>`;
                        historicoTableBody.innerHTML += newRow;
                    });

                    Swal.fire({
                        icon: 'success',
                        title: 'Archivo procesado',
                        text: data.message,
                        showConfirmButton: false,
                        timer: 1500
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: data.message,
                        showConfirmButton: false,
                        timer: 1500
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema con la solicitud.',
                    showConfirmButton: false,
                    timer: 1500
                });
            });
        }
    }

    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevenir el envío del formulario por defecto

        const malla = document.getElementById('malla_curricular').value;
        const file = fileInput.files[0] || draggedFile;  // Usa el archivo arrastrado si no hay uno seleccionado

        if (!malla) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Seleccione una Malla Curricular.',
                showConfirmButton: false,
                timer: 1500
            });
            return;
        }

        if (!file) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Seleccione un archivo Excel.',
                showConfirmButton: false,
                timer: 1500
            });
            return;
        }

        const formData = new FormData(form);
        if (draggedFile) {
            formData.append('archivo_excel', draggedFile);  // Añadir el archivo arrastrado si existe
        }

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Submit response data:', data);  // Depuración
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Datos importados',
                    text: data.message,
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.href = "/Prediccion/administracion_periodo/";
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.message,
                    showConfirmButton: false,
                    timer: 1500
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Hubo un problema con la solicitud.',
                showConfirmButton: false,
                timer: 1500
            });
        });
    });
});
