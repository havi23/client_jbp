# -*- mode: python -*-

block_cipher = None

# pyinstaller --onefile --noconsole main.spec
a = Analysis(['script_launcher.py'],
             pathex=['C:\\Users\\Max\Documents\\GitHub\\client_jbp'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5','PyQt5.QtNetwork','PyQt5.QtMultimedia','PyQt5.QtCore','PyQt5.QtGui','PyQt5.QtWidgets','cv2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

#a.datas += [("ui\\img\\bug_report.bmp", "C:\\Users\\Havi\\Documents\\GitHub\\client_jbp\\ui\\img\\bug_report.bmp", "DATA")]
#a.datas += [("ui\\img\\bug_report.bmp", "C:\\Users\\Max\Documents\\GitHub\\client_jbp\\ui\\img\\bug_report.bmp", "DATA")]
#a.datas += [("ui\\img\\info_bg.png", "C:\\Users\\Max\Documents\\GitHub\\client_jbp\\ui\\img\\info_bg.png", "DATA")]
a.datas += [("data", "C:\\Users\\Max\Documents\\GitHub\\client_jbp\\data", "DATA")]


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          Tree('C:\\Users\\Max\Documents\\GitHub\\client_jbp\\bin', prefix='bin\\'),
          a.datas,
          [],
          name='script',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
