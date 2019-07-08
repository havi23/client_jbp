# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             #pathex=['C:\\Users\\Max\\PycharmProjects\\client_jbp'],
             pathex=['C:\\Users\\Havi\\Documents\\GitHub\\client_jbp'],
             binaries=[],
             #datas=[("C:\\Users\\Max\\PycharmProjects\\client_jbp\\ui\\img", "ui")],
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

#a.datas += [("bug_report.bmp", "C:\\Users\\Max\PycharmProjects\\client_jbp\\ui\\img\\bug_report.bmp", "DATA")]
a.datas += [("bug_report.bmp", "C:\\Users\\Havi\\Documents\\GitHub\\client_jbp\\ui\\img\\bug_report.bmp", "DATA")]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
