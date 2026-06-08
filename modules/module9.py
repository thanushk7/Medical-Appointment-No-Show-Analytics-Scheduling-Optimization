import webbrowser
from pathlib import Path

pdf = Path("powerbi_dashboard/Medical Appointment No-Show Analytics & Scheduling Optimization.pdf").resolve()

webbrowser.open(pdf.as_uri())