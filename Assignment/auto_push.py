import subprocess
import datetime

def git_auto_push(commit_message=None):
    """
    Automates staging, committing, and pushing current changes to Git repository.
    """
    if not commit_message:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-commit assignment update at {timestamp}"
        
    try:
        print("1. Staging files (git add)...")
        subprocess.run(["git", "add", "."], check=True)
        
        print(f"2. Committing changes: '{commit_message}'...")
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            print("No changes detected to commit.")
            return
            
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        print("3. Pushing to remote repository (git push)...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("\nSuccess! Files pushed to Git successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError executing Git command: {e}")

if __name__ == "__main__":
    git_auto_push()
