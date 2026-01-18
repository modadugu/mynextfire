// Simple client-side search functionality
(function() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  if (!searchInput || !searchResults) return;

  let posts = [];

  // Load posts data from JSON file
  fetch('/mynextfire/search.json')
    .then(response => response.json())
    .then(data => {
      posts = data;
    })
    .catch(() => {
      console.log('Search data not available');
    });

  function performSearch(query) {
    if (!query || query.trim().length < 2 || posts.length === 0) {
      searchResults.innerHTML = '';
      return;
    }

    const lowerQuery = query.toLowerCase();
    const matchedPosts = posts.filter(post => {
      const titleMatch = post.title && post.title.toLowerCase().includes(lowerQuery);
      const contentMatch = post.content && post.content.toLowerCase().includes(lowerQuery);
      const tagMatch = post.tags && post.tags.some(tag => tag.toLowerCase().includes(lowerQuery));
      return titleMatch || contentMatch || tagMatch;
    });

    displayResults(matchedPosts, query);
  }

  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-results">No posts found matching "' + query + '"</div>';
      return;
    }

    let html = '<h3>Search Results (' + results.length + ')</h3><ul class="post-list">';
    
    results.forEach(post => {
      const excerpt = post.excerpt || post.content.substring(0, 150) + '...';
      html += `
        <li class="post-item">
          <div class="post-item-text">
            <h3><a href="${post.url}">${post.title}</a></h3>
            <p class="post-meta">${post.date}</p>
            <div class="post-excerpt">${excerpt}</div>
          </div>
        </li>
      `;
    });
    
    html += '</ul>';
    searchResults.innerHTML = html;
  }

  // Debounce search input
  let searchTimeout;
  searchInput.addEventListener('input', function(e) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      performSearch(e.target.value);
    }, 300);
  });
})();
