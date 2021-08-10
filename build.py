import os

# import scripts
actual_path = os.getcwd()
scriptList = os.listdir(actual_path + '/scripts')
scriptList.remove('__init__.py')
if os.path.exists(actual_path + '/scripts/__pycache__'):
  scriptList.remove('__pycache__')
scriptList = [x[:-3] for x in scriptList]

for script in scriptList:
  module = __import__("scripts." + script)
  builder = getattr(module, script)
  builder.build(actual_path)
