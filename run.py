"""YT Auto - Run Script

This script runs the YT Auto Streamlit application.
"""

import subprocess
import sys


def main():
    """Run the Streamlit application."""
    print("Starting YT Auto - YouTube Content Intelligence Platform...")
    print("=" * 60)
    
    try:
        # Run streamlit
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            cwd="/workspace",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
