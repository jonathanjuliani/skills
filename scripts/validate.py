#!/usr/bin/env python3
"""Structural checks for the jon-skills plugin. Run before committing.

Catches what silently breaks a skill pack: frontmatter that is not valid YAML
(an unquoted colon in a description is the recurring one), a name that does not
match its folder, a missing cross-tool manifest, a skill on disk that nobody
registered, a cross-reference to a skill that does not exist, and a relative
link to a reference file that has been renamed or removed.

Pass --links to also resolve external URLs. That is off by default because it
needs the network and can flake; the rest of the run is offline and fast.
"""
import json, pathlib, re, sys

try:
    import yaml
except ImportError:
    yaml = None  # degraded mode, reported at the end

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Skills that ship with a harness rather than with this pack. Referencing one is
# allowed only where the text says whose it is, which the check below enforces:
# the repo is installable standalone and must not imply a dependency it has not
# declared. Anything else belongs in README's "Optional companions", named with
# its source, never as a bare /slash reference.
HARNESS_BUILTINS = {"code-review", "simplify", "run", "dataviz", "security-review"}
errors, skills = [], {}

for f in sorted(ROOT.glob("skills/*/*/SKILL.md")):
    rel = f.relative_to(ROOT)
    text = f.read_text()
    if not text.startswith("---\n"):
        errors.append(f"{rel}: no frontmatter"); continue
    block = text.split("---\n", 2)[1]
    if yaml is None:
        # Without a YAML parser, check the one failure that actually recurs here:
        # an unquoted colon in a value, which silently turns it into a mapping.
        fm = {}
        for raw in block.splitlines():
            if not raw or raw.startswith((" ", "\t", "#")):
                continue
            key, sep, value = raw.partition(":")
            if not sep:
                continue
            value = value.strip()
            if ": " in value and value[:1] not in "\"'>|":
                errors.append(f"{rel}: frontmatter value for '{key}' contains an unquoted ':', "
                              f"which is not valid YAML. Quote it or reword.")
            fm[key.strip()] = value
    else:
        try:
            fm = yaml.safe_load(block)
        except yaml.YAMLError as e:
            line = str(e).split("\n")[-2].strip() if "\n" in str(e) else e
            errors.append(f"{rel}: frontmatter is not valid YAML. An unquoted ':' in "
                          f"description is the usual cause. {line}")
            continue
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"{rel}: missing '{key}'")
    if fm.get("name") != f.parent.name:
        errors.append(f"{rel}: name '{fm.get('name')}' does not match folder '{f.parent.name}'")
    if not (f.parent / "agents" / "openai.yaml").exists():
        errors.append(f"{rel}: missing agents/openai.yaml")
    if "—" in text:
        errors.append(f"{rel}: contains an em-dash, which the authoring conventions ban")
    if "## When this does not apply" not in text:
        errors.append(f"{rel}: missing the 'When this does not apply' guardrail")
    if fm.get("name"):
        skills[fm["name"]] = text

for name, text in skills.items():
    for ref in re.findall(r'call the Skill tool with "([^"]+)"', text, re.IGNORECASE):
        if ref not in skills:
            errors.append(f"{name}: calls '{ref}', which is not a skill in this pack. "
                          f"The Skill tool cannot reach another plugin's skill.")

# No silent external dependency. A bare `/name` for something this pack does not
# ship reads as though the reader has it, which breaks the moment they do not.
for f in sorted([*ROOT.glob("skills/**/*.md"), *ROOT.glob("docs/**/*.md"), ROOT / "README.md"]):
    rel, text = f.relative_to(ROOT), f.read_text()
    for i, line in enumerate(text.splitlines(), 1):
        # With a slash it reads as invocable; without one it still reads as ours.
        # Bare names are only checked against known-external ones, since an
        # unrestricted check would fire on every npm package and CSS token.
        refs = re.findall(r"`/([a-z][a-z0-9-]+)`", line)
        refs += [m for m in re.findall(r"`([a-z][a-z0-9-]+)`", line)
                 if m in HARNESS_BUILTINS and m not in skills]
        for ref in refs:
            if ref in skills or ref == "setup-skills":
                continue
            if ref in HARNESS_BUILTINS and re.search(r"Claude Code|harness|ships", line):
                continue
            errors.append(f"{rel}:{i}: `/{ref}` is not in this pack. Say whose it is on the "
                          f"same line, or list it under README's Optional companions.")

