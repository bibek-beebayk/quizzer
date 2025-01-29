from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django_ckeditor_5",
    "django_summernote",
    "pwa",
    "apps.qna",
    "apps.users",
    "apps.blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.libs.middleware.APILogMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media/"


import os

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PWA settings

PWA_APP_NAME = "quizNfacts"
PWA_APP_DESCRIPTION = "A place to read and test your knowledge. Read informative blogs and take quizzes to test your knowledge on different topics."
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_START_URL = "/"
PWA_APP_ICONS = [
    {
        "src": "/static/images/appicon.png",
        "sizes": "192x192",
        "type": "image/jpg",
    },
    {
        "src": "/static/images/appicon.png",
        "sizes": "512x512",
        "type": "image/jpg",
    },
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"

AUTH_USER_MODEL = "users.User"
EMAIL_SUBJECT_PREFIX = "[QUIZZER] "

# Ckeditor5 settings
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_FILE_STORAGE = "core.libs.storage.CKEditorR2Storage"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "fontFamily",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "imageUpload",
            "imageResize",
            "imageStyle:alignLeft",
            "imageStyle:alignCenter",
            "imageStyle:alignRight",
        ],
        # "plugins": ["Image", "ImageResize"],
        # "image": {
        #     "resizeUnit": "%",
        #     "resizeOptions": [
        #         {"name": "resizeImage:original", "value": None, "label": "Original"},
        #         {"name": "resizeImage:50", "value": "50", "label": "50%"},
        #         {"name": "resizeImage:75", "value": "75", "label": "75%"},
        #     ],
        #     "toolbar": [
        #         "imageStyle:alignLeft",
        #         "imageStyle:alignCenter",
        #         "imageStyle:alignRight",
        #         "|",
        #         "resizeImage",
        #     ],
        # },
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    "iframe": True,
    # Or, you can set it to `False` to use SummernoteInplaceWidget by default - no iframe mode
    # In this case, you have to load Bootstrap/jQuery sources and dependencies manually.
    # Use this when you're already using Bootstrap/jQuery based themes.
    "iframe": False,
    # You can put custom Summernote settings
    "summernote": {
        # As an example, using Summernote Air-mode
        "airMode": False,
        # Change editor size
        "width": "100%",
        "height": "480",
        # Use proper language setting automatically (default)
        "lang": None,
        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        "toolbar": [
            ["style", ["style"]],
            ["font", ["bold", "underline", "clear"]],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "video"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
        # Or, explicitly set language/locale for editor
        # You can also add custom settings for external plugins
        "print": {
            "stylesheetUrl": "/some_static_folder/printable.css",
        },
        "codemirror": {
            "mode": "htmlmixed",
            "lineNumbers": "true",
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            "theme": "monokai",
        },
    },
    # Require users to be authenticated for uploading attachments.
    "attachment_require_authentication": True,
    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),
    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',
    # Set custom model for attachments (default: 'django_summernote.Attachment')
    # 'attachment_model': 'my.custom.attachment.model',
    # You can completely disable the attachment feature.
    "disable_attachment": False,
    # Set to `False` to return attachment paths in relative URIs.
    "attachment_absolute_uri": True,
    # test_func in summernote upload view. (Allow upload images only when user passes the test)
    # https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
    # 'test_func_upload_view': example_test_func,
    # You can add custom css/js for SummernoteWidget.
    "css": (),
    "js": (),
    # You can also add custom css/js for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    "css_for_inplace": (),
    "js_for_inplace": (),
    # Codemirror as codeview
    # If any codemirror settings are defined, it will include codemirror files automatically.
    "css": (
        "//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css",
    ),
    # Lazy initialization
    # If you want to initialize summernote at the bottom of page, set this as True
    # and call `initSummernote()` on your page.
    "lazy": True,
    # To use external plugins,
    # Include them within `css` and `js`.
    "js": {
        "/some_static_folder/summernote-ext-print.js",
        "//somewhere_in_internet/summernote-plugin-name.js",
    },
}

SITE_ID = 1
DOMAIN = "quiznfacts.com"
SITE_NAME = "quizNfacts"