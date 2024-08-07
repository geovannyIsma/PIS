let dataTable;
let dataTableIsInitialized = false;
let mallaIdToDelete = null;

const dataTableOptions = {
    columnDefs: [
        {className: "text-center align-middle", targets: [0, 1, 2, 3, 4]},
        {orderable: false, targets: [0, 4]},
        {searchable: false, targets: [0, 4]}
    ],
    pageLength: 10,
    destroy: true,
    dom: 'Bfrtip',
    buttons: [
        {
            extend: 'copy',
            text: '<i class="fa-solid fa-copy"></i> Copiar',
            className: 'btn btn-copy'
        },
        {
            extend: 'csv',
            text: '<i class="fa-solid fa-file-csv"></i> CSV',
            className: 'btn btn-csv'
        },
        {
            extend: 'excel',
            text: '<i class="fa-regular fa-file-excel"></i> Excel',
            className: 'btn btn-excel'
        },
        {
            extend: 'pdf',
            text: '<i class="fa-solid fa-file-pdf"></i> PDF',
            className: 'btn btn-pdf'
        },
        {
            extend: 'print',
            text: '<i class="fa-solid fa-print"></i> Imprimir',
            className: 'btn btn-print'
        }
    ],
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "No se encontraron registros de mallas curriculares",
        info: "Página _PAGE_ de _PAGES_",
        infoEmpty: "No hay registros disponibles",
        infoFiltered: "(filtrado de _MAX_ registros totales)",
        search: "Buscar:",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await list_mallas();
    dataTable = $('#datatable-mallas').DataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

const list_mallas = async () => {
    try {
        const response = await fetch('/Prediccion/list_malla/');
        const data = await response.json();
        let content = ``;
        data.mallas_Curricular.forEach((mallaCurricular, index) => {
            content += `
                <tr>
                    <td class="text-center align-middle">${index + 1}</td>
                    <td class="text-center align-middle">${mallaCurricular.codigo}</td>
                    <td class="text-center align-middle">${mallaCurricular.nombre_malla}</td>
                    <td class="text-center align-middle">${mallaCurricular.tituloOtorgado}</td>
                    <td class="text-center align-middle">
                        <button class='btn btn-sm btn-primary' onclick='editMalla(${mallaCurricular.id})'>
                            <i class='fa-solid fa-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger' onclick='showDeleteModal(${mallaCurricular.id})'>
                            <i class='fa-solid fa-trash-can'></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        document.getElementById('tableBody_mallas').innerHTML = content;
    } catch (ex) {
        Swal.fire("Error", ex, "error");
    }
};

const deleteMalla = async (mallaId) => {
    try {
        const response = await fetch(`/Prediccion/eliminar_malla/${mallaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            await initDataTable();
            $('#deleteModal').modal('hide');
        } else {
            Swal.fire("Error", "No se pudo eliminar la malla curricular", "error");
        }
    } catch (ex) {
        Swal.fire("Error", ex, "error");
    }
};

const showDeleteModal = (mallaId) => {
    mallaIdToDelete = mallaId;
    $('#deleteModal').modal('show');
};

const confirmDelete = () => {
    if (mallaIdToDelete) {
        deleteMalla(mallaIdToDelete);
    }
};

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

window.addEventListener("load", async () => {
    await initDataTable();
    document.getElementById('confirmDelete').addEventListener('click', confirmDelete);
});

function editMalla(mallaId) {
    window.location.href = `/Prediccion/editar_malla/${mallaId}`;
}