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
    const cycleTabs = document.getElementById('cycleTabs');
    const cycleTabsContent = document.getElementById('cycleTabsContent');

    if (!validateField(numCycles)) {
        return;
    }

    cycleTabs.innerHTML = '';
    cycleTabsContent.innerHTML = '';

    for (let i = 1; i <= numCyclesValue; i++) {
        // Create tab
        const tab = document.createElement('li');
        tab.className = 'nav-item';
        tab.innerHTML = `
            <a class="nav-link ${i === 1 ? 'active' : ''}" id="cycle-tab-${i}" data-bs-toggle="tab" href="#cycle-${i}" role="tab" aria-controls="cycle-${i}" aria-selected="${i === 1}">
                Ciclo ${i}
            </a>
        `;
        cycleTabs.appendChild(tab);

        // Create tab content
        const tabContent = document.createElement('div');
        tabContent.className = `tab-pane fade ${i === 1 ? 'show active' : ''}`;
        tabContent.id = `cycle-${i}`;
        tabContent.role = 'tabpanel';
        tabContent.ariaLabelledby = `cycle-tab-${i}`;
        tabContent.innerHTML = `
            <div class="input-group mb-3">
                <label class="input-group-text" for="num_subjects_${i}">Número de asignaturas:</label>
                <input type="number" class="form-control" id="num_subjects_${i}" min="1" required>
                <button class="btn btn-outline-secondary" type="button" onclick="createSubjectRows(${i})">Aceptar</button>
                <div class="invalid-feedback">
                    Por favor, ingresa un número válido de asignaturas.
                </div>
                <div class="valid-feedback">
                    Número de asignaturas válido.
                </div>
            </div>
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
        cycleTabsContent.appendChild(tabContent);

        // Apply real-time validation for the new num_subjects fields
        document.getElementById(`num_subjects_${i}`).addEventListener('input', function() {
            validateField(this);
        });
    }

    // Habilitar el botón de guardar
    document.getElementById('guardar_button').disabled = false;

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
                <input type="text" name="codigo_asignatura_${cycleIndex}_${i}" id="codigo_asignatura_${cycleIndex}_${i}" class="form-control" readonly required>
            </td>
            <td>
                <input type="text" name="nombre_asignatura_${cycleIndex}_${i}" id="nombre_asignatura_${cycleIndex}_${i}" class="form-control" readonly required>
            </td>
            <td>
                <button type="button" class="btn btn-success" onclick="openAsignaturaModal(${cycleIndex}, ${i})">+</button>
                <button type="button" class="btn btn-danger" onclick="clearAsignaturaFields(${cycleIndex}, ${i})">-</button>
            </td>
        `;
        subjectTable.appendChild(row);
    }

    // Apply Bootstrap validation
    applyBootstrapValidation();
}

function clearAsignaturaFields(cycleIndex, subjectIndex) {
    document.getElementById(`codigo_asignatura_${cycleIndex}_${subjectIndex}`).value = '';
    document.getElementById(`nombre_asignatura_${cycleIndex}_${subjectIndex}`).value = '';
}

function openAsignaturaModal(cycleIndex, subjectIndex) {
    const asignaturaForm = document.getElementById('asignaturaForm');

    // Limpiar los campos del formulario modal
    asignaturaForm.reset();

    // Almacenar los índices del ciclo y de la asignatura en los atributos data
    asignaturaForm.setAttribute('data-cycle', cycleIndex);
    asignaturaForm.setAttribute('data-subject', subjectIndex);

    // Abrir el modal
    $('#asignaturaModal').modal('show');
}

function saveAsignatura() {
    const asignaturaForm = document.getElementById('asignaturaForm');

    if (!asignaturaForm.checkValidity()) {
        asignaturaForm.classList.add('was-validated');
        return;
    }

    const cycleIndex = asignaturaForm.getAttribute('data-cycle');
    const subjectIndex = asignaturaForm.getAttribute('data-subject');
    const codigoAsignatura = document.getElementById('codigo_asignatura_modal').value;
    const nombreAsignatura = document.getElementById('nombre_asignatura_modal').value;

    // Asignar los valores a los campos correspondientes en la tabla
    document.getElementById(`codigo_asignatura_${cycleIndex}_${subjectIndex}`).value = codigoAsignatura;
    document.getElementById(`nombre_asignatura_${cycleIndex}_${subjectIndex}`).value = nombreAsignatura;

    // Cerrar el modal
    $('#asignaturaModal').modal('hide');
}

// Función para aplicar la validación de Bootstrap
let alreadyApplied = false;
function applyBootstrapValidation() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false || !validateAllSubjects()) {
                event.preventDefault();
                event.stopPropagation();

                if (!validateAllSubjects() && !alreadyApplied) {
                    alreadyApplied = true;
                    alert('Por favor, ingresa todas las asignaturas para los ciclos.');
                }
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Función para validar campos individuales en tiempo real
function validateField(field) {
    if (field.checkValidity() === false) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        return false;
    } else {
        field.classList.add('is-valid');
        field.classList.remove('is-invalid');
        return true;
    }
}

// Función para validar si se han ingresado todas las asignaturas para los ciclos
function validateAllSubjects() {
    const numCycles = document.getElementById('num_cycles').value;

    for (let i = 1; i <= numCycles; i++) {
        const numSubjects = document.getElementById(`num_subjects_${i}`).value;

        if (numSubjects === '') {
            return false;
        }

        for (let j = 1; j <= numSubjects; j++) {
            const codigoAsignatura = document.getElementById(`codigo_asignatura_${i}_${j}`).value;
            const nombreAsignatura = document.getElementById(`nombre_asignatura_${i}_${j}`).value;

            if (codigoAsignatura === '' || nombreAsignatura === '') {
                return false;
            }
        }
    }

    return true;
}