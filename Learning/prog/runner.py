import os
import sys
from pathlib import Path
from local_library.stoch import StochasticProcessType, StochasticProcessGenerator

# Get the current working directory
current_directory = Path(os.getcwd())

parent_directory = Path(current_directory).parent
lib_dir = current_directory / 'local_library'

sys.path.append(parent_directory)
sys.path.append(current_directory)
sys.path.append(lib_dir)

print(f"Parent Directory Directory: {parent_directory}")
print(f"Current Directory: {current_directory}")
print(f"Library Directories: {lib_dir}")
print(f"Current Module directories: {sys.path}")

test = StochasticProcessGenerator(StochasticProcessType.BROWNIAN_MOTION, 10, 10)
test.generate_process

