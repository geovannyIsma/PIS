function createCycleTabs() {
    const numCycles = document.getElementById('num_cycles').value;
    if (!numCycles || numCycles < 1) {
        alert('Por favor, ingresa un número válido de ciclos.');
        return;
    }

    const cycleContainer = document.getElementById('cycle_tabs');
    cycleContainer.innerHTML = '';

    for (let i = 1; i <= numCycles; i++) {
        const tab = document.createElement('div');
        tab.className = 'tab';
        tab.id = 'cycle_' + i;
        tab.innerHTML = `
            <h3>Ciclo ${i}</h3>
            <div class="form-group">
                <label for="num_subjects_${i}">Número de asignaturas:</label>
                <input type="number" class="form-control" id="num_subjects_${i}" min="1" required>
            </div>
            <button type="button" class="btn btn-primary mb-3" onclick="createSubjectRows(${i})">Aceptar</button>
            <table id="subject_table_${i}" class="table">
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Nombre</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `;
        cycleContainer.appendChild(tab);
    }
}

function createSubjectRows(cycleIndex) {
    const numSubjects = document.getElementById('num_subjects_' + cycleIndex).value;
    if (!numSubjects || numSubjects < 1) {
        alert('Por favor, ingresa un número válido de asignaturas.');
        return;
    }

    const subjectTable = document.getElementById('subject_table_' + cycleIndex).getElementsByTagName('tbody')[0];
    subjectTable.innerHTML = '';

    for (let i = 1; i <= numSubjects; i++) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><input type="text" name="codigo_asignatura_${cycleIndex}_${i}" required class="form-control"></td>
            <td><input type="text" name="nombre_asignatura_${cycleIndex}_${i}" required class="form-control"></td>
            <td><button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#asignaturaModal" onclick="openAsignaturaModal(${cycleIndex}, ${i})">+</button></td>
        `;
        subjectTable.appendChild(row);
    }
}

function openAsignaturaModal(cycleIndex, subjectIndex) {
    document.getElementById('asignaturaForm').setAttribute('data-cycle', cycleIndex);
    document.getElementById('asignaturaForm').setAttribute('data-subject', subjectIndex);
}


function saveAsignatura() {
    const codigoAsignatura = document.getElementById('codigo_asignatura_modal').value;
    const nombreAsignatura = document.getElementById('nombre_asignatura_modal').value;

    // Obtener el ciclo y asignatura actual
    const cycleIndex = document.getElementById('asignaturaForm').getAttribute('data-cycle');
    const subjectIndex = document.getElementById('asignaturaForm').getAttribute('data-subject');

    // Verificar si el código de asignatura ya existe en el mismo ciclo
    const codigoInput = document.getElementsByName(`codigo_asignatura_${cycleIndex}_${subjectIndex}`)[0];
    const codigoValue = codigoInput.value.trim();  // Obtener el valor del campo y quitar espacios en blanco

    // Realizar una petición AJAX o verificar en el lado del cliente si es necesario
    // Aquí asumimos una validación básica en el lado del cliente
    const asignaturasExistentes = document.querySelectorAll(`input[name^="codigo_asignatura_${cycleIndex}"]`);
    for (let asignatura of asignaturasExistentes) {
        if (asignatura !== codigoInput && asignatura.value.trim() === codigoValue) {
            alert('Ya existe una asignatura con el mismo código en este ciclo.');
            return;
        }
    }

    // Asignar los valores al campo correspondiente en la tabla de asignaturas
    codigoInput.value = codigoAsignatura;
    document.getElementsByName(`nombre_asignatura_${cycleIndex}_${subjectIndex}`)[0].value = nombreAsignatura;

    // Cerrar el modal
    $('#asignaturaModal').modal('hide');
}

