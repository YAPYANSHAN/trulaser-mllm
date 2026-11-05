"""Run every notebook in notebooks/ in order (01, 02, ... 10) and save the outputs inside each notebook.

Usage, from the repo folder:
    python run_all.py                 # run all notebooks
    python run_all.py 09 10           # run only these
    python run_all.py --skip 05 07    # run all except these

Needs: notebook 05 needs Ollama running, 07 needs Neo4j running, 08 needs Java.
If one notebook fails, the rest still run, and a summary at the end says which failed.
"""
import subprocess
import sys
import time
from pathlib import Path

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
        # --inplace saves outputs into the notebook; no timeout because the LLM notebook is slow
        done = subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
                               "--inplace", "--ExecutePreprocessor.timeout=-1", str(nb)])
        ok = done.returncode == 0
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
