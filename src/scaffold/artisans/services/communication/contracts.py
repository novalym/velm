from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

@dataclass
class MessageEnvelope:
    """
    [THE SEALED LETTER]
    The normalized vessel that all Couriers understand.
    """
    to: List[str]
    subject: str
    body_text: str
    body_html: Optional[str] = None
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    attachments: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)