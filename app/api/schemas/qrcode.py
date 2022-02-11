import enum
from typing import Optional

from pydantic import BaseModel, Field


class QRCodeDrawer(enum.Enum):
    Square: str = "Square"
    GappedSquare: str = "GappedSquare"
    Circle: str = "Circle"
    Rounded: str = "Rounded"
    VerticalBars: str = "VerticalBars"
    HorizontalBars: str = "HorizontalBars"


class QRCodeErrorCorrection(enum.Enum):
    L: str = "L"
    M: str = "M"
    Q: str = "Q"
    H: str = "H"


class QRCodeFileType(enum.Enum):
    PNG: str = "png"
    SVG: str = "svg"
    SVG_FRAGMENT: str = "svg_fragment"
    SVG_PATH: str = "svg_path"
    # JPG: str = "jpg"


class QRCodeStyle(BaseModel):
    version: Optional[int] = Field(example=1, description="QRコードサイズ")
    error_correction: Optional[QRCodeErrorCorrection] = Field(example=QRCodeErrorCorrection.M, description="誤り訂正レベル")
    size: Optional[int] = Field(example=10, description="QRコードのセルのサイズ")
    border: Optional[int] = Field(example=4, description="QRコードの枠")
    fill_color: Optional[str] = Field(default="#000000", description="QRコードの色")
    back_color: Optional[str] = Field(default="#ffffff", description="QRコードの背景色")
    drawer: Optional[QRCodeDrawer] = Field(default=QRCodeDrawer.Square, description="QRコードの描画方法")
    file_type: Optional[QRCodeFileType] = Field(default=QRCodeFileType.PNG, description="出力ファイルの種類")


class QRGenerateParameter(QRCodeStyle):
    text: str = Field(..., example="https://example.com", description="QRコードの文字列")
