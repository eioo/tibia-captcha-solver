# Tibia captcha solver

## Requirements

* **Python 3.6:** [32bit](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe) or [64bit](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)

* **Tesseract OCR:** [32bit](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20191030.exe) or [64bit](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20191030.exe) 

❗️ Install both before proceeding.

## Installation

1. Download and extract this project from [this link](https://github.com/eioo/tibia-captcha-solver/archive/master.zip).

2. Add following directories to your `PATH` environment variable:

    ```
    C:\Program Files\Tesseract-OCR
    C:\Python
    ```
    
    Python directory may be called `C:\Python36`, depending where you installed it.

    [Guide](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) on how to add environment variables.

    You can confirm that they work by going to command prompt and typing `tesseract -v` and `python --version`

3. Run `setup.bat` (only run once)

4. Run `start.bat` to run the solver
