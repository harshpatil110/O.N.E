# GitHub SSH Key Setup

## Why SSH?
Nexus AI Innovations requires SSH-based authentication for all Git operations.
HTTPS-based cloning is disabled on our GitHub organization.

## Step 1: Generate an SSH Key
```bash
ssh-keygen -t ed25519 -C "your.name@nexusai.dev" -f ~/.ssh/nexusai_ed25519
```
When prompted for a passphrase, choose a strong one and store it in
your password manager.

## Step 2: Add to SSH Agent
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/nexusai_ed25519
```

## Step 3: Configure SSH for GitHub
Add to `~/.ssh/config`:
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/nexusai_ed25519
  AddKeysToAgent yes
```

## Step 4: Upload Public Key to GitHub
```bash
cat ~/.ssh/nexusai_ed25519.pub | pbcopy  # macOS
# Then paste into GitHub → Settings → SSH Keys → New SSH Key
```

## Step 5: Verify
```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

## Organization Access
After adding your key, request org access from
Harshvardhan Patil (harshvardhan@nexusai.dev).
You'll receive an invitation to the `nexusai` GitHub organization.

---
*DevOps — Nexus AI Innovations*
