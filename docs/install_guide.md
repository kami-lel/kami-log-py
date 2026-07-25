# kamilog Installation Guide

## Package Install

install via `pip`. This also registers the `kamilog` shell command (`console_scripts` entry point) automatically.

#### Clone and Install

```bash
git clone https://github.com/kami-lel/kamilog.git
cd kamilog
pip install .
```

#### Install Directly from Github

```bash
pip install git+https://github.com/kami-lel/kamilog.git
```

## Copy Install

embed kamilog directly into your project — no `pip` required.

#### Copy Single Script

copy the single file into your project root:

```
your_project/
├── kamilog.py
└── main.py
```

#### Copy Entire Module

copy the entire folder into your project's source directory:

```
your_project/
├── project_abc/
│   ├── kamilog/
│   │   ├── __init__.py
│   │   └── kamilog.py
│   ├── module_a/
│   └── module_b/
└── pyproject.toml
```
