import face_alignment
from skimage import io

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False,device='cpu')

input = io.imread('frame0523.jpg')
preds = fa.get_landmarks(input)
print(preds)