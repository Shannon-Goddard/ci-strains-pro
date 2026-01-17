// Configuration
const API_ENDPOINT = 'https://wdl3umx2og7kdf447gfhaebpme0owqcb.lambda-url.us-east-1.on.aws/';

// DOM Elements
const urlInput = document.getElementById('url-input');
const lookupBtn = document.getElementById('lookup-btn');
const statusDiv = document.getElementById('status');
const metadataDiv = document.getElementById('metadata');
const viewerContainer = document.getElementById('viewer-container');
const htmlViewer = document.getElementById('html-viewer');
const seedBankSpan = document.getElementById('seed-bank');
const collectionDateSpan = document.getElementById('collection-date');
const expiresInSpan = document.getElementById('expires-in');
const legalModal = document.getElementById('legal-modal');
const acceptLegalBtn = document.getElementById('accept-legal');
const seedBankFilter = document.getElementById('seed-bank-filter');
const strainSearch = document.getElementById('strain-search');
const searchResults = document.getElementById('search-results');

// Inventory data (loaded from API or embedded)
let inventoryData = [];

// Check if user has accepted legal disclaimer
const LEGAL_ACCEPTED_KEY = 'ci_legal_accepted';

// Show legal modal on first visit
window.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem(LEGAL_ACCEPTED_KEY)) {
        legalModal.style.display = 'flex';
    }
    loadInventory();
});

// Handle legal acceptance
acceptLegalBtn.addEventListener('click', () => {
    localStorage.setItem(LEGAL_ACCEPTED_KEY, 'true');
    legalModal.style.display = 'none';
    trackEvent('legal_acceptance', { action: 'accepted' });
});

// Event Listeners
lookupBtn.addEventListener('click', handleLookup);
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleLookup();
});
seedBankFilter.addEventListener('change', handleFilterChange);
strainSearch.addEventListener('input', handleStrainSearch);

// Google Analytics tracking helper
function trackEvent(eventName, params = {}) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, params);
    }
}

// Load inventory data (mock for now - will be populated from Lambda)
async function loadInventory() {
    // TODO: Replace with actual API call to get inventory summary
    // For now, populate seed banks manually
    const seedBanks = [
        { name: 'Attitude Seed Bank', count: 7673 },
        { name: 'Crop King', count: 3336 },
        { name: 'North Atlantic', count: 2727 },
        { name: 'Gorilla Seed Bank', count: 2009 },
        { name: 'Neptune', count: 1995 },
        { name: 'Seedsman', count: 866 },
        { name: 'Multiverse Beans', count: 799 },
        { name: 'Herbies Seeds', count: 753 },
        { name: 'Sensi Seeds', count: 620 },
        { name: 'Seed Supreme', count: 353 },
        { name: 'Mephisto Genetics', count: 245 },
        { name: 'Exotic Genetix', count: 227 },
        { name: 'Amsterdam Marijuana', count: 163 },
        { name: 'ILGM', count: 133 },
        { name: 'Barney\'s Farm', count: 88 },
        { name: 'Royal Queen Seeds', count: 67 },
        { name: 'Dutch Passion', count: 44 },
        { name: 'Seeds Here Now', count: 43 },
        { name: 'Great Lakes Genetics', count: 16 },
        { name: 'Compound Genetics', count: 1 }
    ];
    
    // Populate dropdown
    seedBanks.forEach(bank => {
        const option = document.createElement('option');
        option.value = bank.name;
        option.textContent = `${bank.name} (${bank.count.toLocaleString()} strains)`;
        seedBankFilter.appendChild(option);
    });
}

// Handle seed bank filter change
function handleFilterChange() {
    const selectedBank = seedBankFilter.value;
    trackEvent('seed_bank_filter', { seed_bank: selectedBank || 'all' });
    
    if (selectedBank) {
        showStatus(`Filtered to ${selectedBank}. Enter a URL or search by strain name.`, 'success');
    } else {
        statusDiv.classList.add('hidden');
    }
    searchResults.classList.add('hidden');
}

// Handle strain search
function handleStrainSearch() {
    const query = strainSearch.value.trim().toLowerCase();
    
    if (query.length < 3) {
        searchResults.classList.add('hidden');
        return;
    }
    
    trackEvent('strain_search', { query: query });
    
    // TODO: Replace with actual search API call
    // For now, show placeholder message
    searchResults.innerHTML = `
        <p class="search-placeholder">
            🔍 Searching for "${query}"...<br>
            <small>Full search functionality will be available after Lambda deployment.</small>
        </p>
    `;
    searchResults.classList.remove('hidden');
}

// Main lookup function
async function handleLookup() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showStatus('Please enter a URL', 'error');
        return;
    }
    
    // Validate URL format
    try {
        new URL(url);
    } catch (e) {
        showStatus('Invalid URL format', 'error');
        return;
    }
    
    // Show loading state
    lookupBtn.disabled = true;
    lookupBtn.textContent = 'Loading...';
    showStatus('Looking up strain in inventory...', 'loading');
    hideMetadata();
    hideViewer();
    
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            trackEvent('lookup_error', { error: data.error, url: url });
            throw new Error(data.error || 'Failed to lookup URL');
        }
        
        // Success - display results
        trackEvent('lookup_success', { seed_bank: data.seed_bank, url: url });
        showStatus('✅ Source HTML found! Loading archive...', 'success');
        displayMetadata(data);
        displayHTML(data.signed_url);
        
    } catch (error) {
        showStatus(`❌ Error: ${error.message}`, 'error');
    } finally {
        lookupBtn.disabled = false;
        lookupBtn.textContent = 'View Source';
    }
}

// Display status message
function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.classList.remove('hidden');
}

// Display metadata
function displayMetadata(data) {
    seedBankSpan.textContent = data.seed_bank;
    collectionDateSpan.textContent = data.collection_date;
    expiresInSpan.textContent = `${data.expires_in_minutes} minutes`;
    metadataDiv.classList.remove('hidden');
}

// Display HTML in iframe
function displayHTML(signedUrl) {
    htmlViewer.src = signedUrl;
    viewerContainer.classList.remove('hidden');
    
    // Start expiration countdown
    startExpirationTimer(5);
}

// Hide metadata
function hideMetadata() {
    metadataDiv.classList.add('hidden');
}

// Hide viewer
function hideViewer() {
    viewerContainer.classList.add('hidden');
    htmlViewer.src = '';
}

// Expiration countdown timer
function startExpirationTimer(minutes) {
    let seconds = minutes * 60;
    
    const interval = setInterval(() => {
        seconds--;
        
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        expiresInSpan.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
        
        if (seconds <= 0) {
            clearInterval(interval);
            showStatus('⏰ Signed URL expired. Please request a new one.', 'error');
            hideViewer();
        }
    }, 1000);
}

// Sample URLs for testing (optional - can be removed)
const sampleUrls = [
    'https://www.northatlanticseed.com/product/og-kush-f-3/',
    'https://www.seedsman.com/us-en/platinum-green-apple-candy-feminized-seeds-atl-pgac-fem',
    'https://ilgm.com/products/critical-mass-feminized-seeds'
];

// Add sample URL on page load (optional - can be removed)
if (urlInput.value === '') {
    urlInput.value = sampleUrls[0];
}
