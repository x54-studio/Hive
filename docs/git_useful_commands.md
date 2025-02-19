**Git Useful Commands with Examples**

### **1. Initialize a New Repository**
```bash
git init
```
Initializes a new Git repository in the current directory.

### **2. Clone a Remote Repository**
```bash
git clone <repository_url>
```
Copies a remote repository to your local machine.

### **3. Check Repository Status**
```bash
git status
```
Displays the status of the working directory (staged, unstaged, untracked files).

### **4. Add Files to Staging Area**
```bash
git add <file>
git add .
```
Stages files for commit. Use `.` to add all changes.

### **5. Commit Changes**
```bash
git commit -m "Commit message"
```
Saves staged changes with a descriptive message.

### **6. Push Changes to Remote Repository**
```bash
git push origin <branch_name>
```
Uploads local commits to a remote branch.

### **7. Pull Latest Changes**
```bash
git pull origin <branch_name>
```
Fetches and merges changes from a remote branch into the current branch.

### **8. View Commit History**
```bash
git log
git log --oneline
```
Shows the commit history. `--oneline` displays a compact view.

### **9. View Differences Between Commits**
```bash
git diff
```
Shows changes between the working directory and the last commit.

### **10. Create a New Branch**
```bash
git branch <branch_name>
```
Creates a new branch.

### **11. Switch to Another Branch**
```bash
git checkout <branch_name>
```
or (modern approach)
```bash
git switch <branch_name>
```
Moves to a different branch.

### **12. Create and Switch to a New Branch**
```bash
git checkout -b <branch_name>
```
or
```bash
git switch -c <branch_name>
```
Creates a new branch and switches to it.

### **13. Merge Branches**
```bash
git merge <branch_name>
```
Merges another branch into the current branch.

### **14. Delete a Branch Locally**
```bash
git branch -d <branch_name>
```
For force deletion:
```bash
git branch -D <branch_name>
```

### **15. Delete a Remote Branch**
```bash
git push origin --delete <branch_name>
```
Removes a branch from the remote repository.

### **16. Reset Changes (Undo)**
```bash
git reset --hard <commit_hash>
```
Resets to a previous commit, discarding all changes.

### **17. View Remote Repositories**
```bash
git remote -v
```
Displays remote repositories linked to the local repository.

### **18. Change Remote Repository URL**
```bash
git remote set-url origin <new_repository_url>
```
Updates the remote repository URL.

### **19. Stash Temporary Changes**
```bash
git stash
```
Saves local changes temporarily without committing.
To retrieve stashed changes:
```bash
git stash pop
```

### **20. Remove Untracked Files**
```bash
git clean -f
```
Deletes untracked files.
To remove untracked directories as well:
```bash
git clean -fd
```

### **21. View Who Made Changes to a File**
```bash
git blame <file>
```
Shows who last modified each line in a file.

---

### **More Useful Git Commands**

### **22. Revert a Specific Commit**
```bash
git revert <commit_hash>
```
Creates a new commit that undoes the changes from a specific commit.

### **23. Rebase a Branch**
```bash
git rebase <branch_name>
```
Reapplies commits from one branch onto another, creating a cleaner history.

### **24. Force Push (Use with Caution)**
```bash
git push --force
```
Overwrites remote changes with local changes.

### **25. Show Last Commit**
```bash
git show HEAD
```
Displays details of the most recent commit.

### **26. List All Local & Remote Branches**
```bash
git branch -a
```
Lists all branches, both local and remote.

### **27. Check the Current Working Directory**
```bash
git rev-parse --show-toplevel
```
Displays the root directory of the repository.

### **28. Check if a Directory Is a Git Repository**
```bash
git rev-parse --is-inside-work-tree
```
Outputs `true` if inside a Git repository.

### **29. Check for Corruption**
```bash
git fsck
```
Checks the integrity of the repository.

### **30. Garbage Collection**
```bash
git gc
```
Cleans up unnecessary files and optimizes the repository.

### **31. Check Git Version**
```bash
git --version
```
Displays the installed Git version.
