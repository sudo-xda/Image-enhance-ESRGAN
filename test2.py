import os.path as ospath
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

model_path = 'dataset/ESRGAN.pth'#ESRGAN DATASET
device = torch.device('cpu')
test_img_folder = 'lowres/*'
model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)
idx = 0
for path in glob.glob(test_img_folder):
    idx += 1
    base = ospath.splitext(ospath.basename(path))[0]
    print(idx, base)
    # read images
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    output1 = cv2.filter2D(img, -1, sharpen_kernel)
    output1==img
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    
    cv2.imwrite('highres/{:s}_upsamp2.png'.format(base), output)
