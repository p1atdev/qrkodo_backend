from cmath import e
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.svg import SvgImage, SvgFillImage, SvgFragmentImage, SvgPathImage, SvgPathFillImage
from qrcode.image.styles.moduledrawers import (
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


def generate_qrcode_from(
    text: str,
    version: int,
    error_correction: qrcode_schema.QRCodeErrorCorrection,
    size: int,
    border: int,
    fill_color: str,
    back_color: str,
    drawer: qrcode_schema.QRCodeDrawer,
    file_type: qrcode_schema.QRCodeFileType,
):
    _error_correction = None
    if error_correction == qrcode_schema.QRCodeErrorCorrection.L:
        _error_correction = qrcode.constants.ERROR_CORRECT_L
    elif error_correction == qrcode_schema.QRCodeErrorCorrection.M:
        _error_correction = qrcode.constants.ERROR_CORRECT_M
    elif error_correction == qrcode_schema.QRCodeErrorCorrection.Q:
        _error_correction = qrcode.constants.ERROR_CORRECT_Q
    elif error_correction == qrcode_schema.QRCodeErrorCorrection.H:
        _error_correction = qrcode.constants.ERROR_CORRECT_H
    else:
        raise HTTPException(status_code=400, detail="Invalid error_correction")

    _drawer = None
    if drawer == qrcode_schema.QRCodeDrawer.Square:
        _drawer = SquareModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.GappedSquare:
        _drawer = GappedSquareModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.Circle:
        _drawer = CircleModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.Rounded:
        _drawer = RoundedModuleDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.VerticalBars:
        _drawer = VerticalBarsDrawer()
    elif drawer == qrcode_schema.QRCodeDrawer.HorizontalBars:
        _drawer = HorizontalBarsDrawer()
    else:
        raise HTTPException(status_code=400, detail="Invalid drawer")

    _factory = None
    if file_type == qrcode_schema.QRCodeFileType.PNG:
        _factory = StyledPilImage
    elif file_type == qrcode_schema.QRCodeFileType.SVG:
        _factory = SvgImage
    elif file_type == qrcode_schema.QRCodeFileType.SVG_FRAGMENT:
        _factory = SvgFragmentImage
    elif file_type == qrcode_schema.QRCodeFileType.SVG_PATH:
        _factory = SvgPathImage
    else:
        raise HTTPException(status_code=400, detail="Invalid file_type")

    qr = qrcode.QRCode(
        version=version,
        error_correction=_error_correction,
        box_size=size,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=fill_color,
        back_color=back_color,
        image_factory=_factory,
        module_drawer=_drawer,
    )
    return img


@router.post("/api/qrcode")
async def generate_qrcode(param: qrcode_schema.QRGenerateParameter):
    # validate the param
    if param.version > 40 or param.version < 1:
        raise HTTPException(status_code=400, detail="version must be between 1 and 40")
    if param.border < 0:
        raise HTTPException(status_code=400, detail="border must be greater than 0")

    img = generate_qrcode_from(
        text=param.text,
        version=param.version,
        error_correction=param.error_correction,
        size=param.size,
        border=param.border,
        fill_color=param.fill_color,
        back_color=param.back_color,
        drawer=param.drawer,
        file_type=param.file_type,
    )

    if param.file_type == qrcode_schema.QRCodeFileType.PNG:
        image = io.BytesIO()
        img.save(image, format="PNG")
        image.seek(0)
        return StreamingResponse(
            image,
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=qrcode.png"},
        )
    elif param.file_type in [
        qrcode_schema.QRCodeFileType.SVG,
        qrcode_schema.QRCodeFileType.SVG_FRAGMENT,
        qrcode_schema.QRCodeFileType.SVG_PATH,
    ]:
        stream = io.BytesIO()
        img.save(stream=stream)
        stream.seek(0)
        svg = stream
        return StreamingResponse(
            svg,
            media_type="image/svg+xml",
            headers={"Content-Disposition": "inline; filename=qrcode.svg", "Content-Type": "image/svg+xml"},
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid file_type")
