name: Combine Textures

on:
  workflow_dispatch:
  push:
    paths:
      - 'parts/**.png'
      - '.github/workflows/combine_textures.yml'

jobs:
  combine:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install Pillow
      run: pip install Pillow

    - name: Generate combined textures
      run: python combine_textures.py

    - name: Upload generated textures
      uses: stefanzweifel/git-auto-commit-action@v5
      with:
        commit_message: "Generate combined textures"
        file_pattern: "resourcepack/textures/item/*.png"
