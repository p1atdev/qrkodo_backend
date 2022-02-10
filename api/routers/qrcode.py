from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import  (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
    CircleModuleDrawer,
)
import io

import api.schemas.qrcode as qrcode_schema

router = APIRouter()

def generate_qrcode_from(text, size=32, border=4, fill_color="#000000", back_color="#ffffff", drawer=qrcode_schema.QRCodeDrawer.Square):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    module_drawer = None
    if drawer == qrcode_schema.QRCodeDrawer.Square:
        module_drawer = SquareModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.GappedSquare:
        module_drawer = GappedSquareModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.Circle:
        module_drawer = CircleModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.Rounded:
        module_drawer = RoundedModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.VerticalBars:
        module_drawer = VerticalBarsDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.HorizontalBars:
        module_drawer = HorizontalBarsDrawer()
    else:
        module_drawer = SquareModuleDrawer()

    img = qr.make_image(fill_color=fill_color, back_color=back_color, image_factory=StyledPilImage, module_drawer=module_drawer)
    return img

@router.post("/api/qrcode")
async def generate_qrcode(param: qrcode_schema.QRGenerateParameter):
    img = generate_qrcode_from(param.text, param.size, param.border, param.fill_color, param.back_color, param.drawer)
    stream = io.BytesIO()
    img.save(stream, format="PNG")
    stream.seek(0)
    return StreamingResponse(stream, media_type="image/png")