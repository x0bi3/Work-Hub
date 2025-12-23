/**
 * Work-Hub Resource Center - JavaScript
 * Handles filtering, search, and dynamic rendering of resources
 */

let allDocuments = [];
let activeFilters = {
    search: '',
    category: '',
    tags: []
};

// Load documents and initialize
function init() {
    loadDocuments();
    setupEventListeners();
    renderDocuments();
}

// Load documents from data.json
function loadDocuments() {
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            allDocuments = data.documents;
            initializeTagFilters();
            renderDocuments();
        })
        .catch(error => console.error('Error loading documents:', error));
}

// Setup event listeners for filters
function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            activeFilters.search = e.target.value.toLowerCase();
            renderDocuments();
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', (e) => {
            activeFilters.category = e.target.value;
            renderDocuments();
        });
    }
}

// Initialize tag filter buttons
function initializeTagFilters() {
    const allTags = new Set();
    allDocuments.forEach(doc => {
        doc.tags.forEach(tag => allTags.add(tag));
    });
    
    const tagFiltersContainer = document.getElementById('tagFilters');
    if (!tagFiltersContainer) return;
    
    const sortedTags = Array.from(allTags).sort();
    tagFiltersContainer.innerHTML = '';
    
    sortedTags.forEach(tag => {
        const button = document.createElement('button');
        button.className = 'tag-filter';
        button.textContent = tag;
        button.setAttribute('aria-label', `Filter by ${tag} tag`);
        button.addEventListener('click', () => toggleTagFilter(tag, button));
        tagFiltersContainer.appendChild(button);
    });
}

// Toggle tag filter
function toggleTagFilter(tag, button) {
    const index = activeFilters.tags.indexOf(tag);
    if (index > -1) {
        activeFilters.tags.splice(index, 1);
        button.classList.remove('active');
    } else {
        activeFilters.tags.push(tag);
        button.classList.add('active');
    }
    renderDocuments();
}

// Filter documents based on active filters
function getFilteredDocuments() {
    return allDocuments.filter(doc => {
        // Search filter
        if (activeFilters.search) {
            const searchMatch = 
                doc.title.toLowerCase().includes(activeFilters.search) ||
                doc.description.toLowerCase().includes(activeFilters.search) ||
                doc.tags.some(tag => tag.includes(activeFilters.search));
            if (!searchMatch) return false;
        }
        
        // Category filter
        if (activeFilters.category && doc.category !== activeFilters.category) {
            return false;
        }
        
        // Tag filters (must match ALL selected tags)
        if (activeFilters.tags.length > 0) {
            const hasAllTags = activeFilters.tags.every(tag => doc.tags.includes(tag));
            if (!hasAllTags) return false;
        }
        
        return true;
    });
}

// Render documents to the grid
function renderDocuments() {
    const filtered = getFilteredDocuments();
    const grid = document.getElementById('documentsGrid');
    const noResults = document.getElementById('noResults');
    
    if (!grid) return;
    
    grid.innerHTML = '';
    
    if (filtered.length === 0) {
        if (noResults) noResults.style.display = 'block';
        return;
    }
    
    if (noResults) noResults.style.display = 'none';
    
    filtered.forEach(doc => {
        const card = createDocumentCard(doc);
        grid.appendChild(card);
    });
}

// Create a document card element
function createDocumentCard(doc) {
    const card = document.createElement('article');
    card.className = 'document-card';
    card.setAttribute('aria-label', `${doc.title} - ${doc.category}`);
    
    const fileIcons = {
        'PDF': '📄',
        'Checklist': '✓️',
        'Guide': '📖',
        'Video': '🎥',
        'default': '📋'
    };
    
    const icon = fileIcons[doc.file_type] || fileIcons.default;
    
    card.innerHTML = `
        <div class="document-header">
            <span class="document-icon">${icon}</span>
            <span class="document-category">${doc.category}</span>
        </div>
        
        <h3 class="document-title">${doc.title}</h3>
        <p class="document-description">${doc.description}</p>
        
        <div class="document-meta">
            <span class="document-author">By ${doc.author}</span>
            <span class="document-date">${formatDate(doc.date)}</span>
        </div>
        
        <div class="document-tags">
            ${doc.tags.map(tag => `
                <button class="doc-tag" onclick="filterByTag('${tag}')" aria-label="Filter by ${tag}">
                    ${tag}
                </button>
            `).join('')}
        </div>
        
        <div class="document-actions">
            <a href="${doc.path}" class="doc-button doc-button-primary" download>
                Download
            </a>
            <button class="doc-button doc-button-secondary" onclick="viewDocument('${doc.path}')">Preview</button>
        </div>
    `;
    
    return card;
}

// Filter by clicking on a tag
function filterByTag(tag) {
    const tagButtons = document.querySelectorAll('.tag-filter');
    tagButtons.forEach(btn => {
        if (btn.textContent === tag) {
            btn.click();
        }
    });
}

// View document (placeholder for preview functionality)
function viewDocument(path) {
    alert(`Preview of ${path}\n\nPreview feature coming soon!`);
}

// Format date to readable format
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Add animation on element visibility
if ('IntersectionObserver' in window) {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px',
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.document-card, .about-card, .support-card').forEach((el) => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

console.log('Work-Hub Resource Center loaded successfully!');
