# Run Python scripts that match the pattern
for py_file in $(find . -maxdepth 1 -name '*simulation*.py' | sort -f)
do
    echo "Running $py_file"
    python "$py_file"
done


