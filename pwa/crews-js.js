
// NEW CREWS BUILDER FUNCTIONS - Added 2026-03-26

// Crews data structure
let crewsData = {
  crews: [
    { id: 'crew_1', name: 'Crew 1', members: [] },
    { id: 'crew_2', name: 'Crew 2', members: [] }
  ],
  availableWorkers: []
};

// Initialize crews panel
function initCrews() {
  syncCrewsWorkers();
  renderCrewsPool();
  renderCrewsList();
}

// Sync workers to crews pool
function syncCrewsWorkers() {
  const assigned = new Set();
  crewsData.crews.forEach(crew => {
    if (crew.members) crew.members.forEach(m => assigned.add(m.name));
  });
  crewsData.availableWorkers = st.workers.filter(w => !assigned.has(w.name));
}

// Render available workers pool
function renderCrewsPool() {
  const pool = document.getElementById('crewsWorkerPool');
  if (!pool) return;
  pool.innerHTML = '';
  if (!crewsData.availableWorkers || crewsData.availableWorkers.length === 0) {
    pool.innerHTML = '<div class="empty-crew-msg">All workers assigned</div>';
    return;
  }
  const container = document.createElement('div');
  container.className = 'crews-pool-items';
  crewsData.availableWorkers.forEach(worker => {
    const el = document.createElement('div');
    el.className = 'crews-pool-worker';
    el.draggable = true;
    el.dataset.name = worker.name;
    const col = wColor(worker.name);
    el.innerHTML = '<span style="background:'+col+';width:8px;height:8px;border-radius:50%;"></span><span>'+worker.name+'</span>';
    el.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('worker', worker.name);
      el.classList.add('dragging');
    });
    el.addEventListener('dragend', () => el.classList.remove('dragging'));
    container.appendChild(el);
  });
  pool.appendChild(container);
}

// Render crews list
function renderCrewsList() {
  const container = document.getElementById('dynamicCrewsList');
  if (!container) return;
  container.innerHTML = '';
  crewsData.crews.forEach(crew => {
    const crewBox = document.createElement('div');
    crewBox.className = 'crew-box';
    const header = document.createElement('div');
    header.className = 'crew-box-header';
    header.innerHTML = '<input type="text" class="crew-name-input" value="'+crew.name+'" onchange="renameCrew(\''+crew.id+'\', this.value)" placeholder="Crew Name"><button class="remove-crew-btn" onclick="removeCrew(\''+crew.id+'\')">Remove</button>';
    const membersArea = document.createElement('div');
    membersArea.className = 'crew-members';
    membersArea.dataset.crewId = crew.id;
    membersArea.addEventListener('dragover', (e) => { e.preventDefault(); membersArea.classList.add('drag-over'); });
    membersArea.addEventListener('dragleave', () => membersArea.classList.remove('drag-over'));
    membersArea.addEventListener('drop', (e) => {
      e.preventDefault();
      membersArea.classList.remove('drag-over');
      const workerName = e.dataTransfer.getData('worker');
      if (workerName) assignWorkerToCrew(workerName, crew.id);
    });
    if (!crew.members || crew.members.length === 0) {
      membersArea.innerHTML = '<div class="empty-crew-msg">Drag workers here</div>';
    } else {
      crew.members.forEach(member => {
        const row = document.createElement('div');
        row.className = 'crew-member-row';
        const col = wColor(member.name);
        row.innerHTML = '<span style="display:flex;align-items:center;gap:6px;"><span style="background:'+col+';width:8px;height:8px;border-radius:50%;"></span>'+member.name+'</span><button class="remove-member-btn" onclick="removeWorkerFromCrew(\''+member.name+'\', \''+crew.id+'\')">×</button>';
        membersArea.appendChild(row);
      });
    }
    crewBox.appendChild(header);
    crewBox.appendChild(membersArea);
    container.appendChild(crewBox);
  });
}

// Add new crew
function addCrew() {
  const newId = 'crew_' + Date.now();
  crewsData.crews.push({
    id: newId,
    name: 'Crew ' + (crewsData.crews.length + 1),
    members: []
  });
  initCrews();
}

// Remove crew
function removeCrew(crewId) {
  if (crewsData.crews.length <= 1) {
    alert('Must have at least one crew');
    return;
  }
  const crew = crewsData.crews.find(c => c.id === crewId);
  if (crew && crew.members) {
    crew.members.forEach(m => crewsData.availableWorkers.push(m));
  }
  crewsData.crews = crewsData.crews.filter(c => c.id !== crewId);
  initCrews();
}

// Rename crew
function renameCrew(crewId, newName) {
  const crew = crewsData.crews.find(c => c.id === crewId);
  if (crew) crew.name = newName;
}

// Assign worker to crew
function assignWorkerToCrew(workerName, crewId) {
  const idx = crewsData.availableWorkers.findIndex(w => w.name === workerName);
  if (idx === -1) return;
  const worker = crewsData.availableWorkers[idx];
  crewsData.availableWorkers.splice(idx, 1);
  const crew = crewsData.crews.find(c => c.id === crewId);
  if (crew) {
    if (!crew.members) crew.members = [];
    crew.members.push(worker);
  }
  initCrews();
}

// Remove worker from crew
function removeWorkerFromCrew(workerName, crewId) {
  const crew = crewsData.crews.find(c => c.id === crewId);
  if (!crew) return;
  crew.members = crew.members.filter(m => m.name !== workerName);
  const worker = st.workers.find(w => w.name === workerName);
  if (worker) crewsData.availableWorkers.push(worker);
  initCrews();
}

// Override renderCrews to use new system
function renderCrews() {
  initCrews();
}
