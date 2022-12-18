#!/usr/bin/env bash

# Check if the argument was provided
if [[ -z "$1" ]]; then
  echo "Please provide a digit as an argument to the script"
  exit 1
fi

# Make sure the argument is a digit
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
  echo "The argument must be a digit"
  exit 1
fi

# Create the destination directory if it doesn't exist
mkdir -p "$1"

# Set the filenames
src_files=(".stubs/day.py" ".stubs/daypt2.py" ".stubs/tools.py" ".stubs/tmpl_data.txt" ".stubs/tmpl_data_test.txt")
dest_files=("$1/$1.py" "$1/$1pt2.py" "$1/tools.py" "$1/data.txt" "$1/data_test.txt")

# Loop over the destination filenames
for i in "${!dest_files[@]}"; do
  dest_file="${dest_files[$i]}"
  src_file="${src_files[$i]}"

  # Check if the destination file already exists
  if [[ -f "$dest_file" ]]; then
    echo "The destination file $dest_file already exists"
  else
    # Copy the file to the destination
    cp "$src_file" "$dest_file"
  fi

done
