// инициализация telegram web app
const tg = window.Telegram.WebApp;
tg.expand(); // развернуть на весь экран

// состояние приложения
const state = {
    currentView: 'view-portfolio',
    settings: {
        language: 'en',
        alertsEnabled: false,
        portfolioThreshold: 5,
        btcPriceThreshold: 0
    },
    portfolio: null
};

// mock data generator (если api недоступен)
const generateMockData = () => {
    return {
        total_balance: 1247.80,
        pnl_today: 32.14,
        pnl_percent: 2.6,
        assets: [
            { symbol: "BTC", name: "Bitcoin", amount: 0.015, value_usd: 960.0, change_24h: 2.1, allocation: 76.9 },
            { symbol: "ETH", name: "Ethereum", amount: 0.1, value_usd: 250.0, change_24h: -1.2, allocation: 20.0 },
            { symbol: "SOL", name: "Solana", amount: 2.5, value_usd: 35.0, change_24h: 5.4, allocation: 2.8 },
            { symbol: "USDT", name: "Tether", amount: 12.8, value_usd: 12.8, change_24h: 0.01, allocation: 0.3 }
        ],
        risk_insight: "49.7% of portfolio is BTC"
    };
};

// загрузка настроек из localStorage
const loadSettings = () => {
    const saved = localStorage.getItem('crypto_tracker_settings');
    if (saved) {
        state.settings = JSON.parse(saved);
    }
    applySettings();
};

// сохранение настроек
const saveSettings = () => {
    localStorage.setItem('crypto_tracker_settings', JSON.stringify(state.settings));
};

// применение настроек к ui
const applySettings = () => {
    document.getElementById('alerts-toggle').checked = state.settings.alertsEnabled;
    document.getElementById('portfolio-threshold').value = state.settings.portfolioThreshold;
    document.getElementById('btc-price-threshold').value = state.settings.btcPriceThreshold || '';
    document.getElementById('language-select').value = state.settings.language;
};

// рендер портфеля
const renderPortfolio = (data) => {
    document.getElementById('total-balance').textContent = `$${data.total_balance.toFixed(2)}`;
    
    const pnlValue = document.getElementById('pnl-value');
    const pnlPercent = document.getElementById('pnl-percent');
    
    const sign = data.pnl_today >= 0 ? '+' : '';
    const colorClass = data.pnl_today >= 0 ? 'pnl-positive' : 'pnl-negative';
    
    pnlValue.textContent = `${sign}$${data.pnl_today.toFixed(2)}`;
    pnlPercent.textContent = `(${sign}${data.pnl_percent}%)`;
    
    pnlValue.className = colorClass;
    pnlPercent.className = colorClass;

    document.getElementById('risk-insight').textContent = data.risk_insight;

    const assetsList = document.getElementById('assets-list');
    assetsList.innerHTML = '';
    
    // топ 3 актива для главной
    data.assets.slice(0, 3).forEach(asset => {
        assetsList.appendChild(createAssetCard(asset));
    });

    drawChart();
};

// создание карточки актива
const createAssetCard = (asset) => {
    const div = document.createElement('div');
    div.className = 'asset-card';
    
    const changeClass = asset.change_24h >= 0 ? 'pnl-positive' : 'pnl-negative';
    const changeSign = asset.change_24h >= 0 ? '+' : '';

    div.innerHTML = `
        <div class="asset-info">
            <h4>${asset.symbol}</h4>
            <span>${asset.name}</span>
        </div>
        <div class="asset-value">
            <span class="amount">$${asset.value_usd.toFixed(2)}</span>
            <span class="change ${changeClass}">${changeSign}${asset.change_24h}%</span>
        </div>
    `;
    return div;
};

// рендер всех активов
const renderAllAssets = (data) => {
    const list = document.getElementById('all-assets-list');
    list.innerHTML = '';
    data.assets.forEach(asset => {
        list.appendChild(createAssetCard(asset));
    });
};

// простой svg график
const drawChart = () => {
    const svg = document.getElementById('portfolio-chart');
    // очистка
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }
    
    // генерация случайной линии для демо
    let pathD = "M 0 50 ";
    for (let i = 1; i <= 10; i++) {
        const y = 20 + Math.random() * 60;
        pathD += `L ${i * 30} ${y} `;
    }
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathD);
    svg.appendChild(path);
};

// навигация
const setupNavigation = () => {
    const buttons = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            
            // обновляем активные классы
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(targetId).classList.add('active');
            
            state.currentView = targetId;
        });
    });
};

// обработчики настроек
const setupSettingsHandlers = () => {
    document.getElementById('alerts-toggle').addEventListener('change', (e) => {
        state.settings.alertsEnabled = e.target.checked;
        saveSettings();
    });

    document.getElementById('portfolio-threshold').addEventListener('change', (e) => {
        state.settings.portfolioThreshold = parseFloat(e.target.value);
        saveSettings();
    });

    document.getElementById('btc-price-threshold').addEventListener('change', (e) => {
        state.settings.btcPriceThreshold = parseFloat(e.target.value) || 0;
        saveSettings();
    });

    document.getElementById('language-select').addEventListener('change', (e) => {
        state.settings.language = e.target.value;
        saveSettings();
        // здесь можно добавить логику смены языка текста
        alert(`language switched to ${e.target.value} (demo)`);
    });

    document.getElementById('delete-data-btn').addEventListener('click', () => {
        if (confirm('are you sure? this will clear all local settings.')) {
            localStorage.removeItem('crypto_tracker_settings');
            location.reload();
        }
    });
};

// инициализация
const init = async () => {
    loadSettings();
    setupNavigation();
    setupSettingsHandlers();

    // пытаемся получить данные (в v1 используем мок)
    // в будущем здесь будет fetch('/api/v1/portfolio')
    const data = generateMockData();
    state.portfolio = data;
    
    renderPortfolio(data);
    renderAllAssets(data);
    
    // сообщаем telegram, что приложение готово
    tg.ready();
};

init();
