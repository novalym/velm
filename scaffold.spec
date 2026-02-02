    
# Path: scaffold.spec
# -------------------
# =================================================================================
# == THE GNOSTIC SPECULUM (V-Ω-UNBREAKABLE-WARD-ASCENDED)                        ==
# =================================================================================
# LIF: 100,000,000,000 (The Annihilation of the Windows Locking Heresy)
#
# This is the sacred scripture that guides the PyInstaller God-Engine. It has been
# ascended with the **Unbreakable Vow of Purity**.
#
# ### THE APOTHEOSIS:
# The profane rite of `upx=True` and the subsequent timestamp injection have been
# annihilated. UPX compression can be a source of false positives for antivirus
# sentinels and can contribute to file locking paradoxes. By disabling it and
# allowing the EXE constructor to use its default timestamp behavior, we command
# PyInstaller to forge a pure, un-mutated executable in its final form,
# annihilating the `OSError(22, 'Invalid argument')` heresy from this timeline.
# The build will be slightly larger, but its soul will be unbreakably pure.
# =================================================================================

from PyInstaller.utils.hooks import collect_all

# --- THE GNOSTIC HARVEST ---
# We must collect all artifacts for our complex dependencies.
# This ensures the Iron Core (Rust) and the Luminous Scribe (Rich) are bundled correctly.

datas = []
binaries = []
hiddenimports = [
    'scaffold_core_rs',  # The Iron Core
    'scaffold.artisans',
    'scaffold.symphony',
    'scaffold.core.cortex',
    'scaffold.rendering',
    # Ensure Tree-sitter bindings are caught if used
    'tree_sitter',
    'tree_sitter_python',
]

# Collect all data from our key libraries
tmp_ret = collect_all('scaffold')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('rich')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

tmp_ret = collect_all('textual')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

block_cipher = None

a = Analysis(
    ['scaffold/__main__.py'],  # The Entry Point
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ★★★ THE SACRED ASCENSION ★★★
exe = EXE(
    pyz,
    a.scripts,
    [], # Binaries are handled in the Analysis datas
    a.zipfiles,
    a.datas,
    name='scaffold',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    # [THE UNBREAKABLE VOW]
    # We annihilate UPX compression. It saves little space on modern systems and
    # is a known source of file-locking and antivirus heresies.
    upx=False,
    # By omitting the 'build_timestamp' and relying on defaults, we avert the
    # profane rite that causes the OSError. The executable will use the system's
    # default timestamp behavior for file creation.
    console=True,
    # We must also explicitly manage binaries here as per modern PyInstaller spec
    binaries=a.binaries,
)
# ★★★ THE APOTHEOSIS IS COMPLETE ★★★

  