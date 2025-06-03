import numpy as np

# cropimg = np.load("/home/dblab/seong_space2/0000_car_bottom/bmb_bottom_lab/bmb_bottom/0003_npy/merged_bbox_images.npy")
bbox = np.load("/home/dblab/seong_space2/0002_move_3d/data/npy/1125/train_bboxes.npy")
type = np.load("/home/dblab/seong_space2/0002_move_3d/data/npy/1125/train_types.npy")
type2 = np.load("/home/dblab/seong_space2/0001_stop_3d/data/npy/1125/train_types.npy")
centers = np.load("/home/dblab/seong_space2/0002_move_3d/data/npy/1125/train_3d_centers.npy")
dims = np.load("/home/dblab/seong_space2/0002_move_3d/data/npy/1125/train_3d_dims.npy")
heading = np.load("/home/dblab/seong_space2/0002_move_3d/data/npy/1125/train_3d_head.npy")
test_3d_dims = np.load("/home/dblab/seong_space2/0002_move_3d/data/train_output/1125/testnpy/predicted_3d_dims_0001_01_train.npy")


# print(cropimg.shape)
# print(bbox.shape)
# print(type.shape)
# print(type2.shape)
# print(heading.shape)
# print(type.dtype)
# print(centers.shape)
# print(dims.shape)

# (179, 224, 224, 3)
# (179, 4)
# (179, 1)

# print(type[0])
# print(type2[0])
print(round(test_3d_dims[0][0],2))