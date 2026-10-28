# Maintaining this profile

The README is a native GitHub profile: six linked SVG cards, a complete repository index, a small toolkit, metadata-based activity, and verified public contact links. All graphics live in this repository; there are no third-party statistics widgets, fonts, scripts, or tracking images.

## Automatic updates

`.github/workflows/update-profile.yml` runs every Monday at 03:23 UTC (08:53 India time), on manual dispatch, and when its scripts/tests/workflow change on main. The Python 3.12 script has no third-party dependencies. It follows repository pages until an empty response, verifies the total against the public profile count, includes forks and archived repositories, and updates only the `REPOSITORIES` and `ACTIVITY` marker pairs. The profile itself is indexed but excluded from project activity. No change means no commit.

New repositories appear under **Experiments / Newly discovered**, with their public description and primary language. Missing descriptions are explicitly labelled. Review a new repository before adding its code-based description, category and stack to `scripts/curated.json`. This intentionally avoids inventing claims from repository names. Featured cards and toolkit remain editorially maintained.

Run locally:

```sh
python -m unittest discover -s tests -v
python scripts/update_repositories.py
python scripts/update_repositories.py --check
```

Use `GH_TOKEN` or `GITHUB_TOKEN` for authenticated API access. A token is never written to the README. `--snapshot path.json` permits reproducible offline validation with an audited API repository list.

## GitHub settings and limitations

Enable Actions for this repository. The workflow requests only `contents: write` for its refresh job; the default is `contents: read`. The automatically supplied `github.token` is sufficient; no personal access token or additional secret is required. Repository/organization policies and branch protection can still prevent the bot from pushing. If direct pushes are prohibited, adapt the final step to the repository's approved pull-request process. Scheduled workflows can be delayed and GitHub may disable schedules in inactive public repositories; manual dispatch remains useful.

The public API is rate limited. Failed requests, incomplete counts and malformed markers fail before any README write. A repository created/deleted during pagination can cause a safe failure; retry the workflow. Public data only is shown. Primary-language counts are repository counts, not code volume or proficiency. Last push is a project push date, not a contribution or commit count.

## Artwork and motion

`assets/hero.svg` uses a geometric wireframe, a slow vertical drift, a travelling stroke and a softly breathing central node. The footer repeats the travelling stroke. CSS keyframes stay inside standalone SVG images; no JavaScript or foreignObject is used. Every image has a viewBox, accessible title and README alt text. Text is visible in the initial frame. Cards are static for reading comfort. The palette is self-contained, so assets remain legible on both GitHub themes.

The hero has a dedicated static mobile layout and a static source selected by `prefers-reduced-motion`; all animated assets also disable CSS motion with that media query. `hero-static.svg` is available for renderers without animation. Browser/GitHub image rendering can vary: local Chromium rendering checks do not prove every GitHub client animates SVGs. GitHub's repository image viewer documents animation limitations. Do not replace this with script injection or claim universal playback.

## Sources

- [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub token authentication](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [Scheduled workflow behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [GitHub image rendering](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)
- [Repository audit](repository-audit.md)
