# Git workflow

## Daily flow

1. **Start work:** create a branch off `main` for what you're doing.
   ```
   git checkout main
   git pull
   git checkout -b your-feature-name
   ```
2. **Work + commit** as you go.
   ```
   git add <files>
   git commit -m "short description of the change"
   ```
3. **Push your branch** and open a PR into `main` (don't push straight to `main`).
   ```
   git push -u origin your-feature-name
   ```
4. Once reviewed (or agreed verbally), merge the PR on GitHub, then locally:
   ```
   git checkout main
   git pull
   ```

## Before you start each session

```
git checkout main
git pull
```
This avoids working on stale code and reduces merge conflicts later.

## Rules of thumb

- One branch per feature/task, named for what it does (e.g. `dem-clipping`, `karst-buffer`).
- Small, frequent commits with clear messages > one giant commit.
- Never commit `.env` (your personal OneDrive path) — it's already gitignored. Each of us keeps our own.
- If `git pull` or merge reports a conflict, stop and sort it out together rather than force-pushing over it.
- Check `git status` before committing to make sure you're not accidentally adding data files.
