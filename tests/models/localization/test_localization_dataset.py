from torch.utils.data import DataLoader

from comic_ocr.dataset import generated_manga
from comic_ocr.models.localization.localization_dataset import LocalizationDataset
from comic_ocr.typing import Size
from comic_ocr.utils.files import get_path_example_dir


def test_load_line_annotated_manga_dataset():
    dataset_dir = get_path_example_dir('manga_annotated')
    dataset = LocalizationDataset.load_line_annotated_manga_dataset(dataset_dir, image_size=Size.of(400, 500))
    assert len(dataset) == 24
    assert dataset.get_image(0).size == (400, 500)
    assert dataset.get_mask_char(0).size == (400, 500)
    assert dataset.get_mask_line(0).size == (400, 500)
    assert len(dataset.get_line_locations(0)) > 0

    train_dataloader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=1)
    batch = next(iter(train_dataloader))

    assert batch['input'].shape == (2, 3, 500, 400)
    assert batch['output_mask_line'].shape == (2, 500, 400)
    assert batch['output_mask_char'].shape == (2, 500, 400)


def test_load_generated_manga_dataset():
    dataset_dir = get_path_example_dir('manga_generated')
    dataset = LocalizationDataset.load_generated_manga_dataset(dataset_dir, image_size=Size.of(500, 500))
    assert len(dataset) == 12

    train_dataloader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=1)
    batch = next(iter(train_dataloader))

    assert batch['input'].shape == (2, 3, 500, 500)
    assert batch['output_mask_char'].shape == (2, 500, 500)
    assert batch['output_mask_line'].shape == (2, 500, 500)
    assert batch['output_mask_paragraph'].shape == (2, 500, 500)


def test_load_generated_manga_dataset_with_resize(tmpdir):
    dataset_dir = tmpdir.join('dataset')
    generated_manga.create_dataset(dataset_dir, output_count=5, output_size=Size.of(500, 500))

    dataset = LocalizationDataset.load_generated_manga_dataset(dataset_dir, image_size=Size.of(200, 200))
    dataset = dataset.shuffle()
    assert len(dataset) > 0

    train_dataloader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=1)
    batch = next(iter(train_dataloader))

    assert batch['input'].shape == (2, 3, 200, 200)
    assert batch['output_mask_char'].shape == (2, 200, 200)
    assert batch['output_mask_line'].shape == (2, 200, 200)
    assert batch['output_mask_paragraph'].shape == (2, 200, 200)


def test_merge_annotated_generated_dataset():
    dataset_annotated = LocalizationDataset.load_line_annotated_manga_dataset(
        get_path_example_dir('manga_annotated'), image_size=Size.of(500, 500))

    dataset_generated = LocalizationDataset.load_line_annotated_manga_dataset(
        get_path_example_dir('manga_annotated'), image_size=Size.of(500, 500))

    dataset = LocalizationDataset.merge(dataset_generated, dataset_annotated)
    dataset = dataset.shuffle()
    assert len(dataset) > 0
    assert len(dataset) == len(dataset_generated) + len(dataset_annotated)

    train_dataloader = DataLoader(dataset, batch_size=2, shuffle=True, num_workers=1)
    batch = next(iter(train_dataloader))

    assert 'output_mask_paragraph' not in batch
    assert batch['input'].shape == (2, 3, 500, 500)
    assert batch['output_mask_line'].shape == (2, 500, 500)
    assert batch['output_mask_char'].shape == (2, 500, 500)
