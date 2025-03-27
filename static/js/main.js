// Main JavaScript file for the Content Management Website

document.addEventListener('DOMContentLoaded', function() {
    // 3-dot menu toggle
    const menuToggle = document.querySelector('.nav-menu-dots');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('show');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (navMenu.classList.contains('show') && !navMenu.contains(e.target)) {
                navMenu.classList.remove('show');
            }
        });
    }
    
    // Set active menu item based on current page
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.nav-menu a');
    
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (currentPath === href || 
            (href !== '/' && currentPath.startsWith(href))) {
            item.classList.add('active');
        }
    });
    
    // Video embed handling
    function setupVideoEmbeds() {
        const videoContainers = document.querySelectorAll('.video-embed-container');
        
        videoContainers.forEach(container => {
            const videoUrl = container.dataset.videoUrl;
            if (!videoUrl) return;
            
            let embedHtml = '';
            
            // YouTube
            if (videoUrl.includes('youtube.com') || videoUrl.includes('youtu.be')) {
                const youtubeId = extractYoutubeId(videoUrl);
                if (youtubeId) {
                    embedHtml = `<iframe width="100%" height="315" src="https://www.youtube.com/embed/${youtubeId}" 
                                 frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
                                 gyroscope; picture-in-picture" allowfullscreen></iframe>`;
                }
            }
            // Vimeo
            else if (videoUrl.includes('vimeo.com')) {
                const vimeoId = extractVimeoId(videoUrl);
                if (vimeoId) {
                    embedHtml = `<iframe src="https://player.vimeo.com/video/${vimeoId}" width="100%" 
                                 height="315" frameborder="0" allow="autoplay; fullscreen; 
                                 picture-in-picture" allowfullscreen></iframe>`;
                }
            }
            // Google Drive
            else if (videoUrl.includes('drive.google.com')) {
                const driveId = extractGoogleDriveId(videoUrl);
                if (driveId) {
                    embedHtml = `<iframe src="https://drive.google.com/file/d/${driveId}/preview" 
                                 width="100%" height="315" frameborder="0" allowfullscreen></iframe>`;
                }
            }
            // Default - show as link
            else {
                embedHtml = `<div class="alert alert-info">
                              Video available at: <a href="${videoUrl}" target="_blank">${videoUrl}</a>
                             </div>`;
            }
            
            container.innerHTML = embedHtml;
        });
    }
    
    // Extract video IDs from various platforms
    function extractYoutubeId(url) {
        const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
        const match = url.match(regExp);
        return (match && match[7].length === 11) ? match[7] : null;
    }
    
    function extractVimeoId(url) {
        const regExp = /vimeo\.com\/(?:channels\/(?:\w+\/)?|groups\/([^\/]*)\/videos\/|)(\d+)(?:|\/\?)/;
        const match = url.match(regExp);
        return match ? match[2] : null;
    }
    
    function extractGoogleDriveId(url) {
        const regExp = /drive\.google\.com\/file\/d\/([^\/\?&]+)/;
        const match = url.match(regExp);
        return match ? match[1] : null;
    }
    
    // Call setup function for video embeds
    setupVideoEmbeds();
    
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});
