# RapidExtractor ReadMe

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

### Required File Structure on external drive

%DriveLetter%\
│
├── WPy64-31241\                 --> portable Python distribution
│ └── python-3.12.4.amd64\
│     └── python.exe
|     └── [...]
│
└── RapidExtractor\              --> RapidExtractor Tool
   ├── cases\
   ├── documents\
   ├── scripts\
   │    ├── main.py
   │    ├── dir_tree_extractor.py
   │    ├── prefetch_extractor.py
   │    ├── process_extractor.py
   │    ├── installed_programs_extractor.py
   │    ├── teamviewer_extractor.py
   │    ├── cbc_extractor.py
   │    ├── browser_history_extractor.py
   │    ├── gui.py
   │    └── *.py (other scripts)
   └─── start_RapidExtractor.bat

Other portable Python than WinPython can be used. Just don't forget to adapt the path to the portable interpreter in the code. 
Also make sure, that the executable is always run with administrative privileges.



### Usage

#### GUI Mode

1. Run `start_RapidExtractor.bat`.
2. Insert casename and device name then select modules to generate a batch file.
3. Attach external drive to target device and start the generated batch-file to automatically collect evidence.
