# Update Overview

## Updates 21-01-2025
- `Alsico.py` -> `Alsico v1.0.0.py`
    - Changed the name of `Alsico.py` to `Alsico v1.0.0.py`
    - This reflects that it is version 1 of the code and might reduce any possible confusion about
    which Alsico file to use.
    - Added this file to a "Bin" folder
- `Alscio_with_manual_annotations/py` -> `Alsico v2.0.0.py`
    - Changed the name of `Alscio_with_manual_annotations/py` to `Alsico v2.0.0.py`
    - this more accurately represents the fact that this is a second iteration of the code with a 
    major new feature added.
- `Cyclop/Bin/`
    - Added a `Bin` folder to store earlier versions of the code.
- `Cyclop/Data_processing`
    - Added a `Data_preprocessing` folder to store scripts associated with data processing/analysis.
    - This folder is still included in the `.gitignore`, but will be made available when scripts
    are finished.


## Updates 20-01-2025
- `Alsico.py`
    - Cleaned up the code for readability and to follow the PEP8 guidelines.
    - Added a function that checks if the "Experiment_data" folder exists. If this does not exists, 
    it creates this folder automatically.

- `Alsico_with_manual_annotations.py`
    - Cleaned up the code for readability and to follow the PEP8 gudielines.
    - Added a function that checks if the "Experiment_data" folder exists. If this does not exists, 
    it creates this folder automatically.
    

## Updates 17-01-2025
-  `Alsico_with_manual_annotations.py`
    - Added a script that allows manual annotations during the experiment. Run this script if you 
    want to include manual annotations.
    - After starting the experiment, you can now enter manual annotations in `Terminal`.
    - Just type your annotation and press **Enter**.
    - This will save your annotation and the timestamp at the moment you press enter. 
    This annotation is then included in the final savefile.

- `Alsico.py`
    - Timestamps corrected from GMT to GMT-1.

- `Updates.md`
    - Added Updates.md as a means to communicate updates.

- `README.md`
    - changes to include additional files