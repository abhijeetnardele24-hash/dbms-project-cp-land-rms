// DataTables initialization with advanced features
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all data tables
    .data-table.DataTable({
        responsive: true,
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, 'All']],
        dom: '<\"row\"<\"col-sm-12 col-md-6\"l><\"col-sm-12 col-md-6\"f>>' +
             '<\"row\"<\"col-sm-12\"tr>>' +
             '<\"row\"<\"col-sm-12 col-md-5\"i><\"col-sm-12 col-md-7\"p>>B',
        buttons: [
            { extend: 'copy', className: 'btn btn-sm btn-secondary' },
            { extend: 'csv', className: 'btn btn-sm btn-secondary' },
            { extend: 'excel', className: 'btn btn-sm btn-secondary' },
            { extend: 'pdf', className: 'btn btn-sm btn-secondary' },
            { extend: 'print', className: 'btn btn-sm btn-secondary' }
        ],
        language: {
            search: '_INPUT_',
            searchPlaceholder: 'Search records...'
        }
    });
});

// Advanced search functionality
function initAdvancedSearch() {
    const searchForm = document.getElementById('advancedSearchForm');
    if (!searchForm) return;
    
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const params = new URLSearchParams(formData);
        
        fetch(/api/v1/properties/search?)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data.results);
            })
            .catch(error => console.error('Search error:', error));
    });
}

function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<div class=\"alert alert-info\">No properties found matching your criteria.</div>';
        return;
    }
    
    let html = '<div class=\"row\">';
    results.forEach(property => {
        html += 
            <div class=\"col-md-6 col-lg-4 mb-3\">
                <div class=\"card h-100\">
                    <div class=\"card-body\">
                        <h5 class=\"card-title\"></h5>
                        <p class=\"card-text\">
                            <strong>Location:</strong> <br>
                            <strong>Area:</strong>  <br>
                            <strong>Value:</strong> ₹
                        </p>
                        <a href=\"/property/\" class=\"btn btn-sm btn-primary\">View Details</a>
                    </div>
                </div>
            </div>
        ;
    });
    html += '</div>';
    container.innerHTML = html;
}
