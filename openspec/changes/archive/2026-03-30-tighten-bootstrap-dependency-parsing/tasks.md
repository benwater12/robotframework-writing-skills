## 1. Update dependency loading

- [x] 1.1 Refine `read_dependencies()` to distinguish parser availability from configuration errors
- [x] 1.2 Validate that `project.dependencies` is a list of strings before returning it
- [x] 1.3 Add clear `SystemExit` messages for malformed TOML and invalid dependency structures

## 2. Verify

- [x] 2.1 Run a targeted check to confirm the script still falls back to defaults only when dependency metadata is absent
