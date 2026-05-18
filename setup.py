import importlib.util
import os
import sys
import tempfile

if sys.version_info < (3, 9):
    print("You need at least Python 3.9 for this application!")
    if sys.version_info[0] < 3:
        print("try running with python3 {}".format(" ".join(sys.argv)))
    sys.exit(1)

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext as _build_ext
except ImportError:
    print("Could not find setuptools")
    print("Try installing them with pip install setuptools")
    sys.exit(1)


def _load_module(name, relpath):
    abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), relpath)
    spec = importlib.util.spec_from_file_location(name, abspath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ExtensionHelper = _load_module(
    "urh_build.ExtensionHelper", "src/urh/dev/native/ExtensionHelper.py"
)
COMPILER_DIRECTIVES = ExtensionHelper.COMPILER_DIRECTIVES

if sys.platform == "win32":
    OPEN_MP_FLAG = "/openmp"
    NO_NUMPY_WARNINGS_FLAG = ""
elif sys.platform == "darwin":
    OPEN_MP_FLAG = ""  # no OpenMP support in default Mac OSX compiler
    NO_NUMPY_WARNINGS_FLAG = "-Wno-#warnings"
else:
    OPEN_MP_FLAG = "-fopenmp"
    NO_NUMPY_WARNINGS_FLAG = "-Wno-cpp"

IS_RELEASE = os.path.isfile(os.path.join(tempfile.gettempdir(), "urh_releasing"))

try:
    from Cython.Build import cythonize
except ImportError:
    print(
        "You need Cython to build URH's extensions!\n"
        "You can get it e.g. with python3 -m pip install cython.",
        file=sys.stderr,
    )
    sys.exit(1)


def set_builtin(name, value):
    if isinstance(__builtins__, dict):
        __builtins__[name] = value
    else:
        # to support https://github.com/pypa/build
        # see https://github.com/jopohl/urh/issues/1106
        setattr(__builtins__, name, value)


class build_ext(_build_ext):
    def finalize_options(self):
        print("Finalizing options")
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        set_builtin("__NUMPY_SETUP__", False)
        import numpy

        self.include_dirs.append(numpy.get_include())


def get_extensions():
    filenames = [
        os.path.splitext(f)[0]
        for f in os.listdir("src/urh/cythonext")
        if f.endswith(".pyx")
    ]
    extensions = [
        Extension(
            "urh.cythonext." + f,
            ["src/urh/cythonext/" + f + ".pyx"],
            extra_compile_args=[OPEN_MP_FLAG],
            extra_link_args=[OPEN_MP_FLAG],
            language="c++",
        )
        for f in filenames
    ]

    ExtensionHelper.USE_RELATIVE_PATHS = True
    (
        device_extensions,
        device_extras,
    ) = ExtensionHelper.get_device_extensions_and_extras()
    extensions += device_extensions

    if NO_NUMPY_WARNINGS_FLAG:
        for extension in extensions:
            extension.extra_compile_args.append(NO_NUMPY_WARNINGS_FLAG)

    extensions = cythonize(
        extensions,
        compiler_directives=COMPILER_DIRECTIVES,
        compile_time_env=device_extras,
    )
    return extensions


extra_package_data = {}
if IS_RELEASE and sys.platform == "win32":
    extra_package_data["urh.dev.native.lib.shared"] = ["*.dll", "*.txt"]

setup(
    ext_modules=get_extensions(),
    cmdclass={"build_ext": build_ext},
    package_data=extra_package_data,
)
