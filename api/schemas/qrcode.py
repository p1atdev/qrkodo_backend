import enum
from typing import Optional
from click import style
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

class QRCodeDrawer(enum.Enum):
    Square: str = "Square"
    GappedSquare: str = "GappedSquare"
    Circle: str = "Circle"
    Rounded: str = "Rounded"
    VerticalBars: str = "VerticalBars"
    HorizontalBars: str = "HorizontalBars"

class QRCodeStyle(BaseModel):
    size: int = Field(example=32, description="QRコードのサイズ")
    border: int = Field(example=4, description="QRコードの枠")
    fill_color: str = Field(default="#000000", description="QRコードの色")
    back_color: str = Field(default="#ffffff", description="QRコードの背景色")
    drawer: QRCodeDrawer = Field(default=QRCodeDrawer.Square, description="QRコードの描画方法")

class QRGenerateParameter(QRCodeStyle):
    text: str = Field(..., example="https://example.com", description="QRコードの文字列")

