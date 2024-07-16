# Author: Liu Li, Priscille de Dumast
# First version: 2022/05/20
# Updated on: 2024/07/16

import os

import numpy as np
import SimpleITK as sitk
import skimage
import gudhi as gd



def compute_topological_features(map):
    """
    Evaluate the topology of a given map.

    Parameters:
    - map: A 3D numpy array representing the map.

    Returns:
    - A tuple containing the Betti numbers and the Euler characteristic of the map.
    """

    # Betti number computation
    cubic = gd.CubicalComplex(dimensions=map.shape,
                              top_dimensional_cells=map.flatten(order='F'))

    cubic.persistence(homology_coeff_field=2, min_persistence=0.99)
    pairs_nda = cubic.cofaces_of_persistence_pairs()

    betti_number_0dim = pairs_nda[0][2].shape[0]
    betti_number_1dim = pairs_nda[0][1].shape[0]
    betti_number_2dim = pairs_nda[0][0].shape[0]
    betti_number_list = [betti_number_0dim, betti_number_1dim, betti_number_2dim]
    ec = int(betti_number_0dim) - int(betti_number_1dim) + int(betti_number_2dim)
    return betti_number_list, ec



def main():
    """
    Sample code to evaluate the betti number and Euler characteristic on segmentation data from FeTA challenge.
    """
    feta_dir = '/home/priscille/feta_2.0'
    sub = 'sub-042'

    print('Computation of the Betti number for: {}'.format(file_dir))

    file_dir = os.path.join(feta_dir, sub, 'anat', sub + '_rec-irtk_dseg.nii.gz')
    
    # Load labelmap image from nifty file
    reader = sitk.ImageFileReader()
    reader.SetFileName(file_dir)
    dseg_sitk = reader.Execute();
    dseg_sitk = sitk.Cast(dseg_sitk, sitk.sitkUInt16)

    # Extract tissue of interest (cortex)
    binarizer = sitk.BinaryThresholdImageFilter()
    binarizer.SetLowerThreshold(2)
    binarizer.SetUpperThreshold(2)
    dseg_sitk = binarizer.Execute(dseg_sitk)

    # Convert sitk image to np array
    dseg = sitk.GetArrayFromImage(dseg_sitk).astype(int)
    

    # Crop array around main region of interest (to reduce computational cost of BN computation)
    nda_ri = skimage.measure.regionprops((dseg > 0).astype(np.uint8), dseg)
    nda_min_0, nda_min_1, nda_min_2, nda_max_0, nda_max_1, nda_max_2 = nda_ri[0].bbox

    min_0 = max(0, nda_min_0 - 2)
    max_0 = min(dseg.shape[0], nda_max_0 + 3)

    min_1 = max(0, nda_min_1 - 2)
    max_1 = min(dseg.shape[1], nda_max_1 + 3)

    min_2 = max(0, nda_min_2 - 2)
    max_2 = min(dseg.shape[2], nda_max_2 + 3)

    dseg = dseg[min_0:max_0, min_1:max_1, min_2:max_2]

    betti_number_list, ec = compute_topological_features(map=dseg, )


    print('0-dimensional Betti number (# of connected components)   : {}'.format(betti_number_list[0]))
    print('1-dimensional Betti number (# of tunnel holes)           : {}'.format(betti_number_list[1]))
    print('2-dimensional Betti number (# of cavity holes)           : {}'.format(betti_number_list[2]))
    print('Euler characteristics                                    : {}'.format(ec))



if __name__ == '__main__':

    main()
