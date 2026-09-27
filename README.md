# Face Age Studio

A lightweight Streamlit app that returns a bundled reference photo for each
effect. It does not generate an aged or younger version of the uploaded
portrait.

## Requirements

- Python 3.9 or newer
- One original portrait image
- Bundled `old uncle photo .jpeg` and `teenage boy  photo.jpeg` reference images

## Setup

### Windows PowerShell

```bash
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Windows Command Prompt

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
python -m streamlit run face_aging_app.py
```

Keep both bundled reference JPEGs beside `face_aging_app.py`. Upload an original
portrait, choose **Age Face** or **De-Age Face**, and select **Show result**.
**Age Face** returns `old uncle photo .jpeg`; **De-Age Face** returns
`teenage boy  photo.jpeg`. The chosen photo is displayed and can be downloaded
as a PNG. On small screens, the original and result stack vertically. The
original portrait is shown for reference but is not transformed.

To open the app on a phone connected to the same Wi-Fi, run:

```bash
python -m streamlit run face_aging_app.py --server.address 0.0.0.0
```

Then open the computer's local network address on the phone, using port `8501`.
Allow Python through Windows Defender Firewall on private networks if prompted.
