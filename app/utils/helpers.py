import os
import base64
from datetime import datetime
from uuid import uuid4
from urllib.parse import quote
from flask import current_app, request
from werkzeug.utils import secure_filename

WA_NUMBER = '6283877345020'


def _is_mobile_ua():
    ua = request.headers.get('User-Agent', '').lower()
    return any(x in ua for x in ('android', 'iphone', 'ipad', 'windows phone', 'mobile'))


def wa_chat_url(message):
    text = quote(message)
    if _is_mobile_ua():
        return f"https://wa.me/{WA_NUMBER}?text={text}"
    return f"https://web.whatsapp.com/send?phone={WA_NUMBER}&text={text}"


def save_base64_image(data, subdir=''):
    if not data:
        return None
    try:
        header, encoded = data.split(',', 1)
        ext = header.split(';')[0].split('/')[-1]
        if ext not in ('png', 'jpg', 'jpeg', 'gif'):
            ext = 'png'
        filename = f"{uuid4().hex}.{ext}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], subdir, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(encoded))
        return filename
    except Exception:
        return None


def format_currency(value):
    if value is None:
        return 'Rp 0'
    return f"Rp {value:,.0f}".replace(',', '.')
