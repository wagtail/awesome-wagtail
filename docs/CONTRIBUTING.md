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
- Additions should be added to the top of the relevant subsection.
- New categories, or improvements to the existing categorization are welcome.

### Formatting

- Use the following format: `[package](link) - Description.`
- Link to the code repository, not PyPI.
- Keep descriptions short and simple, but descriptive.
- Start the description with a capital and end with a full stop/period.
- Check your spelling and grammar.
- Wagtail should be referred to as "Wagtail" instead of "Wagtail CMS", with a capital W.

Thank you for your suggestions!

### Formatting items under "Resources"

Everything under [Resources](../README.md#resources) ends with the resource's **last significant update**, in backticks:

```markdown
- [Wagtail Tutorials: Build Blog Step by Step](https://saashammer.com/blog/wagtail-tutorials/) - The tutorials teach you how to create a standard blog from scratch step by step - `2023-06-21`.
```

- Use `YYYY-MM-DD` when known. If only the month or year is verifiable, use `YYYY-MM` or `YYYY` instead.
- Use the date of the content itself (publish date, or last meaningful revision), not the date you added it to this list.
- Add new items at the top of the relevant subsection — Resources are ordered latest first.
- Descriptions always end with a single full stop, before the date.

Each subsection heading has an HTML comment explaining whether it is auto-archived. Items in **Getting started**, **Articles**, **Presentations** and **Videos** are automatically moved to the [archive](archive.md) once they have not been updated for 5 years. **Podcasts**, **Showcases** and **Package lists** are curated manually and never archived automatically.

Leave these comments in place when you edit nearby content, and do not add blank placeholder entries: empty subsections use a `- None yet.` line.

Resource dates and descriptions are checked by CI. Missing or invalid dates, and descriptions that do not end with a full stop, fail the build.

## Formatting and linting

From the repository root, run Biome for Markdown and Ruff for Python. These commands use Node.js and uv to run the same formatter versions as CI.

```sh
git ls-files -z '*.md' | xargs -0 npx --yes @biomejs/biome@2.6.8 format --write
git ls-files -z '*.py' | xargs -0 uvx ruff@0.17.6 format
```

Stage new Markdown and Python files first so Git includes them. To check formatting without editing files, omit `--write` from the Biome command and add `--check` after `format` in the Ruff command.

Run Ruff's Python lint checks with the following command. Add `--fix` to apply available safe fixes.

```sh
git ls-files -z '*.py' | xargs -0 uvx ruff@0.17.6 check
```

## Python type checking

Run ty through uv (CI uses uv 0.13.8). Each tracked Python script declares its Python version and dependencies in an inline metadata block so uv can check it in its own environment.

```sh
git ls-files -z '*.py' | xargs -0 -n 1 uv check --ty-version 0.0.108 --script
```

## Reusing the content

The content of this list is published as an API hosted on [GitHub Pages](https://pages.github.com/): [https://wagtail.github.io/awesome-wagtail/api/v1/readme.json](https://wagtail.github.io/awesome-wagtail/api/v1/readme.json).

Otherwise, directly access the Markdown README: [README.md](https://raw.githubusercontent.com/wagtail/awesome-wagtail/refs/heads/main/README.md).

## Agent skills

The project comes with [agent skills](https://agentskills.io/) to help with maintenance.

### Link maintenance

`/check-links` guides the automated archival workflow: running the script, reviewing its output, moving stale entries to the archive, and updating the README.
