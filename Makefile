.PHONY: demo

default: demo

bin/pygmentize:
	python3 -m venv .
	bin/pip install pygments>=2.2.0

demo: bin/pygmentize
	bin/pygmentize -f terminal -l cddl_lexer.py:CddlLexer -x demo.cddl

html: bin/pygmentize
	mkdir -p out
	bin/pygmentize -f html -O full,style=default -l cddl_lexer.py:CddlLexer -x demo.cddl > out/demo_default.html
	bin/pygmentize -f html -O full,style=monokai -l cddl_lexer.py:CddlLexer -x demo.cddl > out/demo_monokai.html
