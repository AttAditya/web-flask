from .base import Base
from .drive import Drive

databases = {
    "content": Base("Content"),
    "tags": Base("Tags"),
    "content_drive": Drive("ContentDrive"),
    "thumbnails_drive": Drive("ThumbnailsDrive"),
    "picture_drive": Drive("PicturesDrive"),
    "accounts": Base("Accounts"),
    "ads": Base("Ads"),
    "analytics": Base("Analytics"),
    "errors": Base("Errors")
}