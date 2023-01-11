import shutil
import os
from zipfile import ZipFile
import glob
import numpy as np
import nrrd
import matplotlib.pyplot as plt

# Change the following to the path to Plastimatch
plastimatch_path = r"c:\Program Files\Plastimatch\bin\plastimatch.exe"

# List of zipped Dicom-files that should be downloaded 
patient_list = [
'1_01_P',
'1_02_P',
'1_03_P',
'1_04_P',
'1_05_P',
'1_06_P',
'1_07_P',
'1_08_P',
'2_03_P',
'2_04_P',
'2_05_P',
'2_06_P',
'2_09_P',
'2_10_P',
'2_11_P',
'3_01_P',
'3_02_P',
'3_03_P',
'3_04_P']

# We are only interested in a set of segmentations described by a particular rtstruct file in each DICOM-folder
rtstruct_list = [
'RS1.2.752.243.1.1.20170427154035429.1370.70822.dcm',
'RS1.2.752.243.1.1.20170427102023318.3200.43424.dcm',
'RS1.2.752.243.1.1.20170427104554025.4000.57421.dcm',
'RS1.2.752.243.1.1.20170427110950995.6600.33771.dcm',
'RS1.2.752.243.1.1.20170427111829785.7400.55867.dcm',
'RS1.2.752.243.1.1.20170427112855618.8800.86717.dcm',
'RS1.2.752.243.1.1.20170427134811058.9900.60476.dcm',
'RS1.2.752.243.1.1.20170427140215948.1090.61415.dcm',
'RS1.2.752.243.1.1.20170427181319346.1520.76456.dcm',
'RS1.2.752.243.1.1.20170503093409104.7100.87740.dcm',
'RS1.2.752.243.1.1.20170427170200673.1400.50461.dcm',
'RS1.2.752.243.1.1.20170503094223488.9100.40107.dcm',
'RS1.2.752.243.1.1.20170427174600300.1420.63875.dcm',
'RS1.2.752.243.1.1.20170428085727667.2000.22800.dcm',
'RS1.2.752.243.1.1.20170427175711382.1470.10702.dcm',
'RS1.2.752.243.1.1.20170427142211409.1210.25812.dcm',
'RS1.2.752.243.1.1.20170427144724037.1320.22835.dcm',
'RS1.2.752.243.1.1.20170428153620336.2700.32818.dcm',
'RS1.2.752.243.1.1.20170428153833470.3000.17263.dcm'
]

# List of ROIs (region of interest)
roi_list = [
'Urinary bladder',
'Rectum',
'Anal canal',
'Penile bulb',
'Neurovascular bundles',
'Femoral head_R',
'Femoral head_L',
'Prostate',
'Seminal vesicles'
]

# Converting the rtstruct files to masks using the Plastimatch software
def convert_rtstructs_to_masks():
    # Check so that all files are donwloaded
    files = [s[6:-4] for s in glob.glob('dicom/*.zip')]
    check = False in [patient_list[i] in files for i in range(len(patient_list))]
    assert(not check), 'The dicom folder is not populated correctly: make sure that you have all of the files (still compressed) and that you have renamed "3_03_P (1).zip" to "3_03_P.zip".'

    # Unzip, generate masks and remove unessary files
    os.mkdir('masks')
    for i in range(len(patient_list)):
       with ZipFile('dicom/' + patient_list[i] + '.zip', 'r') as zipObj:
          zipObj.extract(patient_list[i]+'/'+rtstruct_list[i],'tmp')
       os.system(r'"' + plastimatch_path + '" convert --input tmp/' + patient_list[i] + '/' + rtstruct_list[i] + ' --output-prefix masks/'+ patient_list[i] +' --prefix-format nrrd')
    shutil.rmtree('tmp')


# Construct a marginal function by taking voxel-wise average of the segmentations provided by different users
def get_marginal(i_roi,i_patient):
    tmp = []
    for i_user in range(5):
        filename = 'masks/'+ patient_list[i_patient] +'/'+roi_list[i_roi]+' (User'+str(i_user+1)+').nrrd'
        if os.path.exists(filename):
            readdata, header = nrrd.read(filename)
            tmp.append(readdata)
    m = np.average(tmp,axis=0)

    return m

