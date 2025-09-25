# Run all *simulation*.py scripts in all subdirectories

find . -type f -name '*simulation*.py' | sort -f | while read -r py_file
do
    dir=$(dirname "$py_file")
    base=$(basename "$py_file")
    echo "Running $base in $dir"
    (cd "$dir" && python "$base")
done