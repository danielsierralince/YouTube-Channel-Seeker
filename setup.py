from distutils.core import setup
import py2exe

setup(
    name="YouTube Channel Seeker.exe",
    version="1.0",
    description="YouTube Channel Seeker is a mini-proyect developed in Python, which implements a graphical interface (GUI) using PyQt5 library.",
    author="Daniel Sierra",
    author_email="danielsantiagosierralince@gmail.com",
    url="https://github.com/danielsierralince/YouTube-Channel-Seeker",
    license="none",
    scripts=["YouTube Channel Seeker.py"],
    console=["YouTube Channel Seeker.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None,
)