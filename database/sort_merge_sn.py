import sys
import pandas as pd

def process_file(input_file):
    # Load the file (comma-separated)
    df = pd.read_csv(input_file)

    # Sort by SNname
    df = df.sort_values(by='SNname', ignore_index=True)

    # Prepare final DataFrame and conflict tracking
    final_rows = []
    conflict_log = []

    # Group by SNname to check for duplicates
    grouped = df.groupby('SNname')

    for snname, group in grouped:
        if len(group) == 1:
            # No duplicate, keep as is
            final_rows.append(group.iloc[0].to_dict())
        else:
            # Handle duplicates (more than one entry for the same SNname)
            base = group.iloc[0].copy()
            conflicts = []

            for idx, row in group.iterrows():
                if idx == group.index[0]:
                    continue  # Skip first (base)
                for col in df.columns:
                    if pd.notna(row[col]) and pd.notna(base[col]) and row[col] != base[col]:
                        conflicts.append((col, base[col], row[col]))

            if conflicts:
                # Conflict detected — log and keep all original rows (as dicts)
                conflict_log.append(f"Conflict for SNname {snname}:")
                for col, val1, val2 in conflicts:
                    conflict_log.append(f" - Column '{col}': '{val1}' vs '{val2}'")
                final_rows.extend(group.to_dict(orient='records'))
            else:
                # No conflict — merge (fill missing data in base with other rows' data)
                for idx, row in group.iterrows():
                    for col in df.columns:
                        if pd.isna(base[col]) and pd.notna(row[col]):
                            base[col] = row[col]
                final_rows.append(base.to_dict())

    # Convert final rows back into DataFrame
    final_df = pd.DataFrame(final_rows)

    # Output filename (add a suffix to the input name)
    output_file = input_file.replace('.csv', '_sorted_merged.csv')

    # Save to output file (comma-separated)
    final_df.to_csv(output_file, index=False)

    # Print conflicts to screen
    if conflict_log:
        print("\nConflicts detected during merging:\n")
        print("\n".join(conflict_log))

        # Optional: save conflicts to a log file
        conflict_log_file = input_file.replace('.csv', '_conflicts.log')
        with open(conflict_log_file, 'w') as f:
            f.write("\n".join(conflict_log))
        print(f"\nConflicts also saved to '{conflict_log_file}'")
    else:
        print("No conflicts detected — all duplicates merged cleanly.")

    print(f"\nSorted and merged file saved as '{output_file}'")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort_merge_sn.py <input_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_file(input_file)