# Relative links: a renamed reference file breaks these with no other symptom.
LINK = re.compile(r"\[[^\]]*\]\((?!https?://|#)([^)]+)\)")
for f in sorted([*ROOT.glob("skills/**/*.md"), *ROOT.glob("docs/**/*.md"), ROOT / "README.md"]):
    rel = f.relative_to(ROOT)
    for target in LINK.findall(f.read_text()):
        path = (f.parent / target.split("#")[0]).resolve()
        if not path.exists():
            errors.append(f"{rel}: link to '{target}' does not resolve")

# Markdown style. The repo is already uniform on every axis below, so these
# lock it in rather than fixing anything. A formatter was measured against this
# repo and rejected: it churned 384 lines for no consistency gain, and without
# the frontmatter plugin it collapses every SKILL.md's frontmatter into a heading.
for f in sorted([*ROOT.glob("skills/**/*.md"), *ROOT.glob("docs/**/*.md"),
                 ROOT / "README.md", ROOT / "CONTEXT.md", ROOT / ".agents/conventions.md"]):
    rel, text = f.relative_to(ROOT), f.read_text()
    fenced = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            if not fenced and line.strip() == "```":
                errors.append(f"{rel}:{i}: opening code fence has no language (use ```text if none fits)")
            fenced = not fenced
            continue
        if fenced:
            continue
        # Inline code is quoted material, so a rule may name the syntax it bans.
        line = re.sub(r"`[^`]*`", "``", line)
        if re.match(r"^\s*[*+] ", line):
            errors.append(f"{rel}:{i}: list marker is '{line.lstrip()[0]}', this repo uses '-'")
        if re.search(r"(?<!_)__(?!_)\S", line):
            errors.append(f"{rel}:{i}: strong emphasis uses '__', this repo uses '**'")
        if line.startswith("|") and line.count("|") > 2 and not line.startswith("| "):
            errors.append(f"{rel}:{i}: table row needs a space after the leading pipe")
    if "\n\n\n\n" in text:
        errors.append(f"{rel}: three or more consecutive blank lines")

# Hygiene, cheap and keeps diffs from carrying noise.
for f in sorted([*ROOT.glob("skills/**/*"), *ROOT.glob("docs/**/*"), ROOT / "README.md",
                 ROOT / "CONTEXT.md", ROOT / ".agents/conventions.md"]):
    if not f.is_file() or f.suffix not in {".md", ".yaml", ".yml"}:
        continue
    rel, text = f.relative_to(ROOT), f.read_text()
    if text and not text.endswith("\n"):
        errors.append(f"{rel}: no newline at end of file")
    for i, line in enumerate(text.splitlines(), 1):
        if line != line.rstrip():
            errors.append(f"{rel}:{i}: trailing whitespace")
            break

on_disk = {str(p.parent.relative_to(ROOT)) for p in ROOT.glob("skills/*/*/SKILL.md")}

# Harness manifests. They drift the moment one is edited alone, so the shared
# fields are compared rather than trusted. Claude Code and Cursor list every
# leaf path because their plugin loaders do not recurse into bucket folders.
# Codex walks ./skills/ itself.
MANIFESTS = {
    ".claude-plugin/plugin.json": "list",
    ".cursor-plugin/plugin.json": "list",
    ".codex-plugin/plugin.json": "dir",
}
loaded = {}
for path, kind in MANIFESTS.items():
    p = ROOT / path
    if not p.exists():
        errors.append(f"{path}: missing harness manifest"); continue
    try:
        loaded[path] = json.loads(p.read_text())
    except Exception as e:
        errors.append(f"{path}: {e}"); continue
    if kind == "dir":
        target = loaded[path].get("skills")
        if target != "./skills/":
            errors.append(f"{path}: 'skills' should be './skills/', found {target!r}")
        elif not (ROOT / "skills").is_dir():
            errors.append(f"{path}: 'skills' points at a directory that does not exist")
    elif kind == "list":
        listed = loaded[path].get("skills")
        if not isinstance(listed, list):
            errors.append(f"{path}: 'skills' should be a list of leaf paths, found {listed!r}")
        else:
            names = {r.lstrip("./") for r in listed}
            for missing in sorted(on_disk - names):
                errors.append(f"{path}: {missing} on disk but not registered")
            for stale in sorted(names - on_disk):
                errors.append(f"{path}: {stale} registered but not on disk")

