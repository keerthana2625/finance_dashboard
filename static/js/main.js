// Personal Finance Dashboard general scripts
document.addEventListener('DOMContentLoaded', () => {
    
    // Auto-dismiss Django feedback messages after 5 seconds
    const alerts = document.querySelectorAll('.message-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Mobile Sidebar Toggle mechanism
    const sidebar = document.querySelector('.sidebar');
    const hamburger = document.querySelector('.hamburger');
    
    if (hamburger && sidebar) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('open');
        });

        // Close sidebar when clicking outside of it on mobile
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== hamburger) {
                sidebar.classList.remove('open');
            }
        });
    }
});
