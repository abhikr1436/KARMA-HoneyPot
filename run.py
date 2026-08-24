"""
K.A.R.M.A Cloud SIEM Application Entry Point
Team: Abhijeet Kumar, Kanaka C, Raghunandan T V
Department of Computer Science & Engineering
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.launcher_gui import launch_gui

if __name__ == "__main__":
    print("================================================================")
    print("      K.A.R.M.A: AUTONOMOUS AI THREAT DECEPTION PLATFORM       ")
    print("================================================================")
    print("[+] Launching K.A.R.M.A Desktop Control Panel GUI...")
    print("================================================================")
    
    launch_gui()