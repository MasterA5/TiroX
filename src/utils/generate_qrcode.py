import base64
import io
import json

import qrcode

from core.RegisterManager import Register


def generate_qrcode(register: Register) -> str:
    data = {
        "value": register.value,
        "hormone": register.hormone,
    }

    json_data = json.dumps(data)

    qr = qrcode.make(json_data)

    buffer = io.BytesIO()
    qr.save(buffer)

    img_bytes = buffer.getvalue()
    base64_string = base64.b64encode(img_bytes).decode("utf-8")

    return base64_string
