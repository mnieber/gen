# :Post-processing

## Snippet (`specs/foo/settings.yml`)

```yaml
bin:
  prettier:
    exe: ~/.yarn/bin/prettier
    config: ~/.prettierrc
post_process:
  '.ts(x)?': [prettier]
```

## Fact

The moonleap :settings file may contain a list of post-processing steps.
