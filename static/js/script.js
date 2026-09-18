// Stock Prediction App - Client Logic

document.addEventListener('DOMContentLoaded', function() {
    setDefaultDates();
    
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    const infoBtn = document.getElementById('info-btn');
    if (infoBtn) {
        infoBtn.addEventListener('click', fetchStockInfo);
    }
    
    const symbolInput = document.getElementById('symbol');
    if (symbolInput) {
        symbolInput.addEventListener('blur', function() {
            if (this.value.trim().length > 0) {
                fetchStockInfo();
            }
        });
    }
});

function setDefaultDates() {
    const today = new Date();
    const endDateInput = document.getElementById('end_date');
    
    const endDate = new Date(today);
    endDate.setDate(today.getDate() - 1);
    if (endDateInput) {
        endDateInput.value = formatDate(endDate);
        endDateInput.max = formatDate(endDate);
    }
    
    const startDate = new Date(endDate);
    startDate.setFullYear(startDate.getFullYear() - 1);
    const startDateInput = document.getElementById('start_date');
    if (startDateInput) {
        startDateInput.value = formatDate(startDate);
    }
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function handleFormSubmit(event) {
    const submitBtn = document.getElementById('predict-btn');
    const btnText = document.getElementById('btn-text');
    const spinner = document.getElementById('spinner');
    
    if (submitBtn && btnText && spinner) {
        btnText.textContent = 'Training LSTM Model...';
        spinner.classList.remove('d-none');
        submitBtn.disabled = true;
    }
}

function fetchStockInfo() {
    const symbolInput = document.getElementById('symbol');
    const stockInfoDiv = document.getElementById('stock-info');
    const stockName = document.querySelector('.stock-name');
    const stockDetails = document.querySelector('.stock-details');
    
    if (!symbolInput || !stockInfoDiv || !stockName || !stockDetails) return;
    
    const symbol = symbolInput.value.trim().toUpperCase();
    if (!symbol) return;
    
    stockInfoDiv.classList.remove('d-none');
    stockName.textContent = 'Loading stock info...';
    stockDetails.innerHTML = '';
    
    fetch(`/api/stock_info/${symbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Stock info unavailable');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            stockName.textContent = `${data.name} (${symbol})`;
            
            let detailsHTML = '';
            if (data.sector && data.sector !== 'N/A') detailsHTML += `<div>Sector: ${data.sector}</div>`;
            if (data.industry && data.industry !== 'N/A') detailsHTML += `<div>Industry: ${data.industry}</div>`;
            
            if (data.market_cap && data.market_cap !== 'N/A') {
                detailsHTML += `<div>Market Cap: ${formatLargeNumber(data.market_cap)}</div>`;
            }
            
            if (data.pe_ratio && data.pe_ratio !== 'N/A') {
                detailsHTML += `<div>P/E Ratio: ${Number(data.pe_ratio).toFixed(2)}</div>`;
            }
            
            if (data.fifty_two_week_low && data.fifty_two_week_high && data.fifty_two_week_low !== 'N/A') {
                detailsHTML += `<div>52-Wk Range: $${Number(data.fifty_two_week_low).toFixed(2)} - $${Number(data.fifty_two_week_high).toFixed(2)}</div>`;
            }
            
            stockDetails.innerHTML = detailsHTML;
        })
        .catch(error => {
            stockName.textContent = 'Stock Info Not Available';
            stockDetails.innerHTML = `<div class="text-muted small">${error.message || 'Could not load details'}</div>`;
        });
}

function formatLargeNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    
    if (num >= 1_000_000_000) {
        return `$${(num / 1_000_000_000).toFixed(2)}B`;
    } else if (num >= 1_000_000) {
        return `$${(num / 1_000_000).toFixed(2)}M`;
    } else if (num >= 1_000) {
        return `$${(num / 1_000).toFixed(2)}K`;
    }
    
    return `$${num.toFixed(2)}`;
}
