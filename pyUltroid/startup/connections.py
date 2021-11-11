# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os

from redis import Redis
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from ..configs import Var
from . import *

def session_file():
    if os.path.exists("client-session.session"):
        _session = "client-session"
    elif Var.SESSION:
        _session = StringSession(Var.SESSION)
    else:
        raise Exception("No String Session found. Quitting...")
    return _session


def vc_connection(udB, ultroid_bot):
    VC_SESSION = Var.VC_SESSION or udB.get("VC_SESSION")
    if VC_SESSION and VC_SESSION != Var.SESSION:
        try:
            return TelegramClient(
                StringSession(VC_SESSION), api_id=Var.API_ID, api_hash=Var.API_HASH
            ).start()
        except (AuthKeyDuplicatedError, EOFError):
            LOGS.info(
                "Your VC_SESSION Expired. Deleting VC_SESSION from redis..."
                + "\nRenew/Change it to Use Voice/Video Chat from VC Account..."
            )
            udB.delete("VC_SESSION")
        except Exception as er:
            LOGS.error("VC_SESSION: {}".format(str(er)))
    return ultroid_bot


def where_hosted():
    if os.getenv("DYNO"):
        return "heroku"
    if os.getenv("RAILWAY_GIT_REPO_NAME"):
        return "railway"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery"
    if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "windows"
    if os.getenv("HOSTNAME"):
        return "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    return "local"
