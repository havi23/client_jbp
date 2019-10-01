from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE, TOC


def collect_pkg_data(package, include_py_files=False, subdir=None):
    import os
    from PyInstaller.utils.hooks import get_package_paths, remove_prefix, PY_IGNORE_EXTENSIONS

    # Accept only strings as packages.
    if type(package) is not str:
        raise ValueError

    pkg_base, pkg_dir = get_package_paths(package)
    if subdir:
        pkg_dir = os.path.join(pkg_dir, subdir)
    # Walk through all file in the given package, looking for data files.
    data_toc = TOC()
    for dir_path, dir_names, files in os.walk(pkg_dir):
        for f in files:
            extension = os.path.splitext(f)[1]
            if include_py_files or (extension not in PY_IGNORE_EXTENSIONS):
                source_file = os.path.join(dir_path, f)
                dest_folder = remove_prefix(dir_path, os.path.dirname(pkg_base) + os.sep)
                dest_file = os.path.join(dest_folder, f)
                data_toc.append((dest_file, source_file, 'DATA'))

    return data_toc

pkg_data = collect_pkg_data('ahk')
# -*- mode: python -*-

block_cipher = None

# pyinstaller --onefile --noconsole main.spec
a = Analysis(['script_launcher.py'],
             pathex=['C:\\Users\\Max\Documents\\GitHub\\client_jbp'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5','PyQt5.QtNetwork','PyQt5.QtMultimedia','PyQt5.QtCore','PyQt5.QtGui','PyQt5.QtWidgets','cv2', 'ahk'],
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
          pkg_data,
          [],
          name='script',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
