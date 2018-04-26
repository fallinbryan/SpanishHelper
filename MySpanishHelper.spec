# -*- mode: python -*-

block_cipher = None


a = Analysis(['mySpanishHelper.py'],
             pathex=['C:\\Users\\bfallin\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\pandas\\_libs\\tslibs', 'c:\\Users\\bfallin\\Documents\\codeprojects\\SpanishHelper'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# Add the following
def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path


dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)





exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mySpanishHelper',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mySpanishHelper')
