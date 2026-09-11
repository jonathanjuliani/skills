# Installing the verification block

How `setup-skills` adds a short verification rule to a repository's agent instructions file. The text to install is the whole of [verification-block.md](verification-block.md), markers included, and nothing from this file.

It exists because the `verify-before-done` skill is model-invoked, and a completion gate needs to be in context at the moment a claim is written rather than waiting to be reached for. A repo's agent instructions file is read every turn without an invocation, so a short version of the rule lives there and the skill stays as the detail behind it.

## The one thing that must not go wrong

**You are adding to a file someone else owns.** Every heading, rule, and line already in that file must still be there when you are done. This step has exactly one destructive failure mode, which is rewriting the file instead of adding to it, so:

- **Read the target file in full before writing anything.**
- **Use a surgical edit.** Never write the file wholesale, and never reconstruct it from memory. If your tool for this is a whole-file write, read the current contents, and write them back with the block added.
- **After writing, confirm every heading that was there before is still there.** If anything is missing, restore it before reporting.

## Steps

1. **Pick the file.** `AGENTS.md` if it exists, otherwise `CLAUDE.md`. If both exist, ask which one the team treats as canonical. If neither exists, offer `AGENTS.md`, since it is the cross-tool convention and this plugin does not assume a vendor. Creating a file is the only case where there is no prior content to preserve.
2. **Look for the markers.** Search the target for `jon-skills:verification:begin`.
   - **Absent**: append the block at the end of the file, unless the file has an obvious conventions or workflow section it belongs in.
   - **Present, and the text between the markers matches [verification-block.md](verification-block.md)**: change nothing. Say it is already installed and stop. This is the normal outcome of a repeat run.
   - **Present, and the text differs**: someone has edited it, or the block has been updated. Show the difference and ask before replacing. Replace only what lies between the markers.
3. **Never write a second copy.** One pair of markers per file, always.
