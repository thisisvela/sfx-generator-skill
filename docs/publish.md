# Publishing sfx-generator-skill on GitHub

The account is `thisisvela` (shown as **Vela**). The repository name is `sfx-generator-skill`, because every
install line, the plugin manifest and the site already use `https://github.com/thisisvela/sfx-generator-skill`
(held in one place in the code: `REPO` in `src/sfx_generator/__init__.py`). Nothing in this checkout carries
any other name: the licence, the manifests, the site, the docs and every commit are signed **Vela** with the
GitHub no-reply address `thisisvela@users.noreply.github.com`.

Everything below runs in a shell at the root of this checkout. Each step
says what to expect.

## 1. The GitHub account

1. Sign in at github.com as `thisisvela`. If the account does not exist yet, create it with that username;
   the profile **Name** field is what shows beside your username, set it to `Vela`.
2. Settings → Emails: tick **Keep my email addresses private** and **Block command line pushes that expose my
   email**. GitHub then shows your no-reply address. For an account created after 2017 it has the form
   `<id>+thisisvela@users.noreply.github.com`; the shorter `thisisvela@users.noreply.github.com` is also
   accepted and is the one this checkout uses. Either one links the commits to the account without showing a
   real address anywhere.
3. Settings → Profile: leave the real name, company and location empty if they are not meant to be public.

## 2. Authenticate the machine

Pick one. The GitHub CLI is the shortest road and is also what `gh repo create` needs below.

```bash
winget install GitHub.cli
```

```bash
gh auth login
```

Choose GitHub.com, HTTPS, and "Login with a web browser". Confirm with:

```bash
gh auth status
```

Without the CLI: create a fine-grained personal access token (Settings → Developer settings) with "Contents:
read and write" on the new repository, and paste it as the password when `git push` asks; Git for Windows
stores it in the Windows credential manager.

## 3. The local identity (already set in this checkout)

This checkout's own config (`.git/config`, not your global one) already says:

```bash
git config user.name
```

```bash
git config user.email
```

Expect `Vela` and `thisisvela@users.noreply.github.com`. The global config on this machine still has your
real name and address and is used by every other repository; to make the no-reply identity the default for
new work too:

```bash
git config --global user.name "Vela"
```

```bash
git config --global user.email "thisisvela@users.noreply.github.com"
```

The history was squashed to a single commit signed with that identity, so the history to be pushed names
nobody else and carries no earlier version of any file. Check with:

```bash
git log --format='%an <%ae> | %cn <%ce>' | sort -u
```

Expect one line.

The squash left a backup of the old history at `refs/original/refs/heads/main` (git keeps it on purpose). It
is not pushed by `git push origin main`, but delete it before anything like `git push --all` or `--mirror`:

```bash
git update-ref -d refs/original/refs/heads/main
```

```bash
git reflog expire --expire=now --all
```

```bash
git gc --prune=now
```

## 4. Create the remote repository (empty: no README, no licence, no .gitignore)

With the CLI, from the checkout:

```bash
gh repo create thisisvela/sfx-generator-skill --public --source . --remote origin --description "Sound effects made in code: deterministic numpy recipes, a CLI, a tuning page and a skill that turns a short description into a finished sound."
```

That creates the repository, adds it as `origin` and does not push yet.

On the website instead: New repository → Owner `thisisvela`, name `sfx-generator-skill`, Public, leave every
"initialize" box unticked, Create. Then:

```bash
git remote add origin https://github.com/thisisvela/sfx-generator-skill.git
```

## 5. Push

```bash
git branch -M main
```

```bash
git push -u origin main
```

Expect the one commit to upload and the branch to track `origin/main`. Then open
`https://github.com/thisisvela/sfx-generator-skill` and check: the licence badge says Apache-2.0, the README
renders, and the commit list shows **Vela** on every row.

## 6. The site (GitHub Pages)

Two workflows are committed in `.github/workflows/` and run on every push to `main`:

