let dataTable;
let dataTableIsInitialized = false;
let usuarioIdToDelete = null;

const dataTableOptions = {
    columnDefs: [
        { className: "text-center align-middle", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
        { orderable: false, targets: [0, 8] },
        { searchable: false, targets: [0, 8] }
    ],
    pageLength: 10,
    destroy: true,
    dom: 'Bfrtip',
    buttons: [
        { extend: 'copy',
            text: '<i class="fa-solid fa-copy"></i> Copiar',
            className: 'btn btn-copy'
        },
        { extend: 'csv',
            text: '<i class="fa-solid fa-file-csv"></i> CSV',
            className: 'btn btn-csv'
        },
        { extend: 'excel',
            text: '<i class="fa-regular fa-file-excel"></i> Excel',
            className: 'btn btn-excel'
        },
        { extend: 'pdf',
            text: '<i class="fa-solid fa-file-pdf"></i> PDF',
            className: 'btn btn-pdf'
        },
        { extend: 'print',
            text: '<i class="fa-solid fa-print"></i> Imprimir',
            className: 'btn btn-print'
        }
    ],
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "No se encontraron registros de usuarios",
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

const formatDateTime = (dateTimeString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    const date = new Date(dateTimeString);
    return date.toLocaleDateString('es-ES', options);
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await list_usuarios();
    dataTable = $('#datatable-usuarios').DataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

const list_usuarios = async () => {
    try {
        const response = await fetch('/Prediccion/list_usuario/');
        const data = await response.json();
        let content = ``;
        data.usuarios.forEach((usuario, index) => {
            content += `
                <tr>
                    <td class="text-center align-middle">${index + 1}</td>
                    <td class="text-center align-middle">${usuario.first_name}</td>
                    <td class="text-center align-middle">${usuario.last_name}</td>
                    <td class="text-center align-middle">${usuario.username}</td>
                    <td class="text-center align-middle">${usuario.email}</td>
                    <td class="text-center align-middle">${usuario.role}</td>
                    <td class="text-center align-middle">${usuario.is_active ? 'Activo' : 'Inactivo'}</td>
                    <td class="text-center align-middle">${formatDateTime(usuario.date_joined)}</td>
                    <td class="text-center align-middle">${formatDateTime(usuario.last_login)}</td>
                    <td class="text-center align-middle">
                        <button class='btn btn-sm btn-primary' onclick='editUsuario(${usuario.id})'>
                            <i class='fa-solid fa-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger' onclick='showDeleteModal(${usuario.id})'>
                            <i class='fa-solid fa-trash-can'></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        document.getElementById('tableBody_usuarios').innerHTML = content;
    } catch (ex) {
        Swal.fire("Error", ex , "error");
    }
};

const deleteUsuario = async (usuarioId) => {
    try {
        const response = await fetch(`/Prediccion/eliminar_usuario/${usuarioId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            await initDataTable();
            $('#deleteModal').modal('hide');
        } else {
            Swal.fire("Error", "No se pudo eliminar el usuario", "error");
        }
    } catch (ex) {
        Swal.fire("Error", ex , "error");
    }
};

const showDeleteModal = (usuarioId) => {
    usuarioIdToDelete = usuarioId;
    $('#deleteModal').modal('show');
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

document.addEventListener("DOMContentLoaded", async () => {
    await initDataTable();
    document.getElementById('confirmDelete').addEventListener('click', () => {
        deleteUsuario(usuarioIdToDelete);
    });
});

function editUsuario(usuarioId) {
    window.location.href = `/Prediccion/editar_usuario/${usuarioId}/`;
}