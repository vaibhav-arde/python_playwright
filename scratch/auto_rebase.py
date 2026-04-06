import subprocess
import os

def run_cmd(cmd):
    # Use powershell for commands that need env vars
    return subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)

print("Starting rebase automation...")
for i in range(50): # Limit to 50 iterations to be safe
    print(f"Iteration {i}...")
    # Try to continue
    res = run_cmd("$env:GIT_EDITOR='true'; git rebase --continue")
    
    if res.returncode == 0:
        print("Rebase finished successfully!")
        print(res.stdout)
        break
    
    # Check for conflicts
    status = run_cmd("git status")
    print(status.stdout)
    
    if "Unmerged paths:" in status.stdout:
        print("Resolving conflicts in core files...")
        # Resolve core files with --ours
        run_cmd("git checkout --ours pages/*.py utils/*.py pytest.ini")
        # Add all
        run_cmd("git add .")
    else:
        # If there are no unmerged paths but it failed, it might be an empty commit or message issue
        print("No unmerged paths but rebase failed. Trying to skip or continue...")
        if "No changes - did you forget to use 'git add'?" in res.stderr or "No changes - did you forget to use 'git add'?" in res.stdout:
             run_cmd("git rebase --skip")
        else:
             # Just try to continue
             pass

print("Done.")
