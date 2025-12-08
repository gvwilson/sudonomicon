# shell_var_outer.sh
WINDOW="neighbor"
echo "outer: window is ${WINDOW}"
bash src/shell_var_inner.sh
