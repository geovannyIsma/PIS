let dataTable;
let dataTableIsInitialized = false;
let mallaIdToDelete = null;

const dataTableOptions = {
    columnDefs: [
        { className: "text-center align-middle", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [0, 4] },
        { searchable: false, targets: [0, 4] }
    ],
    pageLength: 10,
    destroy: true,
    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "No se encontraron registros de mallas curriculares",
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

    await list_mallas();
    dataTable = $('#datatable-mallas').DataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

const list_mallas = async () => {
    try {
        const response = await fetch('http://localhost:8000/Prediccion/list_malla/');
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
        alert(ex);
    }
};

const deleteMalla = async (mallaId) => {
    try {
        const response = await fetch(`http://localhost:8000/Prediccion/eliminar_malla/${mallaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            await initDataTable();
            $('#deleteModal').modal('hide');
        } else {
            alert('Error al eliminar la malla curricular.');
        }
    } catch (ex) {
        alert(ex);
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

function editMalla(mallaId){
    window.location.href = `/Prediccion/editar_malla/${mallaId}`;
}