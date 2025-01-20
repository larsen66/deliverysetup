INSTALLED_APPS = [
    // ... existing code ...
    'ckeditor',
    'ckeditor_uploader',
    // ... existing code ...
]

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 