
# Import required libraries.
from nilearn import plotting
import pylab as plt
import numpy as np
import nibabel as nb
import logging
import json
import sys
from nilearn import plotting
import pylab as plt
#Scipy
from scipy.ndimage import label, generate_binary_structure
from scipy import ndimage

def max_diff(first, second, connect_diagonal):
	"""Takes two nifti images to identify the difference in lesions when compared
    
    Arguments:
		first: 	Nifti Image .nii.gz file 1.
		second:	Nifti Image .nii.gz file 2. 
        
        
    Calculations:
        additions: all lesions in first which are not in second. 
	subtractions: all lesions in second which are not in first.

    Returns:
	json Object
		volume : Label number.
		center : Center of Mass of the labels.
		connect_diagonal : User input to understand if the labels are diagnoally connected or no(Boolean Value : True/False       )

	Note: This result set will be calculated for both aditions and Subtractions.
	
    """
	
	## Load a functional image of subject 01
	first_img = nb.load(first)
	#first_img = nb.load('C:/Users/I6636/Documents/mask_difference/edited_lesion.nii.gz')
	#print("Data type of first_img is: ",first_img.dtype)
	second_img = nb.load(second)
	#second_img = nb.load('mask_difference/lqsegr.nii.gz')
	#print("Data type of second_img is: ",second_img.dtype)

	#Get the fdata of the images
	first = first_img.get_fdata()
	second = second_img.get_fdata()

	# Set the default value of Connect_diagonal to false
	CONNECT_DIAGONAL = False
	CONNECT_DIAGONAL = connect_diagonal
	
	#Check if dimensions of both the images are same else exit.
	if first.shape != second.shape:
		
		logging.error("Exiting as the Dimensions of the two images dont match")
		
	else:
		
		print("Dimensions of the images match")
		## Convert the labels to 0 if not labelled and 1 if labelled 
		first_bool = (first>0).astype(int)
		second_bool = (second>0).astype(int)
	
		additions = (first_bool > second_bool).astype(int)
		subtractions = (first_bool < second_bool).astype(int)
        
        ## Add labels to 0 and 1 using nd.image.label() function.
        ## Get input from the user to check diagonal connectivity of labels.
		if CONNECT_DIAGONAL == 'True':
			print("Connect diagonal value is set as true by the user")
			labeled_array_additions, num_features_additions = label(additions, np.ones((3, 3, 3)))

			labeled_array_subtractions, num_features_subtractions = label(subtractions, np.ones((3, 3, 3)))

		else:
			print("Connect diagonal value is set as false by the user")
			labeled_array_additions, num_features_additions = label(additions)
			labeled_array_subtractions, num_features_subtractions = label(subtractions)
	
		#Creating additions and subtractions dictionaries.
		additions = {}
		subtractions = {} 
		for i in range(1,num_features_additions+1):
			center_additions= ndimage.center_of_mass(labeled_array_additions, labels=labeled_array_additions, index=i)
			center = list(int(x)+1 for x in list(center_additions))
			tmp = {}
			tmp["Volume"] = np.count_nonzero(labeled_array_additions == i)
			tmp["center"] = center
			additions[i] = tmp


		for i in range(1,num_features_subtractions+1):
			center_subtractions= ndimage.center_of_mass(labeled_array_subtractions, labels=labeled_array_subtractions, index=i)
			center = list(int(x)+1 for x in list(center_subtractions))
			tmp = {}
			tmp["Volume"] = np.count_nonzero(labeled_array_subtractions == i)
			tmp["center"] = center
			subtractions[i] = tmp

		changes = {}
		changes['additions'] = additions
		changes['subtractions'] = subtractions
		changes['CONNECT_DIAGONAL'] = CONNECT_DIAGONAL
		with open("changes.json", "w") as outfile:
			json.dump(changes, outfile)

if __name__ == "__main__":
	first = sys.argv[1]
	second = sys.argv[2]
	connect_diagonal = sys.argv[3]
	max_diff(first, second, connect_diagonal)
