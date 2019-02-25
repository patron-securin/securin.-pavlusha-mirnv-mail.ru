from PIL import Image as PIL_Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.models as models
from fastai.vision import load_learner, Image


class ClassPredictor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = load_learner("../model/tmp.pth")
        self.to_tensor = transforms.ToTensor()

    def predict(self, img_stream):
        
        return self.model.predict(self.process_image(img_stream))[0]

    
    def process_image(self, img_stream):
        image = PIL_Image.open(img_stream).resize((256, 256))
        image = Image(self.to_tensor(image))
        return image
