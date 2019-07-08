# -*- mode: python -*-

block_cipher = None


a = Analysis(['ball_plate.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + [('resources/images/icon.png', 'src/resources/images/icon.png', 'DATA'),
                     ('resources/images/gui.png', 'src/resources/images/gui.png', 'DATA'),
                     ('resources/scripts/start_ap.zsh', 'src/resources/scripts/start_ap.zsh', 'DATA'),
                     ('resources/scripts/stop_ap.zsh', 'src/resources/scripts/stop_ap.zsh', 'DATA')],
          name='ball_plate',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='src\\resources\\images\\icon.ico')
