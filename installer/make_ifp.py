from arch14cz_backend import (__version__)
import codecs
import sys
import os

ftemplate = "installer/arch14cz_installer.tpl"
fout = "installer/arch14cz_installer.ifp"
fdist = "dist/arch14cz"

args = sys.argv[1:]
if not len(args) == 1:
	raise Exception("Invalid number of arguments. Enter Arch14CZ_backend root path.")

root_path, = args

root_path = os.path.normpath(root_path)

extra_dirs = []

with open(ftemplate, "r", encoding = "utf-8-sig") as f:
	text = f.read()

files = []
dirs = []
for name in os.listdir(fdist):
	path = os.path.join(fdist, name)
	if os.path.isdir(path):
		dirs.append(path)
	else:
		files.append(path)
dirs += extra_dirs
dirs = sorted([os.path.normpath(os.path.abspath(path)) for path in dirs])
files = sorted([os.path.normpath(os.path.abspath(path)) for path in files])

filestext = ""
for path in dirs:
	filestext += "%s\nN/A\n[Folder]\n" % (path)
for path in files:
	size = os.stat(path).st_size
	units = "KB"
	size /= 1024
	if size > 1024:
		units = "MB"
		size /= 1024
	size = str(round(size, 1)).strip(".0")
	ext = os.path.splitext(path)[1][1:]
	filestext += "%s\n%s %s\n%s\n" % (path, size, units, ext)
filestext = filestext[:-1]

vars = dict(
	version = __version__,
	filename = "arch14cz_%s_setup.exe" % "_".join(__version__.split(".")),
	files = filestext,
	root_path = root_path,
)

text = text % vars

with open(fout, "w", encoding = "utf-8-sig") as f:
	f.write(text)
