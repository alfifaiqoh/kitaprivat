import os
import base64
from datetime import datetime
from uuid import uuid4
from flask import current_app
from werkzeug.utils import secure_filename


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
