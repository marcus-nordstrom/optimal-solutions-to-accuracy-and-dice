Setup instructions

------------------------------------------------------------------------
1. Path: 
Before executing any code, make sure to set the file path to "Experiments_L".
This folder will contain the code together with the data when downloaded and processed.
------------------------------------------------------------------------
2. Data:
To get the data set, follow this link:
https://doi.org/10.7937/K9/TCIA.2015.LO9QL9SX
and download the Radiologist Annotations/Segmentations (XML) file.

In our experiments, we use version 3, which at the time of writing is the current version.
Extract the zip file to "Experiments_L/xml".
Note that the DICOM files are not necessary in order to run the experiments.
------------------------------------------------------------------------
3. Python:
We use Python 3.10.4 which can be found at the following address.
https://www.python.org/downloads/

Once in the right python environment, the necessary packages can be installed by using the provided requirements file.
> pip install -r requirements.txt
------------------------------------------------------------------------
4. Running the code:
To execute the code, make sure your path is set to the Experiments_L.
The code is then simply executed with the following.
> python main.py¨

It will take approximately 30min on a  descent desktop computer and should be no problems running on a laptop.
No GPU computations are done.
The code will use the pilidc library to query annotation data and generate masks.
The masks are used to compute the discrete versions of the marginal functions and used to compute the relative volumes.
When complete, the results of the experiment can be found under "Experiments_L/results".
------------------------------------------------------------------------
