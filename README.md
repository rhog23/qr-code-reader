# QRCodeReader

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Table of Contents

- [QRCodeReader](#qrcodereader)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Getting Started](#getting-started)
    - [Requirements](#requirements)
  - [Usage](#usage)
  - [Roadmap](#roadmap)
  - [License](#license)

## About

QRCodeReader is a GUI program that supports creating QR codes and reading QR codes from image file or camera (computer webcam/external camera module) using Python and Tkinter.

## Getting Started

### Requirements

Only Python 3.11+ is tested and guaranteed to work.

To run the program, the following Python libraries are needed. To install the Python library with `pip`,

```python
pip install opencv-python
pip install qrcode
pip install pillow
pip install pyzbar
```

> Latest versions of the Python libraries _(as of 10 Aug 2023)_ are used in the program.

Alternatively, users can install the required libraries using `pip` and the `requirements.txt` file using the following command:

```python
pip install -r requirements.txt
```

## Usage

## Roadmap

- [ ] Add more error handling functions.
- [ ] Handle external camera module taking a long time to start issue.
- [ ] Save generated QR codes under `images` directory.

## License

Distributed under the MIT License. See `LICENSE` for more information.
