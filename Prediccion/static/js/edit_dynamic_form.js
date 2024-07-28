// Función para crear pestañas de ciclo dinámicamente
function createCycleTabs() {
    let numCycles = document.getElementById('num_cycles').value;
    let cycleTabs = document.getElementById('cycleTabs');
    let cycleTabsContent = document.getElementById('cycleTabsContent');

    // Limpiar pestañas y contenido existente
    cycleTabs.innerHTML = '';
    cycleTabsContent.innerHTML = '';

    // Crear pestañas y contenido para cada ciclo
    for (let i = 1; i <= numCycles; i++) {
        let cycleId = `cycle${i}`;
        let cycleName = `Ciclo ${i}`;

        // Crear pestaña
        let tabItem = document.createElement('li');
        tabItem.className = 'nav-item';
        tabItem.innerHTML = `
            <a class="nav-link" id="${cycleId}-tab" data-toggle="tab" href="#${cycleId}" role="tab" aria-controls="${cycleId}" aria-selected="false">${cycleName}</a>
        `;
        cycleTabs.appendChild(tabItem);

        // Crear contenido del ciclo
        let cycleContent = document.createElement('div');
        cycleContent.className = 'tab-pane fade';
        cycleContent.id = cycleId;
        cycleContent.role = 'tabpanel';
        cycleContent.setAttribute('aria-labelledby', `${cycleId}-tab`);
        cycleContent.innerHTML = `
            <h3>${cycleName}</h3>
            <div class="form-group">
                <label for="codigo_asignatura_${i}_1">Código de asignatura:</label>
                <input type="text" class="form-control" id="codigo_asignatura_${i}_1" name="codigo_asignatura_${i}_1" required>
            </div>
            <div class="form-group">
                <label for="nombre_asignatura_${i}_1">Nombre de asignatura:</label>
                <input type="text" class="form-control" id="nombre_asignatura_${i}_1" name="nombre_asignatura_${i}_1" required>
            </div>
        `;
        cycleTabsContent.appendChild(cycleContent);
    }
}
