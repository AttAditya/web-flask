from keys import SECRETS
import deta as deta_sh

deta = deta_sh.Deta(*[key for key in [SECRETS["DETA"]] if key])

content_db = deta.Base("Content")
tags_db = deta.Base("Tags")
content_dr = deta.Drive("Content-Drive")
thumbnails_dr = deta.Drive("Thumbnails")
picture_dr = deta.Drive("Pictures")
accounts_db = deta.Base("Accounts")
ads_db = deta.Base("Ads")
analytics_db = deta.Base("Analytics")
errors_db = deta.Base("Errors")

databases = {
    "content": content_db,
    "tags": tags_db,
    "content_drive": content_dr,
    "thumbnails_drive": thumbnails_dr,
    "picture_drive": picture_dr,
    "accounts": accounts_db,
    "ads": ads_db,
    "analytics": analytics_db,
    "errors": errors_db,
}