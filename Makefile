# Makefile example of the same functionality

all: buildir buildir/a buildir/b buildir/c

buildir:
	sleep 1
	mkdir -p $@

buildir/a: buildir
	sleep 1
	echo "a" > $@

buildir/b: buildir
	sleep 1
	echo "b" > $@

buildir/c: buildir/a buildir/b
	sleep 1
	cat $^ > $@
