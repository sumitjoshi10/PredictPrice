# Will predict the price
## STEPS

### STEP 1: Clone the Repository using the following commang
```bash
 git clone https://github.com/sumitjoshi10/PredictScore.git
```
### STEP 2- Create a conda environment after opening the repository in VSCODE

```bash
conda create -p venv python=3.12 -y
```

```bash
conda activate ./venv
```
OR
```bash
source activate ./venv
```

### STEP 3- install the requirements
```bash
pip install -r requirements.txt
```

### STEP 4 - To train the model (Optional)
```bash
python src\pipeline\training.py
```

### STEP 5 - Predcition
```bash
python3 app.py
```
```bash
https://127.0.0.0:5000
```


