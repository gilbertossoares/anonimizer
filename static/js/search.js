let currentPage = 1;
let currentQuery = '';
let totalResults = 0;

document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    currentPage = 1;
    currentQuery = document.getElementById('searchInput').value;
    searchBackend(currentQuery, currentPage);
});

document.getElementById('perPageSelect').addEventListener('change', function() {
    if (currentQuery) {
        currentPage = 1;
        searchBackend(currentQuery, currentPage);
    }
});

function searchBackend(query, page) {
    const perPage = parseInt(document.getElementById('perPageSelect').value);
    
    fetch('/search/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            query: query,
            page: page,
            perPage: perPage
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Search response:', data); 
        totalResults = data.total;
        displayResults(data.results, query);
        displayPagination(data.total, perPage, page);
    })
    .catch(error => {
        console.error('Error:', error);
        displayError('An error occurred while fetching search results.');
    });
}

function displayPagination(total, perPage, currentPage) {
    const totalPages = Math.ceil(total / perPage);
    const paginationContainer = document.getElementById('pagination');
    paginationContainer.innerHTML = '';

    if (totalPages <= 1) return;

    const fragment = document.createDocumentFragment();

   
    if (currentPage > 1) {
        const prevButton = createPaginationButton('Previous', currentPage - 1);
        fragment.appendChild(prevButton);
    }

   
    for (let i = 1; i <= totalPages; i++) {
        if (
            i === 1 || 
            i === totalPages || 
            (i >= currentPage - 2 && i <= currentPage + 2)
        ) {
            const pageButton = createPaginationButton(i.toString(), i);
            if (i === currentPage) {
                pageButton.classList.add('active');
            }
            fragment.appendChild(pageButton);
        } else if (
            i === currentPage - 3 || 
            i === currentPage + 3
        ) {
            const ellipsis = document.createElement('span');
            ellipsis.textContent = '...';
            ellipsis.className = 'pagination-ellipsis';
            fragment.appendChild(ellipsis);
        }
    }

  
    if (currentPage < totalPages) {
        const nextButton = createPaginationButton('Next', currentPage + 1);
        fragment.appendChild(nextButton);
    }

    paginationContainer.appendChild(fragment);
}

function createPaginationButton(text, page) {
    const button = document.createElement('button');
    button.textContent = text;
    button.className = 'pagination-button';
    button.addEventListener('click', () => {
        currentPage = page;
        searchBackend(currentQuery, page);
    });
    return button;
}

function displayResults(results, query) {
    const resultsContainer = document.getElementById('results');
    const resultsCount = document.getElementById('resultsCount');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsCount.textContent = 'No matching results';
        return;
    }

    resultsCount.textContent = `Total results: ${totalResults} - Showing ${results.length} items`;

    const fragment = document.createDocumentFragment();
    results.forEach(result => {
        const resultItem = createResultItem(result, query);
        fragment.appendChild(resultItem);
    });
    resultsContainer.appendChild(fragment);
}

function createResultItem(result, query) {
    const resultItem = document.createElement('li');
    resultItem.className = 'result-item';
    const highlightedText = getHighlightedSnippet(result.merged_content, query);
    resultItem.innerHTML = `
        <p>${highlightedText}</p>
        <p><strong>File Name:</strong> ${result.metadata_storage_name}</p>
    `;
    resultItem.addEventListener('click', () => {
        displayImage(result.metadata_storage_path);
    });
    return resultItem;
}

function getHighlightedSnippet(text, term) {
    const termIndex = text.toLowerCase().indexOf(term.toLowerCase());
    if (termIndex === -1) return text;
    const start = Math.max(0, termIndex - 60);
    const end = Math.min(text.length, termIndex + term.length + 60);
    const snippet = text.substring(start, end);

    const regex = new RegExp(`(${term})`, 'gi');
    return snippet.replace(regex, '<span class="highlight">$1</span>');
}

function displayImage(encodedPath) {
    const imageViewer = document.getElementById('imageViewer');
    const iframeViewer = document.getElementById('imageFrame');

    
    let decodedPath = atob(encodedPath.replace(/=+$/, '').replace(/0$/, ''));

    
    decodedPath = decodedPath.replace(/(\.png)5$/, '$1');

    iframeViewer.src = decodedPath;
    imageViewer.style.display = 'block';
}


document.getElementById('closeButton').addEventListener('click', function() {
    const imageViewer = document.getElementById('imageViewer');
    imageViewer.style.display = 'none';  
});

function displayError(message) {
    const resultsContainer = document.getElementById('results');
    const resultsCount = document.getElementById('resultsCount');
    resultsContainer.innerHTML = '';
    resultsCount.textContent = message;
}

document.getElementById('results').addEventListener('click', function(event) {
    if (event.target.tagName === 'IMG') {
        const imageUrl = event.target.src;
        document.getElementById('imageFrame').src = imageUrl;
        document.getElementById('imageViewer').style.display = 'block';
    }
});

document.getElementById('closeButton').addEventListener('click', function() {
    document.getElementById('imageViewer').style.display = 'none';
});