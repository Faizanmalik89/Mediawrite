// JavaScript for Admin Panel functionality

document.addEventListener('DOMContentLoaded', function() {
    // Rich text editor initialization for blog content using Summernote
    if (document.querySelector('#content')) {
        $('#content').summernote({
            placeholder: 'Write your blog content here...',
            tabsize: 2,
            height: 300,
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']]
            ]
        });
    }
    
    // Video URL preview functionality
    const videoUrlInput = document.querySelector('#video_url');
    const previewBtn = document.querySelector('#preview-video-btn');
    const previewContainer = document.querySelector('#video-preview');
    
    if (videoUrlInput && previewBtn && previewContainer) {
        previewBtn.addEventListener('click', function() {
            const videoUrl = videoUrlInput.value.trim();
            if (!videoUrl) {
                previewContainer.innerHTML = '<div class="alert alert-warning">Please enter a video URL.</div>';
                return;
            }
            
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
                              Preview not available for this URL. Check if it's a supported video platform.
                             </div>`;
            }
            
            previewContainer.innerHTML = embedHtml;
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
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.delete-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Image URL preview for blog posts
    const imageUrlInput = document.querySelector('#featured_image');
    const imagePreviewBtn = document.querySelector('#preview-image-btn');
    const imagePreviewContainer = document.querySelector('#image-preview');
    
    if (imageUrlInput && imagePreviewBtn && imagePreviewContainer) {
        imagePreviewBtn.addEventListener('click', function() {
            const imageUrl = imageUrlInput.value.trim();
            if (!imageUrl) {
                imagePreviewContainer.innerHTML = '<div class="alert alert-warning">Please enter an image URL.</div>';
                return;
            }
            
            imagePreviewContainer.innerHTML = `<img src="${imageUrl}" class="img-fluid rounded" alt="Featured image preview">`;
        });
    }
    
    // Toggle between blog form and blog list in mobile view
    const toggleFormBtn = document.querySelector('#toggle-form-btn');
    const blogForm = document.querySelector('#blog-form-container');
    const blogList = document.querySelector('#blog-list-container');
    
    if (toggleFormBtn && blogForm && blogList) {
        toggleFormBtn.addEventListener('click', function() {
            if (blogForm.classList.contains('d-none')) {
                blogForm.classList.remove('d-none');
                blogList.classList.add('d-none');
                toggleFormBtn.textContent = 'View Blogs';
            } else {
                blogForm.classList.add('d-none');
                blogList.classList.remove('d-none');
                toggleFormBtn.textContent = 'Add New Blog';
            }
        });
    }
    
    // Similar toggle for videos
    const toggleVideoFormBtn = document.querySelector('#toggle-video-form-btn');
    const videoForm = document.querySelector('#video-form-container');
    const videoList = document.querySelector('#video-list-container');
    
    if (toggleVideoFormBtn && videoForm && videoList) {
        toggleVideoFormBtn.addEventListener('click', function() {
            if (videoForm.classList.contains('d-none')) {
                videoForm.classList.remove('d-none');
                videoList.classList.add('d-none');
                toggleVideoFormBtn.textContent = 'View Videos';
            } else {
                videoForm.classList.add('d-none');
                videoList.classList.remove('d-none');
                toggleVideoFormBtn.textContent = 'Add New Video';
            }
        });
    }
});
