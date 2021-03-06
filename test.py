import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

model_path = 'dataset/ESRGAN.pth'#ESRGAN DATASET

device = torch.device('cpu')#Device used for trainning

test_img_folder = 'lowres/*'#lowres image folder

model = arch.RRDBNet(3, 3, 64, 23, gc=32)#RRDBNet Module Parameter
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)
print('Prepairing DataSet for Trainning ')
idx = 0
for path in glob.glob(test_img_folder):
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)
    # read images
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite('highres/{:s}_highres1.png'.format(base), output)
