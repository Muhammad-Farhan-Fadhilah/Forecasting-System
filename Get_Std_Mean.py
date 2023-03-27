import torchvision
import torch
import torchvision.transforms as transforms


train_dataset_path = r'D:\OneDrive - Hochschule für Technik und Wirtschaft Berlin\Uni\Sem.7\BA\Dataset\RiceDiseaseDataset\train'
test_dataset_path = r'D:\OneDrive - Hochschule für Technik und Wirtschaft Berlin\Uni\Sem.7\BA\Dataset\RiceDiseaseDataset\validation'

mean_std_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

train_dataset = torchvision.datasets.ImageFolder(root = train_dataset_path, transform = mean_std_transforms)
test_dataset = torchvision.datasets.ImageFolder(root = test_dataset_path, transform = mean_std_transforms)

train_loader = torch.utils.data.DataLoader(dataset = train_dataset, batch_size = 6, shuffle = True)
test_loader = torch.utils.data.DataLoader(dataset = test_dataset, batch_size = 6, shuffle = False)

def get_mean_and_std(loader):
    mean = 0.
    std = 0.
    total_images_count = 0
    for images, _ in loader:
        image_count_in_a_batch = images.size(0)
        images = images.view(image_count_in_a_batch, images.size(1), -1)
        mean += images.mean(2).sum(0)
        std += images.std(2).sum(0)
        total_images_count += image_count_in_a_batch
    mean /= total_images_count
    std /= total_images_count
    return mean, std

print(get_mean_and_std(train_loader))
