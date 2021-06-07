import subprocess

def run(self, cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


# subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=True)

subprocess.run('bash -c "conda activate adq; python -V"', shell=True)
# fails