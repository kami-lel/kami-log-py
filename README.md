# kami-log-py README 📝

## 🚀 Features

- Custom log message formatting with timestamp and padded log level names
- Padded log levels for consistent and neat alignment ("INFO ", "WARN ", etc.)
- Fully compatible with Python’s native `logging` module for seamless integration
- Ensures that each logger is configured only once to avoid duplicate handlers
- Lightweight, simple to integrate, and easily extensible













## 📜 Installation as Script

Copy the single script `./kamilog/kamilog.py` into your project folder.

Example directory structure:

```
your_project/
├── kamilog.py
└── main.py
```

In `main.py`, import the module as follows:

```python
import kamilog
```













## 📦 Installation as Module

Copy the entire `kamilog` folder into your project's source folder.

Example directory structure:

```
your_project/
├── project_abc/
│   ├── kamilog/
│   │   ├── __init__.py
│   │   └── kamilog.py
│   ├── module_a/
│   │   └── some_code.py
│   └── module_b/
│       └── other_code.py
└── setup.py
```

Then you can import `kamilog` anywhere within the project like this:

```python
from project_abc import kamilog
```













## Usage

```python
import logging
import kamilog

my_logger = kamilog.getLogger("myLogger")
my_logger.setLevel(logging.DEBUG)

my_logger.debug("Debugging details here")
my_logger.error("Error occurred!")
```