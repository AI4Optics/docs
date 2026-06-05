# Landing a docstring-markup fix upstream

When step 4 of the sync finds Sphinx cross-reference roles (`:meth:`, `:class:`,
`:func:`, …) in the DeepLens docstrings, they will render as raw text in the API
pages because mkdocstrings expects plain Markdown. The source lives in a
**submodule**, so it cannot be edited from this docs repo — the fix has to land
**upstream in DeepLens**, then the submodule is bumped to that commit.

This is exactly how it was handled when the site was first built.

## The pattern

1. **Make the fix in DeepLens.** Replace Sphinx roles with backticks in the
   affected docstrings, e.g.:
   - `` :meth:`psf` `` → `` `psf` ``
   - `` :class:`~deeplens.geolens.GeoLens` `` → `` `GeoLens` ``

   Keep it docstring-only — no logic changes — so it's a safe, reviewable commit.

2. **Get it onto a public, durable ref.** A submodule pins a SHA, and that SHA
   must stay reachable, so land it on `dev`/`main` (or a tag), not a throwaway
   branch. Do it via a normal PR/merge when possible; a direct push to a shared
   branch bypasses review and may be blocked by safety tooling — if so, ask the
   user how they want it landed rather than forcing it.

   The original fix was prepared by cherry-picking the cleanup commit onto
   `origin/dev` in a throwaway worktree and pushing:

   ```bash
   # from a DeepLens checkout
   git fetch origin
   git worktree add --detach /tmp/dl-port origin/dev
   cd /tmp/dl-port
   git cherry-pick <cleanup-commit>     # docstring-only
   git push origin HEAD:dev             # or open a PR instead
   git -C <deeplens-checkout> worktree remove /tmp/dl-port --force
   ```

3. **Bump the submodule to the fixed commit** (back in this docs repo):

   ```bash
   git -C deeplens-src fetch origin
   git -C deeplens-src checkout <fixed-sha>
   ```

4. **Re-run the API check and continue the normal sync** (steps 3, 6, 7 of
   SKILL.md). Verify no leak on the live page:

   ```bash
   curl -s https://ai4optics.github.io/AI4Optics-docs/api/geolens/ \
     | grep -cE ':class:`~deeplens|:meth:`'   # expect 0
   ```

## If the user doesn't want to touch DeepLens right now

It's acceptable to ship with a few raw-markup spots — the build still succeeds,
it's only cosmetic. Note it in your summary so it isn't forgotten, and the fix
can be batched into a later DeepLens change.
