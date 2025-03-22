import pandas as pd

# Load both files (comma-separated)
file1 = pd.read_csv('SwiftSNweblist2016PTF.csv')
file2 = pd.read_csv('MatchedSwiftTNS.csv')

# Drop 'TNSprefix' column from file2 if it exists
if 'TNSprefix' in file2.columns:
    file2 = file2.drop(columns=['TNSprefix'])

# Rename columns in file2 to match file1 where appropriate
file2 = file2.rename(columns={
    'name': 'SNname',
    'right ascension': 'SNra',
    'declination': 'SNdec'
})

# Add any missing columns from file1 to file2, filling with NaN
for col in file1.columns:
    if col not in file2.columns:
        file2[col] = pd.NA

# Reorder columns in file2 to match file1
file2 = file2[file1.columns]

# Combine both DataFrames into one
combined = pd.concat([file1, file2], ignore_index=True)

# Sort by SNname
combined = combined.sort_values(by='SNname', ignore_index=True)

# Prepare final DataFrame and conflict tracking
final_rows = []
conflict_log = []

# Group by SNname to check for duplicates
grouped = combined.groupby('SNname')

for snname, group in grouped:
    if len(group) == 1:
        # No duplicate, keep as is — convert to dict to be consistent
        final_rows.append(group.iloc[0].to_dict())
    else:
        # Handle duplicates (more than one entry for the same SNname)
        base = group.iloc[0].copy()
        conflicts = []

        for idx, row in group.iterrows():
            if idx == group.index[0]:
                continue  # Skip first (base)
            for col in combined.columns:
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
                for col in combined.columns:
                    if pd.isna(base[col]) and pd.notna(row[col]):
                        base[col] = row[col]
            final_rows.append(base.to_dict())

# Convert final rows back into DataFrame
final_df = pd.DataFrame(final_rows)

# Save to output file (comma-separated)
final_df.to_csv('CombinedTrimmedAllSwiftSNlist.csv', index=False)

# Print conflicts to screen
if conflict_log:
    print("\nConflicts detected during merging:\n")
    print("\n".join(conflict_log))
else:
    print("No conflicts detected — all duplicates merged cleanly.")

print("\nCombined file saved as 'CombinedTrimmedAllSwiftSNlist.csv'")

