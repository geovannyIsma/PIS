let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4] },
        { orderable: false, targets: [0, 4] },
        { searchable: false, targets: [0, 4] }
    ],
    pageLength: 10,
    destroy: true
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
                    <td>${index + 1}</td>
                    <td>${mallaCurricular.codigo}</td>
                    <td>${mallaCurricular.nombre_malla}</td>
                    <td>${mallaCurricular.tituloOtorgado}</td>
                    <td>
                        <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>
            `;
        });
        document.getElementById('tableBody_mallas').innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});
