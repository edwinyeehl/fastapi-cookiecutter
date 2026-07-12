import os
import subprocess
import sys

def run_command(command, description):
    print(f"--> {description}...")
    try:
        # shell=True allows running uv natively from the user's path
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed during: {description}")
        print(e.stderr)
        return False

def main():
    if not run_command("uv sync", "Initializing environment and syncing dependencies via uv sync"):
        sys.exit(1)

    print("\n🎉 Project generated and environment bootstrapped successfully!")
    print("Next steps:")
    print(f"  cd {os.path.basename(os.getcwd())}")
    print("  uv run fastapi dev")

if __name__ == "__main__":
    main()