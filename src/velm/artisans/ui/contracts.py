# Path: artisans/ui/contracts.py
from typing import Optional, Literal
from pydantic import Field
from ...interfaces.requests import BaseRequest

class UIRequest(BaseRequest):
    """
    The sacred plea to materialze the Sovereign UI.
    """
    port: int = Field(default=7860, ge=1024, le=65535, description="The Localhost Port.")
    host: str = Field(default="127.0.0.1", description="The Network Interface.")
    mode: Literal["production", "development"] = Field(default="production")
    no_browser: bool = Field(default=False, description="Suppress browser auto-opening.")
    adrenaline: bool = Field(default=True, description="Force high-performance I/O.")