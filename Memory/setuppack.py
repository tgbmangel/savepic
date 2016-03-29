from distutils.core import setup
import py2exe

includes=[]
includes.append('psutil')
setup(windows=["MemorySpy.py"],
      options={"py2exe":{
          'includes':includes,
          'dll_excludes':['msvcr71.dll',"IPHLPAPI.DLL","NSI.dll","WINNSI.DLL","WTSAPI32.dll"]
          },}
      )
    
      