try:
    json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
except Exception as e:
    errors.append(f".claude-plugin/marketplace.json: {e}")

try:
    mkt = json.loads((ROOT / ".cursor-plugin/marketplace.json").read_text())
    plugins = mkt.get("plugins") or []
    if not plugins:
        errors.append(".cursor-plugin/marketplace.json: no plugins listed")
    else:
        entry = plugins[0]
        for banned in ("keywords", "category", "tags"):
            if banned in entry:
                errors.append(f".cursor-plugin/marketplace.json: '{banned}' belongs on plugin.json, not the marketplace entry")
        expected_name = loaded.get(".cursor-plugin/plugin.json", {}).get("name")
        if expected_name and entry.get("name") != expected_name:
            errors.append(f".cursor-plugin/marketplace.json: plugin name {entry.get('name')!r} does not match plugin.json {expected_name!r}")
        if entry.get("source") not in ("./", "."):
            errors.append(f".cursor-plugin/marketplace.json: source should be './', found {entry.get('source')!r}")
except FileNotFoundError:
    errors.append(".cursor-plugin/marketplace.json: missing")
except Exception as e:
    errors.append(f".cursor-plugin/marketplace.json: {e}")

if len(loaded) > 1:
    ref_path, ref = next(iter(loaded.items()))
    for field in ("name", "version", "license", "homepage", "repository"):
        values = {p: m.get(field) for p, m in loaded.items()}
        if len(set(values.values())) > 1:
            errors.append(f"manifests disagree on '{field}': {values}")

gem = ROOT / "gemini-extension.json"
if not gem.exists():
    errors.append("gemini-extension.json: missing harness manifest")
else:
    try:
        ctx = json.loads(gem.read_text()).get("contextFileName")
        if not ctx:
            errors.append("gemini-extension.json: no contextFileName")
        elif not (ROOT / ctx).exists():
            errors.append(f"gemini-extension.json: contextFileName '{ctx}' does not exist")
    except Exception as e:
        errors.append(f"gemini-extension.json: {e}")

for required in ("AGENTS.md",):
    if not (ROOT / required).exists():
        errors.append(f"{required}: missing")

if "--links" in sys.argv:
    import urllib.request, urllib.error
    # URLs inside a code fence are illustrative, and RFC 2606 reserves the
    # example domains for exactly that, so neither is a link to resolve.
    RESERVED = ("example.com", "example.org", "example.net", "localhost")
    urls = set()
    for f in [*ROOT.glob("**/*.md")]:
        if ".git" in f.parts: continue
        fenced = False
        for line in f.read_text().splitlines():
            if line.startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for u in re.findall(r"https://[^\s)\]]+", line):
                if not any(d in u for d in RESERVED):
                    urls.add(u)
    for url in sorted(urls):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "jon-skills-validate"})
            urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as e:
            if e.code not in (403, 405):  # some hosts refuse HEAD or bots
                errors.append(f"dead link: {url} ({e.code})")
        except Exception as e:
            errors.append(f"unreachable link: {url} ({type(e).__name__})")

if yaml is None:
    print("WARNING: pyyaml not found, so frontmatter is only partially checked.")
    print(f"  This interpreter is {sys.executable}. On macOS the system python3 cannot")
    print("  pip install; use a different interpreter, a venv, or pipx.")
    print("  CI runs the full check either way.\n")

if errors:
    print(f"FAIL ({len(errors)})")
    for e in errors: print("  -", e)
    sys.exit(1)
print(f"OK: {len(skills)} skills")
