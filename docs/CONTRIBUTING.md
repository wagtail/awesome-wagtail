# Contribution Guidelines

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Guidelines for additions

Please ensure your pull request adheres to the following guidelines.

### Criteria for inclusion

- Additions should be awesome. Tell us why you think your addition should be included.
- Should be related to Wagtail.
- For packages - they should be tested and documented.

### Pull request process

- Search previous suggestions before making a new one, as yours may be a duplicate.
- Make an individual pull request for each suggestion, with a useful title.
- Additions should be added to the bottom of the relevant category.
- New categories, or improvements to the existing categorization are welcome.

### Formatting

- Use the following format: `[package](link) - Description.`
- Link to the code repository, not PyPI.
- Keep descriptions short and simple, but descriptive.
- Start the description with a capital and end with a full stop/period.
- Check your spelling and grammar.
- Wagtail should be referred to as "Wagtail" instead of "Wagtail CMS", with a capital W.

Thank you for your suggestions!

## Formatting files

From the repository root, run Biome for Markdown and Ruff for Python. These commands use Node.js and uv to run the same formatter versions as CI.

```sh
git ls-files -z '*.md' | xargs -0 npx --yes @biomejs/biome@2.6.8 format --write
git ls-files -z '*.py' | xargs -0 uvx ruff@0.17.6 format
```

Stage new Markdown and Python files first so Git includes them. To check formatting without editing files, omit `--write` from the Biome command and add `--check` after `format` in the Ruff command.

## Reusing the content

The content of this list is published as an API hosted on [GitHub Pages](https://pages.github.com/): [https://wagtail.github.io/awesome-wagtail/api/v1/readme.json](https://wagtail.github.io/awesome-wagtail/api/v1/readme.json).

Otherwise, directly access the Markdown README: [README.md](https://raw.githubusercontent.com/wagtail/awesome-wagtail/refs/heads/main/README.md).

## Agent skills

The project comes with [agent skills](https://agentskills.io/) to help with maintenance.

### Link maintenance

`/check-links` guides the automated archival workflow: running the script, reviewing its output, moving stale entries to the archive, and updating the README.
