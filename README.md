Paradigms website
-----------------

This is the source code for the [Paradigms in Physics
website](https://paradigms.oregonstate.edu).

## Setting up the virtual environment

Here should be instructions on how to set up a virtual environment for
running the project.

## Running tests

This should be as simple as running
```
python3 ./manage.py test
```
in the osu_www directory.

## Building the latex_snippet code

First you need to install rust.  Then install `wasm-pack`.  This takes a while.
```
cargo install wasm-pack
```
The actual build (in the directory with the `latex_snippets` code) is done via
```
wasm-pack build --target web
```
and outputs the relevant files in `pkg/latex_snippets.js` and `pkg/latex_snippets_bg.wasm`.
