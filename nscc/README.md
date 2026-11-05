# Running the LLM notebooks on NSCC (ASPIRE 2A)

Notebooks 05 and 11 call Ollama. On an A100 (40 GB) the whole `llama3.1:8b` model fits in GPU memory,
so it runs much faster than on a laptop GPU that has to share the model with the CPU.

The idea: the **login node** has internet, so you install Ollama and download the model there once.
The **GPU job** has no internet; it starts Ollama on the GPU node and runs the notebook without opening it,
saving the outputs into the `.ipynb` file. No notebook code changes: Ollama runs at `localhost:11434` inside the job,
which is what the notebooks already use.

## One-time setup (on the login node)

```bash
ssh <your-nscc-username>@aspire2a.nscc.sg          # NTU VPN first if you are off campus
git clone https://github.com/YAPYANSHAN/trulaser-mllm.git
cd trulaser-mllm

# Python packages
module load miniforge3
conda create -y -n fyp python=3.11
source activate fyp
pip install -r requirements.txt

# Ollama (no admin rights needed: it unpacks into your home folder)
mkdir -p ~/ollama
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o /tmp/ollama.tgz
tar -C ~/ollama -xzf /tmp/ollama.tgz
# If that download 404s, newer releases use .tar.zst instead:
#   curl -L https://ollama.com/download/ollama-linux-amd64.tar.zst | tar -C ~/ollama --zstd -x

# Download the model once (about 5 GB) into your home folder
export PATH="$HOME/ollama/bin:$PATH" OLLAMA_MODELS="$HOME/ollama-models"
ollama serve > /tmp/ollama.log 2>&1 &
sleep 5 && ollama pull llama3.1:8b
kill %1
```

Copy the gold list (it is not in git) from your PC, in PowerShell from the folder that holds it:

```powershell
scp manual_gold_facts.csv <your-nscc-username>@aspire2a.nscc.sg:~/trulaser-mllm/data/
```

## Each run

```bash
cd ~/trulaser-mllm && git pull
qsub nscc/run_notebook.pbs                                   # notebook 11
qsub -v NB=05_diagnose_with_llm.ipynb nscc/run_notebook.pbs  # notebook 05
qstat -u $USER                                               # Q = waiting, R = running
```

When it finishes, `fyp_nb.o<jobid>` has the log, and the notebook in `notebooks/` holds the outputs.
Copy it back to your PC (PowerShell):

```powershell
scp <your-nscc-username>@aspire2a.nscc.sg:~/trulaser-mllm/notebooks/11_manual_to_graph_facts.ipynb notebooks/
```

## If something fails

- `qsub` asks for a project: add `-P personal-<your-nscc-username>` (or the project code NSCC gave you).
- `module load miniforge3` fails: run `module avail` and load the conda/python module listed there, then edit the
  same line in `run_notebook.pbs`.
- Notebook says "Ollama is not running": look at `ollama_<jobid>.log` in the repo folder.
- Job killed at 2 hours: raise `walltime` in `run_notebook.pbs`.
