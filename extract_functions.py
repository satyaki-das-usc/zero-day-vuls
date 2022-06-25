import os
import shutil

from pycparser import c_ast, parse_file, c_generator


SRC_PATH = 'data/2015-10-27-openssl-v1-0-1e/just-functions'
DST_PATH = 'c_obfuscator/just-functions'
FAKE_LIBS_PATH = 'c_obfuscator/utils/fake_libc_include'

DENY_LIST = [
  '119-3300-c', '119-3400-c', '119-3500-c', '119-3600-c',
  '119-3700-c', '119-3800-c', '119-3900-c', '119-4000-c',
  '119-4100-c', '119-4200-c', '119-4300-c', '119-12600-c',
]


class ExtractFunctionsVisitor(c_ast.NodeVisitor):
  def __init__(self, filename):
      self.filename = filename
      self.typedefs = []
      self.idx = 0

  def visit_Typedef(self, node):
    self.typedefs.append((c_generator.CGenerator().visit(node)))

  def visit_FuncDef(self, node):
    self.test = True
    file_path = os.path.join(DST_PATH, f'{self.filename[:-2]}_{self.idx}.c')
    while os.path.exists(file_path):
        file_path = file_path[:-2] + '0.c'
    with open(file_path, 'w') as out_file:
        out_file.write(';\n'.join(self.typedefs))
        out_file.write(';\n')
        out_file.write(c_generator.CGenerator().visit(node))
    self.idx += 1


def main():
  try:
    os.mkdir(DST_PATH)

    print(SRC_PATH)

    for root, _, files in os.walk(SRC_PATH):
      # Skip all subdirectories listed in |DENY_LIST|.
      if any(dir in root for dir in DENY_LIST):
        continue

      # Builds list of paths to header directories to pass to the C preprocessor.
      # Usually contained in the 'shared' subdirectory of a given testcase.
      headers_argument_list = []
      if 'testcases' in root:
        headers_root = os.path.join(root.split("testcases", maxsplit=1)[0], 'testcases', 'shared')
        if os.path.isdir(headers_root):
          for dir in os.listdir(headers_root):
            headers_dir = os.path.join(headers_root, dir)
            headers_argument_list.append(f'-I{headers_dir}')

      for name in files:
        if not 'shared' in root and name.endswith('.c'):
            file_path = os.path.join(root, name)

            ast = parse_file(file_path, use_cpp=True, cpp_args=[*headers_argument_list, f'-I{FAKE_LIBS_PATH}'])
            
            visitor = ExtractFunctionsVisitor(name)
            visitor.visit(ast)
          
  except Exception as e:
    shutil.rmtree(DST_PATH)
    print(f"Error {e} occurred")


if __name__ == "__main__":
    main()
