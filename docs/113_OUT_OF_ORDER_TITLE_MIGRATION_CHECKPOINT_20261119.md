# Out of Order — public storyboard title migration checkpoint (2026-11-19)

The owner has chosen **Out of Order** as the official game title. The previous working title, *The Acceptable Error*, is historical, not an active name. This review branch stages display-name changes for the public storyboard without changing narrative, art, gameplay, schemas or canonical exports.

## Scoped changes in this review branch

- Public README's current title and current-source description
- Root redirect page's HTML title
- Storyboard viewer's tab heading, visible header and fatal-ending preview label
- Pages workflow's human-facing job name

## Still pending — do not claim migrated

- Private game repo: `InterstellarHarvest/CYOA` (rename target `InterstellarHarvest/out-of-order`)
- Canonical public storyboard repo: `InterstellarHarvest/CYOA-storyboard` (rename target `InterstellarHarvest/out-of-order-storyboard`)
- Live Pages site: `https://interstellarharvest.github.io/CYOA-storyboard/` (anticipated new path must be verified after rename)
- Hardcoded active repository URLs, GitHub Actions links, JSON sync configuration, export generators and cross-repository integration records
- Any external bookmarked links, tools or review-app deep links that reference the old Pages prefix

Do not replace immutable source repository names in historic art-provenance records. Do not rename `cyoa-*` schema IDs, localStorage keys, pinned source revisions, or code paths merely for branding: those are compatibility contracts. Changing an export generator requires regenerating its output and passing the canonical drift check. Historical design documents retain their original titles and dates.

## Deployment gate

Keep this as an independent review until the coordinated repository migration. Before public publication, verify canonical sync validation, review-app URLs (root, storyboard, artwork lab), selected image previews, Chapter 3 review-layout routes, and old-link behavior. The private game `main` and public storyboard `main` are untouched by this branch.
