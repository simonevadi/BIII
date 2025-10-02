import re
import pandas as pd
from pathlib import Path
from typing import Dict, List

def extract_energy_flux(base_filename: str, n_files: int, output_filename: str):
    """
    Extract Energy and Flux columns from a series of files and combine them into one DataFrame.
    Column numbering follows odd integers: 1, 3, 5, ...

    Args:
        base_filename (str): Base filename (without the "-X.txt" part).
        n_files (int): Number of files to read (expects files named base-X.txt for X=0..n_files-1).
        output_filename (str): Path where the combined DataFrame will be saved as CSV.

    Returns:
        pd.DataFrame: The combined DataFrame with all extracted columns.
    """
    dfs = []
    for i in range(n_files):
        fname = f"{base_filename}{i}.txt"

        # read file, skip first 2 header lines
        df = pd.read_csv(fname, delim_whitespace=True, skiprows=1)

        # odd numbering: 1, 3, 5, ...
        idx = i * 2 + 1

        # select and rename columns
        df = df[["eV", "ph/s/0.1%"]].rename(
            columns={
                "eV": f"Energy{idx}[eV]",
                "ph/s/0.1%": f"Photons{idx}"
            }
        )

        dfs.append(df)

    # combine side by side
    final_df = pd.concat(dfs, axis=1)

    # save
    final_df.to_csv(output_filename, index=False)

    return final_df


# uses your existing extract_energy_flux(base_filename, n_files, output_filename)

def batch_extract_energy_flux(folder: str) -> Dict[str, pd.DataFrame]:
    """
    Scan `folder` for files named like '<base>-<index>.txt' (index = 0..N),
    group by <base>, infer the number of files for each base, and call
    `extract_energy_flux` for each group. Saves one CSV per base inside `folder`.

    Returns:
        dict[str, pd.DataFrame]: Mapping base -> resulting DataFrame from extract_energy_flux.
    """
    folder_path = Path(folder)
    pattern = re.compile(r"^(?P<base>.+-)(?P<idx>\d+)\.txt$")

    # 1) collect files and group by base
    groups: Dict[str, List[int]] = {}
    for p in folder_path.glob("*.txt"):
        m = pattern.match(p.name)
        if not m:
            continue
        base = m.group("base")        # keep trailing '-'
        idx = int(m.group("idx"))
        groups.setdefault(base, []).append(idx)

    if not groups:
        print(f"No matching '*-<index>.txt' files found in: {folder}")
        return {}

    results: Dict[str, pd.DataFrame] = {}

    # 2) process each base
    for base, indices in groups.items():
        indices_sorted = sorted(set(indices))
        n_files = max(indices_sorted) + 1  # assume indices start at 0

        # warn if indices are not contiguous from 0..max
        expected = list(range(n_files))
        if indices_sorted != expected:
            missing = set(expected) - set(indices_sorted)
            print(f"[WARN] For base '{base}', missing indices: {sorted(missing)}. "
                  f"Proceeding with n_files={n_files} (based on max index).")

        base_filename = str(folder_path / base)  # include trailing '-'
        # output file name: strip trailing '-' and add .csv, saved in folder
        output_stem = base[:-1]  # remove trailing '-'
        output_filename = str(folder_path / f"{output_stem}.csv")

        df = extract_energy_flux(base_filename=base_filename,
                                 n_files=n_files,
                                 output_filename=output_filename)
        results[base] = df
        print(f"[OK] Wrote: {output_filename} (n_files={n_files})")

    return results


####################################
# assuming extract_energy_flux is defined as in your message
all_dfs = batch_extract_energy_flux("Elisa-UE65-HL-1-1")
########################################