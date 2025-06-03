import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error


# Load the saved model
loaded_model = tf.keras.models.load_model('/home/dblab/seong_space2/0002_move_3d/data/train_output/1125/model/0001_01_train.keras') # 200 4fclayer
npfolder = '/home/dblab/seong_space2/0002_move_3d/data/npy/1125/'
# Load your test data (adjust the paths accordingly)
test_3d_head = np.load(f'{npfolder}test_3d_head.npy')
test_bboxes = np.load(f'{npfolder}test_bboxes.npy')
test_types = np.load(f'{npfolder}test_types.npy')

# Assuming you have test data for 3D centers and dimensions as well
test_3d_centers = np.load(npfolder + 'test_3d_centers.npy')
test_3d_dims = np.load(npfolder + 'test_3d_dims.npy')
# test_3d_head = np.load(npfolder + 'test_3d_head.npy')

# Perform predictions on the test data
predictions = loaded_model.predict([test_3d_head, test_bboxes, test_types])
true_labels = [test_3d_centers, test_3d_dims]


# Assuming you want to predict both 3D centers and dimensions
predicted_3d_centers = predictions[0]
print(predicted_3d_centers.shape)
predicted_3d_dims = predictions[1]
print(predicted_3d_dims.shape)
# predicted_3d_head = predictions[2]
# print(predicted_3d_head.shape)
true_labels_3d_centers = true_labels[0]
true_labels_3d_dims = true_labels[1]

predicted_3d_centers_mse = mean_squared_error(true_labels_3d_centers, predicted_3d_centers)
predicted_3d_centers_mae = mean_absolute_error(true_labels_3d_centers, predicted_3d_centers)
print(f'predicted_3d_centers_MSE: {predicted_3d_centers_mse}, predicted_3d_centers_MAE: {predicted_3d_centers_mae}')

predicted_3d_dims_mse = mean_squared_error(true_labels_3d_dims, predicted_3d_dims)
predicted_3d_dims_mae = mean_absolute_error(true_labels_3d_dims, predicted_3d_dims)
print(f'predicted_3d_dims_MSE: {predicted_3d_dims_mse}, predicted_3d_dims_MAE: {predicted_3d_dims_mae}')


np.save('/home/dblab/seong_space2/0002_move_3d/data/train_output/1125/testnpy/predicted_3d_centers_0001_01_train.npy', predicted_3d_centers)
np.save('/home/dblab/seong_space2/0002_move_3d/data/train_output/1125/testnpy/predicted_3d_dims_0001_01_train.npy', predicted_3d_dims)
# np.save('/home/dblab/seong_space2/0002_move_3d/data/train_output/1125/testnpy/predicted_3d_head_0001_06_train.npy', predicted_3d_head)