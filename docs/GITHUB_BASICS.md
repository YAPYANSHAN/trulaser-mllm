# GitHub basics for this project

This page explains the pieces of a GitHub repository you will touch in this project, in plain words. Each section says what the thing is, why it exists, and how to change it.

## The big picture

- **Git** is a program on your computer that remembers every saved version of your project folder. You can always go back to an old version.
- **GitHub** is a website that stores a copy of that history online, so it is backed up, you can share it, and your supervisor can look at it.
- A **repository** (or "repo") is one project folder plus its full history. This one is `YAPYANSHAN/trulaser-mllm`.

Nothing is ever really lost. Even the old `pipeline/` code that was deleted is still in the history and can be brought back.

## The words you will meet

| Word | Plain meaning |
|---|---|
| **Clone** | Download a repository to your computer for the first time. |
| **Commit** | Save a snapshot of your changes with a short message saying what you did, like a save point in a game. |
| **Push** | Upload your commits from your computer to GitHub. |
| **Pull** | Download commits from GitHub that you don't have yet. |
| **Branch** | A separate line of work. `main` is the official version; you can try things on another branch without touching `main`. |
| **Pull request (PR)** | A request on GitHub to merge one branch into `main`. It shows exactly what changed, so you (or your supervisor) can review it first. |
| **Merge** | Accept the pull request, so its changes become part of `main`. |

## README.md

**What it is.** The front page of the repository. GitHub shows it automatically below the file list. Every folder can have its own README too, such as [`datasets/README.md`](../datasets/README.md).

**Why it matters.** It is the first thing your supervisor or examiner reads. It should answer: what is this project, what is in each folder, and how do I run it.

**How to write it.** It is written in **Markdown**, a simple way to format plain text:

```markdown
# Big heading
## Smaller heading
Normal text. **Bold**, *italic*, `code`.
- a bullet point
1. a numbered step
[link text](https://example.com)
| Column A | Column B |
|---|---|
| a table | row |
```

You can edit a README directly on GitHub: open the file, click the pencil icon, change it, and press **Commit changes**. The **Preview** tab shows how it will look.

**Keep it up to date.** When you add a folder or a script, add one line to the README saying what it is.

## .gitignore

**What it is.** A plain text file listing files and folders that git should **not** track or upload. It lives in the top folder of the repo. The dot at the start of the name is normal; it makes the file hidden on some systems.

**Why it matters here.** This repo is public. Real company data, paper PDFs, and large files your code creates must stay on your computer only. If a file matches a pattern in `.gitignore`, git simply pretends it isn't there.

**How the patterns work** (open [`.gitignore`](../.gitignore) to see them with comments):

| Pattern | Means |
|---|---|
| `data/` | Ignore the whole `data` folder, wherever it is. |
| `*.pdf` | Ignore every file ending in `.pdf`. |
| `!datasets/documents/*.pdf` | Exception: do track PDFs in `datasets/documents/`. |
| `# text` | A comment, ignored by git. |

**How to change it.** Add a new line with a pattern, save, and commit. For example, if you start saving trained models as `.pkl` files, add a line `*.pkl`.

**One catch.** `.gitignore` only affects files git isn't tracking yet. If you already committed a file, adding it to `.gitignore` later won't remove it from GitHub. Ask before committing anything you're unsure about.

## Other files you may see later

| File | What it is for |
|---|---|
| `requirements.txt` | A list of the Python packages the code needs, so anyone can install them with `pip install -r requirements.txt`. |
| `LICENSE` | Says what others may do with your code. Ask your supervisor whether you need one. |
| `.github/` | Settings for GitHub itself, such as automatic tests. Not needed yet. |

## Getting the repo on your Windows computer

The easiest way for a beginner is **GitHub Desktop**, a free app with buttons instead of commands.

1. Install GitHub Desktop from desktop.github.com and sign in with your GitHub account.
2. Click **File → Clone repository**, pick `YAPYANSHAN/trulaser-mllm`, and choose a folder such as `Documents\GitHub`.
3. Open the folder in VS Code or File Explorer and work as normal.

## Your everyday routine

1. **Pull first.** In GitHub Desktop press **Fetch origin**, then **Pull**, so you have the latest version.
2. **Work.** Edit files, write code, add notebooks.
3. **Commit.** GitHub Desktop lists every changed file on the left. Tick the ones you want, write a short summary such as `Clean job log dates`, and press **Commit to main** (or to your branch).
4. **Push.** Press **Push origin** to upload.

Commit small and often, with messages that say what you did. "Add photo loader" is better than "update".

The same steps on the command line (Anaconda Prompt or Git Bash), if you prefer:

```bash
git pull                       # get the latest
git status                     # see what changed
git add datasets/README.md     # pick a file to save (or: git add .  for all)
git commit -m "Explain columns" # save a snapshot with a message
git push                       # upload
```

## Branches and pull requests

When you try something bigger, work on a branch so `main` stays clean:

1. In GitHub Desktop: **Current branch → New branch**, name it after the task, such as `explore-data`.
2. Commit and push as usual.
3. Click **Create Pull Request**. GitHub opens a page showing every change.
4. Check it, then press **Merge pull request**. Your work is now on `main`.

When I make changes for you, I do the same: I put them on a branch and open a pull request, and you decide whether to merge it.

## If something goes wrong

- **"Your branch is behind"**: press Pull first, then Push.
- **Merge conflict**: two versions changed the same line. GitHub Desktop shows both; keep the one you want and commit. Ask me if unsure.
- **Committed the wrong file**: don't panic. Tell me which file and I'll help remove it. If it was real company data, say so straight away, because public history needs extra cleaning.
