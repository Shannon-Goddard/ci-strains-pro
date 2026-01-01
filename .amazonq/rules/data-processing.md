# Data Processing Rules

## File Integrity
- NEVER overwrite raw data. 
- Always create a `_cleaned` or `_processed` version of a column or file.
- Use `latin-1` encoding for CSV reads to handle special cannabis breeder characters.

## Transparency Log Requirement
- Every time you generate a Python script, you must also generate a `methodology.md` for that folder.
- The methodology must state: "Logic designed by Amazon Q, verified by Shannon Goddard."

## Naming Conventions
- Repos: `ci-strains-pro`
- Folders: `pipeline/0X_step_name/`
- CSVs: lowercase_with_underscores.csv