# Protected artifacts

The version-of-record and archive lineage is immutable. Package construction
must not build or overwrite `main.tex`, `main.pdf`, `main_post-submit.pdf`, or
`servo_caiscfp2026.pdf`. Their required SHA-256 values are:

- `main.pdf`: `7d48eeb1c71ed2cd12e9a677d62587d5f749c5ec19bd8faf0dc9926801bc138d`
- `main_post-submit.pdf`: `4a45951cffd67a80dc25531f103a9a49d65a4c42fed951bdf13eaa07e97e9a01`
- `servo_caiscfp2026.pdf`: `7d48eeb1c71ed2cd12e9a677d62587d5f749c5ec19bd8faf0dc9926801bc138d`

All other tracked PDFs are protected except
`servo_caiscfp2026_post-submit.pdf`. That file alone may be replaced, and only
by copying a verified product from an isolated build directory.

