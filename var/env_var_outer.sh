# env_var_outer.sh
WINDOW="neighbor"
export THRESHOLD=0.5
echo "outer: window is ${WINDOW} and threshold is ${THRESHOLD}"
bash src/env_var_inner.sh
