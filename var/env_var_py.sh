# env_var_py.sh
WINDOW="neighbor"
export THRESHOLD=0.5
echo "outer: window is ${WINDOW} and threshold is ${THRESHOLD}"
python src/env_var_py.py
