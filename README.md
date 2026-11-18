# TEAM4-FALL2026-SQA

**Team name:** Team4

**Members:** An Dinh, Sarabeth Shannon


## Setup

Requires Python 3.11+ and [yq](https://github.com/mikefarah/yq) (used by the scanner).

```bash
python3 -m venv .venv
source .venv/bin/activate # FOR WINDOWS: .venv/Scripts/activate
pip install ruamel.yaml pandas numpy pyyaml typer sarif-om jschema-to-python
brew install yq        # macOS; preinstalled on GitHub Actions runners
```

## Running the SQA activities locally

| Activity | Command | Output |
|---|---|---|
| Unit tests | `python TEST_PARSING.py` | console |
| Fuzzing | `python fuzz.py` | `fuzz_report.txt` |
| Forensics | `python -c "import scanner; scanner.runScanner('TEST_ARTIFACTS')"` | `forensics.log` |

## Continuous integration

The GitHub Actions workflow [`.github/workflows/sqa.yml`](.github/workflows/sqa.yml) runs
on every push. It runs the unit tests, the fuzzer, and the scanner, then uploads
`fuzz_report.txt` and `forensics.log` as the **sqa-evidence** artifact.

To run it manually: **Actions → SQA Pipeline → Run workflow**.
To see results: open a run → **Artifacts → sqa-evidence**.