- `ci.yml` ("tests"): installs the package on Ubuntu with Python 3.10 and 3.12, runs `pytest -q`, then two
  `sfx make` acceptance runs. About five minutes. A red cross on the commit means a test failed on Linux;
  the log is under the Actions tab.
- `pages.yml` ("pages"): builds the site with `sfx site -o site`, checks every link, and deploys the folder to
  GitHub Pages. The deploy job fails until Pages is switched on, so do this once, right after the first push:
  Settings → Pages → Build and deployment → Source: **GitHub Actions**. Then re-run the failed "pages" run from
  the Actions tab (or push again). After that every push rebuilds and redeploys the site on its own.

The site appears at `https://thisisvela.github.io/sfx-generator-skill/` a minute after the deploy job goes
green; the address is also shown at the top of Settings → Pages and on the deploy job itself. It is fully
static: HTML, CSS, two scripts, the sounds as WAV, OGG and MP3, the presets, the spectrograms, the zips and
the narration clip, about 140 MB in all, every file served from the Pages host and nothing fetched from
anywhere else. Playback is Web Audio in the browser. The tuning page is not on the site; it is the local
`sfx tune` server only.

The `site/` folder is never committed (`/site/` is in `.gitignore`); the workflow builds it from the code,
so the published site is always the library as of the last push.

## 7. Search engines and sharing

The build already writes what search and answer engines look for: a canonical URL, Open Graph and Twitter
card tags on every page (the card image is `og.png`, the thunder spectrogram), JSON-LD on the home page
(SoftwareApplication) and the library page (an ItemList of 99 AudioObjects with their MP3 URLs, durations
and licence), `sitemap.xml`, `robots.txt`, a `404.html`, and `llms.txt` for AI crawlers. Two things need you:

1. **Google Search Console.** Open search.google.com/search-console, add a property of type "URL prefix"
   with `https://thisisvela.github.io/sfx-generator-skill/`, and pick the "HTML tag" method. It shows a
   tag like `<meta name="google-site-verification" content="abc123...">`. Copy only the `content` value,
   then in the repository: Settings → Secrets and variables → Actions → Variables → New repository
   variable, name `SFX_SITE_VERIFICATION`, value that string. Push anything (or re-run the pages workflow)
   so the tag is built in, then press Verify in Search Console. Finally Sitemaps → add `sitemap.xml`.
   Indexing follows within days; the Performance report shows queries and clicks after that.
2. **Bing Webmaster Tools** can import the verified property from Search Console in one click, which also
   covers DuckDuckGo and the answer engines that use Bing's index.

**Analytics** (optional): GitHub has none for Pages. The builder takes a Google Analytics Measurement ID from
the repository variable `SFX_GA_ID` (`G-XXXXXXXXXX`) the same way and adds the Google tag to every page; with
the variable unset the site loads nothing external. Set it under Settings → Secrets and variables → Actions →
Variables, then run the pages workflow.

Check a shared link's preview card with any social preview checker, or by pasting the URL into a chat
app; the image and description come from the tags above.

## 8. After the first push

- Repository Settings → General: tick "Discussions" or "Issues" as you like; untick "Wikis".
- Add topics: `sound-effects`, `procedural-audio`, `numpy`, `claude-code`, `codex`, `skill`.
- The plugin install line in the README works as soon as the repository is public:
  `/plugin install sfx-generator --marketplace thisisvela/sfx-generator-skill`.
- A release is not needed for installs (they use `git+https://...`), but a tag marks the first public version:

```bash
git tag -a v0.1.0 -m "first public version"
```

```bash
git push origin v0.1.0
```

## If something goes wrong

- `remote: Permission denied` or a login prompt loop: `gh auth status`, or re-create the token with
  Contents read/write on this repository.
- `! [rejected] main -> main (fetch first)`: the remote was created with a README or licence. Delete and
  re-create it empty, or `git pull --rebase origin main` once and push again.
- `remote: error: GH007: Your push would publish a private email address`: a commit still carries the real
  address; run the identity check in step 3.
