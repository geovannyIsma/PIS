document.addEventListener('DOMContentLoaded', function() {
    applyBootstrapValidation();

    // Real-time validation for num_cycles
    document.getElementById('num_cycles').addEventListener('input', function() {
        validateField(this);
    });
});

function createCycleTabs() {
    const numCycles = document.getElementById('num_cycles');
    const numCyclesValue = numCycles.value;
    const cycleContainer = document.getElementById('cycle_tabs');

    if (!validateField(numCycles)) {
        return;
    }

    cycleContainer.innerHTML = '';

    for (let i = 1; i <= numCyclesValue; i++) {
        const tab = document.createElement('div');
        tab.className = 'tab';
        tab.id = 'cycle_' + i;
        tab.innerHTML = `
            <h3>Ciclo ${i}</h3>
            <div class="form-group position-relative">
                <label for="num_subjects_${i}">Número de asignaturas:</label>
                <input type="number" class="form-control" id="num_subjects_${i}" min="1" required>
                <div class="invalid-feedback">
                    Por favor, ingresa un número válido de asignaturas.
                </div>
                <div class="valid-feedback">
                    Número de asignaturas válido.
                </div>
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

        // Apply real-time validation for the new num_subjects fields
        document.getElementById(`num_subjects_${i}`).addEventListener('input', function() {
            validateField(this);
        });
    }

    // Apply Bootstrap validation
    applyBootstrapValidation();
}

function createSubjectRows(cycleIndex) {
    const numSubjects = document.getElementById('num_subjects_' + cycleIndex);
    const numSubjectsValue = numSubjects.value;
    const subjectTable = document.getElementById('subject_table_' + cycleIndex).getElementsByTagName('tbody')[0];

    if (!validateField(numSubjects)) {
        return;
    }

    subjectTable.innerHTML = '';

    for (let i = 1; i <= numSubjectsValue; i++) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <input type="text" name="codigo_asignatura_${cycleIndex}_${i}" required class="form-control">
                <div class="invalid-feedback">
                    Por favor, ingresa un código válido.
                </div>
                <div class="valid-feedback">
                    ¡Código válido!
                </div>
            </td>
            <td>
                <input type="text" name="nombre_asignatura_${cycleIndex}_${i}" required class="form-control">
                <div class="invalid-feedback">
                    Por favor, ingresa un nombre válido.
                </div>
                <div class="valid-feedback">
                    ¡Nombre válido!
                </div>
            </td>
            <td><button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#asignaturaModal" onclick="openAsignaturaModal(${cycleIndex}, ${i})">+</button></td>
        `;
        subjectTable.appendChild(row);
    }

    // Apply Bootstrap validation
    applyBootstrapValidation();
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

    // Asignar los valores de los campos al formulario
    const codigoInputRow = document.getElementsByName(`codigo_asignatura_${cycleIndex}_${subjectIndex}`)[0];
    const nombreInputRow = document.getElementsByName(`nombre_asignatura_${cycleIndex}_${subjectIndex}`)[0];
    codigoInputRow.value = codigoAsignatura;
    nombreInputRow.value = nombreAsignatura;

    // Cerrar el modal
    $('#asignaturaModal').modal('hide');
}

function applyBootstrapValidation() {
    const forms = document.getElementsByClassName('needs-validation');
    Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
}

function validateField(field) {
    if (!field.checkValidity()) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        return false;
    } else {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        return true;
    }
}

function clearValidationStyles(field) {
    field.classList.remove('is-invalid');
    field.classList.remove('is-valid');
}

function clearValidationFeedback() {
    const fields = document.getElementsByClassName('form-control');
    for (let field of fields) {
        clearValidationStyles(field);
    }
}

