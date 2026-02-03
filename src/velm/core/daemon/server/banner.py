# Path: core/daemon/server/banner.py
# ----------------------------------
# LIF: INFINITY | ROLE: VISUAL_IDENTITY
import sys
from ....logger import Scribe

def proclaim_banner(port: int, version: str):
    """
    [ASCENSION 6]: RICH BANNERS
    Prints the sacred sigil of the Daemon to stderr (for log visibility).
    """
    banner = f"""
   ______                     __  _      
  / ____/____   ____   _____ / /_(_)_____
 / / __ / __ \ / __ \ / ___// __// // __/
/ /_/ // / / // /_/ /(__  )/ /_ / // /__ 
\____//_/ /_/ \____//____/ \__//_/ \___/ 
:: GNOSTIC NEXUS :: v{version} :: PORT {port} ::
    """
    print(banner, file=sys.stderr)