# Computes a segmentation according to eq [17]
def get_opt_A_seg(m):
    s = m>=1/2
    return s

# Computes a segmentation according to eq [18]
def get_opt_D_seg(m):
    psi = np.flip(np.sort(m.flatten())) # Corresponds to a discrete version of 1-F^{-1}(v)  in the paper
    d = 2*np.cumsum(psi)/(np.sum(m)+np.arange(1,len(psi)+1)) # Vectorized computaton of Dice score for all threshold solutions
    s = m>=np.max(d)/2
    return s

# Compute the relative volumes
def get_rel_vol():
    res_data = np.zeros([len(roi_list), len(patient_list), 2])

    for i_roi in range(len(roi_list)):
        for i_patient in range(len(patient_list)):
            print("Processing marginal: " + str(i_roi*len(patient_list)+i_patient+1) + " of " + str(len(roi_list)*len(patient_list)))
            m = get_marginal(i_roi,i_patient)
            res_data[i_roi,i_patient,0] = np.sum(get_opt_A_seg(m))/np.sum(m)
            res_data[i_roi,i_patient,1] = np.sum(get_opt_D_seg(m))/np.sum(m)

    return res_data

# Store data, table and figure
def save_results(res_data):
    os.mkdir('results')
    np.save("results/results_data_G", res_data)
     
    res_table = open("results/results_table_G.txt", "w")
    res_figure, ax = plt.subplots(3,3,figsize=(9,9))
    for i_roi in range(len(roi_list)):
        ax[i_roi//3,i_roi%3].set_title(roi_list[i_roi].replace("_"," "))
        ax[i_roi//3,i_roi%3].set_xlabel(r'$|s^{\mathrm{A}_m}|/|m|$', fontsize=10)
        ax[i_roi//3,i_roi%3].set_ylabel(r'$|s^{\mathrm{D}_m}|/|m|$', fontsize=10)
        ax[i_roi//3,i_roi%3].set_xlim([0.4,1.6])
        ax[i_roi//3,i_roi%3].set_ylim([0.4,1.6])
        ax[i_roi//3,i_roi%3].set_xticks([0.4,0.7,1.0,1.3,1.6],["0.4","0.7","1.0","1.3","1.6"])
        ax[i_roi//3,i_roi%3].set_yticks([0.4,0.7,1.0,1.3,1.6],["0.4","0.7","1.0","1.3","1.6"])
        ax[i_roi//3,i_roi%3].scatter(res_data[i_roi,:,0],res_data[i_roi,:,1],s=20,facecolors='none', edgecolors='b')

        res_table.write('-------- ' + roi_list[i_roi] + str(' --------') +'\n')
        res_table.write('|s^{\mathrm{A}_m}|/|m| Mean: ' + '{0:.3f}'.format(np.average(res_data[i_roi,:,0]))+ ', Std: ' + '{0:.3f}'.format(np.std(res_data[i_roi,:,0])) + ', Min: ' + '{0:.3f}'.format(np.min(res_data[i_roi,:,0]))+ ', Max: ' + '{0:.3f}'.format(np.max(res_data[i_roi,:,0])) + '\n')
        res_table.write('|s^{\mathrm{D}_m}|/|m| Mean: ' + '{0:.3f}'.format(np.average(res_data[i_roi,:,1]))+ ', Std: ' + '{0:.3f}'.format(np.std(res_data[i_roi,:,1])) + ', Min: ' + '{0:.3f}'.format(np.min(res_data[i_roi,:,1]))+ ', Max: ' + '{0:.3f}'.format(np.max(res_data[i_roi,:,1])) + '\n')
        res_table.write('\n')

    res_figure.tight_layout()
    res_figure.savefig('results/results_G.pdf', bbox_inches='tight', pad_inches=0.0, transparent=True)
    res_table.close()

convert_rtstructs_to_masks()
res_data = get_rel_vol()
save_results(res_data)
