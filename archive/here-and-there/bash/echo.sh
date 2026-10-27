#!/bin/bash

echo "input two number:"
read a
read b

echo '[+]' `expr $a + $b`
echo '[-]' `expr $a - $b`
echo '[*]' `expr $a \* $b`
echo '[/]' `expr $a / $b`
