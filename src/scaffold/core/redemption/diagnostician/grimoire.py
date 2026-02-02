# Path: scaffold/core/redemption/diagnostician/grimoire.py
# --------------------------------------------------------

"""
=================================================================================
== THE BOOK OF KNOWN NAMES (V-Ω-KNOWLEDGE-BASE)                                ==
=================================================================================
The static memory of the Doctor. Maps symptoms to known remedies.
"""

# Maps Python import names to PyPI package names
PACKAGE_MAP = {
    "yaml": "PyYAML",
    "PIL": "Pillow",
    "dotenv": "python-dotenv",
    "jwt": "pyjwt",
    "cv2": "opencv-python",
    "bs4": "beautifulsoup4",
    "sklearn": "scikit-learn",
    "docker": "docker",
    "rich": "rich",
    "textual": "textual",
    "pathspec": "pathspec",
    "scaffold_core_rs": "scaffold-core-rs",
    "dateutil": "python-dateutil",
    "boto3": "boto3",
    "requests": "requests",
}

# Maps system binaries to their installation pages/commands
BINARY_INSTALL_MAP = {
    "git": "https://git-scm.com/downloads",
    "docker": "https://www.docker.com/products/docker-desktop",
    "node": "https://nodejs.org",
    "npm": "https://nodejs.org",
    "go": "https://go.dev/dl/",
    "rustc": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
    "terraform": "https://developer.hashicorp.com/terraform/downloads",
}