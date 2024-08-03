# RapidExtractor by prvtm8

## Overview

RapidExtractor is a modular tool for forensic analysis on Windows devices, designed to collect system and application data.

## Features

- Directory Tree Extraction
- Prefetch Data Extraction
- Process Extraction
- Installed Programs Extraction
- TeamViewer Log Extraction
- CBC Logfile Extraction
- Browser History Extraction (Chrome, Edge, Firefox)

## Dependencies

- tqdm (Install using `pip install tqdm`)

## Installation

### Required File Structure

%DriveLetter%\(ExternalDrive)
│
├── WPy64-31241/
│ └── python-3.12.4.amd64/
│ └── python.exe
│
├── RapidExtractor/
│   ├── scripts/
│   │   ├── main.py
│   │   ├── dir_tree_extractor.py
│   │   ├── prefetch_extractor.py
│   │   ├── process_extractor.py
│   │   ├── installed_programs_extractor.py
│   │   ├── teamviewer_extractor.py
│   │   ├── cbc_extractor.py
│   │   ├── browser_history_extractor.py
│   │   ├── gui.py
│   │   └── *.py (other script)
│   ├── start_RapidExtractor.bat
└── cases/

Other portable Python than WinPython can be used of course. Just don't forget to adapt the path to the portable interpreter in the code. 
Also make sure, that the executable is always run with administrative privileges.



#### Usage

#### GUI Mode

1. Run `start_RapidExtractor.bat`.
2. Select modules and generate the batch file with case and device names.
3. Double click on the generated batch-file when the external drive is attached to suspect device.
4. Wait for evidence to be collected.

#### Command Line Mode

```bash
python main.py "<selected_modules>" "<case_name>" "<device_name>"


This tool is provided as-is, without warranty. Use at your own risk.


