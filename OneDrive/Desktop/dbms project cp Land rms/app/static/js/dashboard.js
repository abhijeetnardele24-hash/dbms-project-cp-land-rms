// Advanced dashboard with charts and analytics
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips and popovers
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle=\"tooltip\"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Property Statistics Chart
    if (document.getElementById('propertyStatsChart')) {
        const ctx = document.getElementById('propertyStatsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Pending', 'Approved', 'Rejected', 'Under Review'],
                datasets: [{
                    label: 'Properties',
                    data: [12, 45, 5, 8],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Property Status Overview' }
                }
            }
        });
    }
    
    // Revenue Chart
    if (document.getElementById('revenueChart')) {
        const ctx = document.getElementById('revenueChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Revenue (₹ Lakhs)',
                    data: [65, 78, 90, 81, 96, 105],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                    title: { display: true, text: 'Monthly Revenue Trend' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
    
    // Property Distribution Pie Chart
    if (document.getElementById('propertyDistChart')) {
        const ctx = document.getElementById('propertyDistChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Residential', 'Commercial', 'Agricultural', 'Industrial'],
                datasets: [{
                    data: [45, 25, 20, 10],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    title: { display: true, text: 'Property Type Distribution' }
                }
            }
        });
    }
    
    // Load real-time notifications
    function loadNotifications() {
        fetch('/api/v1/notifications/unread')
            .then(response => response.json())
            .then(data => {
                if (data.count > 0) {
                    document.getElementById('notifCount').textContent = data.count;
                    document.getElementById('notifCount').style.display = 'inline';
                }
            })
            .catch(error => console.error('Error loading notifications:', error));
    }
    
    // Refresh notifications every 30 seconds
    setInterval(loadNotifications, 30000);
});
