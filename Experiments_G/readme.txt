Setup instructions

------------------------------------------------------------------------
1. Path:
When unzipping the Supplemental Material, there will be a folder named Exierments_G.
This folder will contain the code together with the data when downloaded and processed.
------------------------------------------------------------------------
2. Data:
The data we use (Version 1, May 24 2017) can be acquired from the following link.
https://doi.org/10.5281/zenodo.583096

Scroll down to the box labeled Files, click on button labeled Request access... and follow the instructions. 
Access will be granted provided your fulfill the criteria of requesting the data for academic or educational purposes.
When granted, an email will be sent to you with a link.
Follow this link and scroll down to the box labeled Files again.
A list of files, each with a button labeled 
"Download" should now be visible.
Download all of the files to the Experiments_G/dicom folder and rename
3_03_P (1).zip  to 3_03_P.zip.
When done Experiments_G/dicom, should be populated with the following 19 files:
1_01_P.zip,
1_02_P.zip,
1_03_P.zip,
1_04_P.zip,
1_05_P.zip,
1_06_P.zip,
1_07_P.zip,
1_08_P.zip,
2_03_P.zip,
2_04_P.zip,
2_05_P.zip,
2_06_P.zip,
2_09_P.zip,
2_10_P.zip,
2_11_P.zip,
3_01_P.zip,
3_02_P.zip,
3_03_P.zip,
3_04_P.zip.
------------------------------------------------------------------------
3. Plastimatch: 
To make our computations, we need to convert the segmentations from the \emph{rtstruct} format to the binary mask format \emph{nrrd}.
We use Plastimatch version 1.9.3 for Windows 64 which has a BSD-style license.
Both the installer and license can be found at the following address.
http://plastimatch.org/

For Ubuntu users, the Plastimatch software is available in the apt-repository.
We see no reason to why running it on this platform should be a problem but it has not been tested.
------------------------------------------------------------------------
4. Python:
We use Python 3.10.4 which can be found at the following address.
https://www.python.org/downloads/

Once in the right python environment, the necessary packages can be installed by using the provided requirements file.
> pip install -r requirements.txt
------------------------------------------------------------------------
5. Running the code:
To execute the code, make sure your path is set to the Experiments_G.
In the main.py file, edit the variable "plastimatch_match" so that it is compatible with the install path of Plastimatch.
The code is then simply executed with the following.
> python main.py

It will take approximately 30 min on a  descent desktop computer and should be no problems running on a laptop.
No GPU computations are done.
The code will start by unzipping all of the downloaded files to a temporary folder that will be deleted after the run.
It will then run Plastimatch to extract a mask for every available segmentation and put the results in \path{Experiments_G/masks}.
Once this is done, the discrete versions of the marginal functions are computed and used to compute the relative volumes.
When complete, the results of the experiment can be found under \path{Experiments_G/results}.
------------------------------------------------------------------------