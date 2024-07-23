let dataTable;
let dataTableIsInitialized = false;
let periodoIdToDelete = null;

const dataTableOptions = {
    columnDefs: [
        { className: "text-center align-middle", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [0, 4] },
        { searchable: false, targets: [0, 4] }
    ],
    pageLength: 10,
    destroy: true,
    language : {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "No se encontraron registros de periodos",
        info: "Página _PAGE_ de _PAGES_",
        infoEmpty: "No hay registros disponibles",
        infoFiltered: "(filtrado de _MAX_ registros totales)",
        search: "Buscar:",

    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await list_periodos();
    dataTable = $('#datatable-periodos').DataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

const list_periodos = async () => {
    try {
        const response = await fetch('http://localhost:8000/Prediccion/list_periodo/');
        const data = await response.json();
        let content = ``;
        data.periodos.forEach((periodo, index) => {
            content += `
                <tr>
                    <td class="text-center align-middle">${index + 1}</td>
                    <td class="text-center align-middle">${periodo.codigo_periodo}</td>
                    <td class="text-center align-middle">${periodo.fecha_inicio}</td>
                    <td class="text-center align-middle">${periodo.fecha_fin}</td>
                    <td class="text-center align-middle">
                        <button class='btn btn-sm btn-primary' onclick='editPeriodo(${periodo.id})'>
                            <i class='fa-solid fa-pencil'></i>
                        </button>
                        <button class='btn btn-sm btn-danger' onclick='showDeleteModal(${periodo.id})'>
                            <i class='fa-solid fa-trash-can'></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        document.getElementById('tableBody_periodos').innerHTML = content;
    } catch (error) {
        Swal.fire("Error", "No se pudo cargar la lista de periodos", "error");
    }
};

const deletePeriodo = async () => {
    try {
        const response = await fetch(`http://localhost:8000/Prediccion/eliminar_periodo/${periodoIdToDelete}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            await initDataTable();
            $('#deleteModal').modal('hide');
        } else {
            Swal.fire("Error", "No se pudo eliminar el periodo", "error");
        }
    } catch (error) {
        Swal.fire("Error", error, "error");
    }

}
const showDeleteModal = (periodoId) => {
    periodoIdToDelete = periodoId;
    $('#deleteModal').modal('show');
};

const confirmDelete = () => {
    if (periodoIdToDelete) {
        deletePeriodo(periodoIdToDelete);
    }
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
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

function editPeriodo(periodo_Id) {
    window.location.href = `/Prediccion/editar_periodo/${periodo_Id}`;
}
