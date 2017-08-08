#!/usr/bin/env bash
jupyter nbconvert --to slides --reveal-prefix=reveal.js \
    --template=custom_template.tpl timezone_troubles.ipynb \
    --post serve