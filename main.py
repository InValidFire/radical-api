import subprocess

script = "tracker_api/api.py"

while True:
    try:
        subprocess.run(f"python {script}", check=True)
    except subprocess.CalledProcessError as err:
        if err.returncode == -1:
            print("Stopping.")
            break
        if err.returncode == -2:
            print("Run update check!")