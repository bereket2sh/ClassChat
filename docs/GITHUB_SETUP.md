# GitHub Setup Instructions

## Creating a GitHub Repository for ClassChat

### Step 1: Create Repository on GitHub

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `ClassChat`
   - **Description**: `A TCP/IP-based online chat system for class communications`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /home/bereket/Desktop/ClassChat

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ClassChat.git

# Rename branch to main (optional, GitHub default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Example:
If your GitHub username is `johndoe`, the command would be:
```bash
git remote add origin https://github.com/johndoe/ClassChat.git
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files:
   - README.md
   - Makefile
   - src/server.py
   - src/client.py
   - docs/
   - etc.

## Alternative: Using SSH

If you prefer SSH authentication:

```bash
# Add remote using SSH
git remote add origin git@github.com:YOUR_USERNAME/ClassChat.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Future Commits

After the initial push, for future updates:

```bash
# Make your changes, then:
git add .
git commit -m "Your commit message describing changes"
git push
```

## Checking Remote Status

To verify your remote is configured:
```bash
git remote -v
```

Should show:
```
origin  https://github.com/YOUR_USERNAME/ClassChat.git (fetch)
origin  https://github.com/YOUR_USERNAME/ClassChat.git (push)
```

## Troubleshooting

### Issue: Authentication Failed
**Solution**: Use a Personal Access Token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use the token as your password when prompted

### Issue: Remote Already Exists
**Solution**: Remove and re-add the remote
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ClassChat.git
```

## What's in the Repository?

Your ClassChat repository contains:

```
ClassChat/
├── .gitignore                          # Python ignore patterns
├── Makefile                            # Build automation
├── README.md                           # Project overview
├── src/
│   ├── server.py                      # TCP server implementation
│   └── client.py                      # TCP client implementation
└── docs/
    ├── QUICK_START.md                 # Quick start guide
    ├── TASK1_TECHNICAL_REPORT.md     # Technical documentation
    └── GITHUB_SETUP.md                # This file
```

## Next Steps

1. ✅ Complete Task 1 (DONE)
2. ✅ Commit to local git (DONE)
3. 📤 Push to GitHub (FOLLOW STEPS ABOVE)
4. 🚀 Continue with Task 2, 3, 4...

---

**Note**: Remember to update your README.md with the actual GitHub repository URL once created!
