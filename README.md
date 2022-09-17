![](https://img.shields.io/badge/code%20style-black-000000.svg)

# Visialization
[streamlit](https://cjkjvfnby-extract-vizualization-app-kchce5.streamlitapp.com/)

# Development

## Install dev requirements
```shell
pip install -r requirements-dev.txt
```

## Install pre-commit
- add hooks
  ```shell
  pre-commit install
  pre-commit install --hook-type commit-msg
  ```
- update to the latest versions
  ```shell
  pre-commit autoupdate
  ```

## Formatting and Linting
```shell
pre-commit run --all-files
```

## Run test
```shell
pytest --cov=zip_cloud --cov-report html
```
