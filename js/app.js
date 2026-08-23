// ===== TEAPEDIA APP =====
const API_URL = 'data/teas.json';
const WARE_URL = 'data/ware.json';
let allTeas = [];
let allWare = { categories: [], items: [] };
let currentFilter = 'all';
let currentSearch = '';
let currentWareFilter = 'all';

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    loadTeas();
    setupFilters();
    setupSearch();
    setupMobileMenu();

    // Если есть блок посуды на главной — загрузим категории
    if (document.getElementById('wareCategories')) {
        loadWareCategories();
    }
});

// ===== ЧАЙ =====
async function loadTeas() {
    try {
        const response = await fetch(API_URL);
        allTeas = await response.json();
        renderTeas();
    } catch (error) {
        console.error('Ошибка загрузки чаёв:', error);
        const grid = document.getElementById('teaGrid');
        if (grid) {
            grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--color-text-light);"><p>Не удалось загрузить каталог чая.</p></div>`;
        }
    }
}

function renderTeas() {
    const grid = document.getElementById('teaGrid');
    if (!grid) return;
    const filtered = filterTeas();
    if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--color-text-light);"><p style="font-size:18px;margin-bottom:8px;">🍵 Ничего не найдено</p><p>Попробуйте изменить фильтр или поисковый запрос</p></div>`;
        return;
    }
    grid.innerHTML = filtered.map(tea => createTeaCard(tea)).join('');
}

function filterTeas() {
    return allTeas.filter(tea => {
        const matchCategory = currentFilter === 'all' || tea.category === currentFilter;
        const searchLower = currentSearch.toLowerCase();
        const matchSearch = !currentSearch ||
            tea.name.toLowerCase().includes(searchLower) ||
            tea.nameCn.includes(searchLower) ||
            tea.origin.toLowerCase().includes(searchLower) ||
            tea.flavor.toLowerCase().includes(searchLower) ||
            tea.description.toLowerCase().includes(searchLower);
        return matchCategory && matchSearch;
    });
}

function createTeaCard(tea) {
    const badgeClass = `badge-${tea.category}`;
    return `
        <a href="tea.html?id=${tea.id}" class="tea-card" data-category="${tea.category}" role="listitem">
            <div class="tea-image">
                <span class="tea-image-placeholder" aria-hidden="true">🍃</span>
                <span class="tea-badge ${badgeClass}">${tea.categoryName}</span>
            </div>
            <div class="tea-info">
                <h3 class="tea-name">${tea.name}</h3>
                <div class="tea-origin">${tea.nameCn} · ${tea.origin}</div>
                <div class="tea-meta">
                    <span class="tea-tag">${tea.altitude}</span>
                    <span class="tea-tag">${tea.oxidation}</span>
                </div>
                <p class="tea-desc">${tea.description}</p>
                <div class="tea-footer">
                    <span class="tea-price">${tea.price}</span>
                    <span class="tea-action">Подробнее →</span>
                </div>
            </div>
        </a>
    `;
}

function setupFilters() {
    const buttons = document.querySelectorAll('.filter-btn[data-filter]');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
            currentFilter = btn.dataset.filter;
            renderTeas();
        });
    });
}

function setupSearch() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    let timeout;
    input.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            currentSearch = e.target.value.trim();
            renderTeas();
        }, 300);
    });
}

// ===== ПОСУДА =====
async function loadWare() {
    try {
        const response = await fetch(WARE_URL);
        allWare = await response.json();
        renderWare();
        setupWareFilters();
    } catch (error) {
        console.error('Ошибка загрузки посуды:', error);
        const grid = document.getElementById('wareGrid');
        if (grid) grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;"><p>Не удалось загрузить каталог посуды.</p></div>`;
    }
}

async function loadWareCategories() {
    try {
        const response = await fetch(WARE_URL);
        const data = await response.json();
        const container = document.getElementById('wareCategories');
        if (!container) return;
        container.innerHTML = data.categories.map(cat => `
            <a href="ware.html#${cat.id}" class="ware-cat-card" role="listitem">
                <div class="ware-cat-icon" aria-hidden="true">${cat.icon}</div>
                <div class="ware-cat-name">${cat.name}</div>
                <div class="ware-cat-name-cn">${cat.nameCn}</div>
                <div class="ware-cat-desc">${cat.description}</div>
            </a>
        `).join('');
    } catch (e) { console.error(e); }
}

function renderWare() {
    const grid = document.getElementById('wareGrid');
    if (!grid) return;
    const filtered = currentWareFilter === 'all' 
        ? allWare.items 
        : allWare.items.filter(w => w.category === currentWareFilter);
    if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--color-text-light);"><p>🫖 Ничего не найдено в этой категории</p></div>`;
        return;
    }
    grid.innerHTML = filtered.map(item => createWareCard(item)).join('');
}

function createWareCard(item) {
    const cat = allWare.categories.find(c => c.id === item.category);
    return `
        <article class="ware-card" role="listitem" itemscope itemtype="https://schema.org/Product">
            <div class="ware-image">
                <span class="ware-image-placeholder" aria-hidden="true">${cat ? cat.icon : '🫖'}</span>
                <span class="ware-badge">${cat ? cat.name : 'Посуда'}</span>
            </div>
            <div class="ware-info">
                <h3 class="ware-name" itemprop="name">${item.name}</h3>
                <div class="ware-name-cn">${item.nameCn}</div>
                <div class="ware-meta">
                    ${item.material ? `<span class="ware-tag">${item.material}</span>` : ''}
                    ${item.volume ? `<span class="ware-tag">${item.volume}</span>` : ''}
                    ${item.size ? `<span class="ware-tag">${item.size}</span>` : ''}
                </div>
                <p class="ware-desc" itemprop="description">${item.desc}</p>
                <div class="ware-footer">
                    <span class="ware-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                        <span itemprop="price">${item.price.replace(' ₽', '').replace(' ', '')}</span>
                        <span itemprop="priceCurrency" content="RUB">₽</span>
                    </span>
                    <span class="ware-material">${item.material || ''}</span>
                </div>
            </div>
        </article>
    `;
}

function setupWareFilters() {
    const buttons = document.querySelectorAll('.filter-btn[data-ware-filter]');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
            currentWareFilter = btn.dataset.wareFilter;
            renderWare();
        });
    });
}

// ===== МОБИЛЬНОЕ МЕНЮ =====
function setupMobileMenu() {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.main-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', () => {
        const isOpen = nav.style.display === 'flex';
        nav.style.display = isOpen ? 'none' : 'flex';
        toggle.setAttribute('aria-expanded', String(!isOpen));
        if (!isOpen) {
            nav.style.position = 'absolute';
            nav.style.top = '72px';
            nav.style.left = '0';
            nav.style.right = '0';
            nav.style.background = 'var(--color-bg)';
            nav.style.flexDirection = 'column';
            nav.style.padding = '20px';
            nav.style.borderBottom = '1px solid var(--color-border)';
            nav.style.zIndex = '99';
        }
    });
}

// ===== УТИЛИТЫ =====
function getUrlParam(name) {
    return new URLSearchParams(window.location.search).get(name);
}

// Экспорт
window.Teapedia = { allTeas, allWare, getUrlParam, loadTeas, loadWare };
