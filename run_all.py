"""Run every notebook in notebooks/ in order (01, 02, ... 10) and save the outputs inside each notebook.

Usage, from the repo folder:
    python run_all.py                 # run all notebooks
    python run_all.py 09 10           # run only these
    python run_all.py --skip 05 07    # run all except these

Needs: notebooks 05 and 11 need Ollama running, 07 needs Neo4j running, 08 needs Java.
If one notebook fails, the rest still run, and a summary at the end says which failed.
"""
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NB_DIR = Path(__file__).parent / "notebooks"


def main(args):
    skip = set()
    if "--skip" in args:
        i = args.index("--skip")
        skip, args = set(args[i + 1:]), args[:i]
    notebooks = sorted(NB_DIR.glob("[0-9][0-9]_*.ipynb"))
    notebooks = [nb for nb in notebooks if (not args or nb.name[:2] in args) and nb.name[:2] not in skip]
    if not notebooks:
        sys.exit("No notebooks matched.")

    results = []
    for nb in notebooks:
        print(f"Running {nb.name} ...", flush=True)
        start = time.time()
        # run inside this Python (no jupyter-nbconvert.exe, which Windows Smart App Control can block)
        notebook = nbformat.read(nb, as_version=4)
        try:
            NotebookClient(notebook, timeout=None, kernel_name="python3",
                           resources={"metadata": {"path": str(NB_DIR)}}).execute()
            ok = True
        except Exception as e:
            print(f"  error: {str(e).strip().splitlines()[-1]}")
            ok = False
        nbformat.write(notebook, nb)  # save outputs, including the error cell if it failed
        results.append((nb.name, ok, time.time() - start))
        print(f"  {'OK' if ok else 'FAILED'} in {time.time() - start:.0f} s\n", flush=True)

    print("Summary")
    for name, ok, secs in results:
        print(f"  {'OK    ' if ok else 'FAILED'} {name} ({secs:.0f} s)")
    if not all(ok for _, ok, _ in results):
        print("\nOpen a FAILED notebook in Jupyter to see the error cell.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
