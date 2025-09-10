# kami-log-py README 📝

## 🚀 Features

- Custom log message formatting with timestamp and padded level names
- Padded log levels for neat alignment ("INFO ", "WARN ", etc.)
- Compatible with Python’s native `logging` module for seamless integration
- Lightweight and simple integration













## 📦 Installation

Copy the single script `kamilog.py` into your current project folder.

Example directory structure:

```
your_project/
├── kamilog.py
└── main.py
```













## 🛠 Usage

In your `main.py` script:

```python
import logging
import kamilog

my_logger = kamilog.getLogger("myLogger")

my_logger.setLevel(logging.DEBUG)

my_logger.debug("Debugging details here")
my_logger.error("Error occurred!")
```