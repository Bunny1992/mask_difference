# mask_difference
Mask difference is a function to identify the difference in lesions between two Nifti nii.gz MRI images.
The functions compares the MRI images and creates two differentiation arrays named additions and subtratcions.
Additions: Numpy array which collects the additional labels in the first nifti image which are not present in the second image.
Subtractions: Numpy array which collects the additional labels in the second image which are not in the first.
The addittions and subtractions are the boolean values with 0,1 at the start. Post new labels are provided to the numpy array using the scipy.ndimage.label function.
Also center of mass is calculated using the scipy ndimage.center_of_mass() for the cluster of labesl within the numpy array.

Input Parameters:
First: The first Nifti iamge to be compared.
Second: The second Nifti image to be compared with first
connect_diagonal: Boolean value (True/False) set by the user to make the function understand if its a need to check the labels diagonally connected or no.

Output: Changes.json file with the below data
{
  additions:
    Index: Volume: Frequcency of a labels with the label cluster in the numpy array.
           Center: Center of mass calulated for the cluster of labels.

  subtratcions:
    Index: Volume: Frequcency of a labels with the label cluster in the numpy array.
           Center: Center of mass calulated for the cluster of labels.
  }
  
