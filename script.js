let allResources = [];
let filters = { search: '', category: '', tags: [] };

async function init() {
    try {
        const response = await fetch('data.json');
        allResources = await response.json();
        
        setupEventListeners();
        renderTags();
        render();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', (e) => {
        filters.search = e.target.value.toLowerCase();
        render();
    });

    document.getElementById('categoryFilter').addEventListener('change', (e) => {
        filters.category = e.target.value;
        render();
    });
}

function renderTags() {
    const allTags = new Set();
    allResources.forEach(r => r.tags.forEach(t => allTags.add(t)));
    
    const container = document.getElementById('tagContainer');
    container.innerHTML = '';
    
    Array.from(allTags).sort().forEach(tag => {
        const btn = document.createElement('button');
        btn.className = 'tag';
        btn.textContent = tag;
        btn.onclick = () => {
            if (filters.tags.includes(tag)) {
                filters.tags = filters.tags.filter(t => t !== tag);
                btn.classList.remove('active');
            } else {
                filters.tags.push(tag);
                btn.classList.add('active');
            }
            render();
        };
        container.appendChild(btn);
    });
}

function getFiltered() {
    return allResources.filter(r => {
        if (filters.search && !r.title.toLowerCase().includes(filters.search) && 
            !r.description.toLowerCase().includes(filters.search)) {
            return false;
        }
        if (filters.category && r.category !== filters.category) return false;
        if (filters.tags.length > 0 && !filters.tags.every(t => r.tags.includes(t))) return false;
        return true;
    });
}

function render() {
    const filtered = getFiltered();
    const grid = document.getElementById('resourcesGrid');
    const noResults = document.getElementById('noResults');
    
    grid.innerHTML = '';
    
    if (filtered.length === 0) {
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    
    filtered.forEach(r => {
        const card = document.createElement('div');
        card.className = 'resource-card';
        card.innerHTML = `
            <div class="resource-icon">${r.icon}</div>
            <div class="resource-category">${r.category}</div>
            <h3>${r.title}</h3>
            <p>${r.description}</p>
            <div class="resource-meta">By ${r.author} • ${r.date}</div>
            <div class="resource-tags">
                ${r.tags.map(t => `<button class="mini-tag" onclick="filterByTag('${t}')">${t}</button>`).join('')}
            </div>
            <div class="resource-actions">
                <a href="${r.path}" class="btn-primary" download>Download</a>
                <button class="btn-secondary" onclick="preview('${r.path}')">Preview</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function filterByTag(tag) {
    filters.tags = filters.tags.includes(tag) 
        ? filters.tags.filter(t => t !== tag) 
        : [...filters.tags, tag];
    
    document.querySelectorAll('.tag').forEach(btn => {
        if (btn.textContent === tag) {
            btn.classList.toggle('active');
        }
    });
    
    render();
}

function preview(path) {
    alert(`Preview of ${path}\n\nPreview feature coming soon!`);
}

function scrollTo(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

init();
