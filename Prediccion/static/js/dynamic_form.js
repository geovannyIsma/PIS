document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('guardar_button').disabled = true;
    applyBootstrapValidation();

    // Real-time validation for num_cycles
    document.getElementById('num_cycles').addEventListener('input', function() {
        validateField(this);
    });
});

function createCycleCards() {
    const numCycles = document.getElementById('num_cycles');
    const numCyclesValue = numCycles.value;
    const cycleCardsContainer = document.getElementById('cycleCardsContainer');

    if (!validateField(numCycles)) {
        return;
    }

    cycleCardsContainer.innerHTML = '';

    for (let i = 1; i <= numCyclesValue; i++) {
        // Create card
        const card = document.createElement('div');
        card.className = 'card col-md-4 card-cycle mb-1';
        card.innerHTML = `
            <div class="card-body">
                <h5>Ciclo ${i}</h5>
            </div>
        `;
        cycleCardsContainer.appendChild(card);
    }

    // Enable the save button
    document.getElementById('guardar_button').disabled = false;

    // Apply Bootstrap validation
    applyBootstrapValidation();
}

// Función para aplicar la validación de Bootstrap
let alreadyApplied = false;
function applyBootstrapValidation() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
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
