# codespace-deleter

Bulk-deletes all codespaces from a chosen organization.

```
Usage: main.py [OPTIONS]

Options:
  --dry / --no-dry  Don't do any deletions (dry run).
  --token TEXT      GitHub Personal Access Token to use. Can also be set via
                    the GITHUB_TOKEN environment variable.  [required]
  --help            Show this message and exit.
```

For the `token`, create a new [Personal Access Token (Classic)](https://github.com/settings/tokens/new) with the
`admin:org` and `codespace` permissions.
