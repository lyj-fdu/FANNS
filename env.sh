# Update conda base environment
conda update -n base -c defaults conda

# Create a new environment named 'fanns' with Python 3.9
# To delete: conda env remove --name fanns
conda create -n fanns python=3.9

# Activate the environment
conda activate fanns

# Add conda-forge channel (for accessing updated packages)
conda config --add channels conda-forge

# Install essential build tools
conda install -c conda-forge gcc gxx cmake ninja

# Install Python packages
pip install pyyaml ipykernel pandas numpy pyarrow tensorflow-cpu tqdm scikit-learn umap-learn POT faiss-cpu

# Install Mahalanobis distance package from GitHub
pip install git+https://github.com/mosegui/mahalanobis.git

echo "IMPORTANT: Manual modification required!"
echo "Locate the conda-installed mahalanobis package using \`pip show mahalanobis\`"
echo "and manually replace \`np.linalg.inv\` with \`np.linalg.pinv\`, then reload:"
echo "------------------- Python code -------------------"
echo "import importlib"
echo "import mahalanobis"
echo "importlib.reload(mahalanobis)"
echo "---------------------------------------------------"
