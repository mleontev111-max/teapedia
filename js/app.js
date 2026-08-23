// ===== TEAPEDIA APP =====
const API_URL = 'data/teas.json';
let allTeas = [];
let currentFilter = 'all';
let currentSearch = '';

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    loadTeas();
    setupFilters();
    setupSearch();
    setupMobileMenu();
});

// Загрузка данных
async function loadTeas() {
    try {
        const response = await fetch(API_URL);
        allTeas = await response.json();
        renderTeas();
    } catch (error) {
        console.error('Ошибка загрузки чаёв:', error);
        document.getElementById('teaGrid').innerHTML = `
            <div class="error-message" style="grid-column:1/-1;text-align:center;padding:40px;color:var(--color-text-light);">
                <p>Не удалось загрузить каталог. Проверьте подключение.</p>
            </div>
        `;
    }
}

// Рендеринг карточек
function renderTeas() {
    const grid = document.getElementById('teaGrid');
    if (!grid) return;

    const filtered = filterTeas();

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--color-text-light);">
                <p style="font-size:18px;margin-bottom:8px;">🍵 Ничего не найдено</p>
                <p>Попробуйте изменить фильтр или поисковый запрос</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = filtered.map(tea => createTeaCard(tea)).join('');
}

// Фильтрация
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

// Карточка чая
function createTeaCard(tea) {
    const badgeClass = `badge-${tea.category}`;
    const categoryColors = {
        green: '#E8F5E9',
        white: '#F5F5F5',
        oolong: '#FFF3E0',
        red: '#FFEBEE',
        dark: '#3E2723',
        yellow: '#FFFDE7'
    };
    const categoryTextColors = {
        green: '#2E7D32',
        white: '#616161',
        oolong: '#E65100',
        red: '#C62828',
        dark: '#D7CCC8',
        yellow: '#F9A825'
    };

    return `
        <a href="tea.html?id=${tea.id}" class="tea-card" data-category="${tea.category}">
            <div class="tea-image" style="background: ${categoryColors[tea.category] || '#F5F0E8'};">
                <span class="tea-image-placeholder">🍃</span>
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

// Фильтры
function setupFilters() {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTeas();
        });
    });
}

// Поиск
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

// Мобильное меню
function setupMobileMenu() {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.main-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', () => {
        nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        nav.style.position = 'absolute';
        nav.style.top = '72px';
        nav.style.left = '0';
        nav.style.right = '0';
        nav.style.background = 'var(--color-bg)';
        nav.style.flexDirection = 'column';
        nav.style.padding = '20px';
        nav.style.borderBottom = '1px solid var(--color-border)';
        nav.style.zIndex = '99';
    });
}

// ===== УТИЛИТЫ ДЛЯ СТРАНИЦЫ ЧАЯ =====
// Получение параметра URL
function getUrlParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// Форматирование текста
function formatText(text) {
    if (!text) return '';
    return text.replace(/\n/g, '<br>');
}

// Экспорт для использования в других скриптах
window.Teapedia = {
    allTeas,
    getUrlParam,
    formatText,
    loadTeas
};
