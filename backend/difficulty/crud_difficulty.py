from sqlalchemy import func
from sqlalchemy.orm import Session
import random
from typing import List

from backend import models, schemas


def calculate_luminance(color_hex):
    """Calculate the relative luminance of a color given in hex format."""
    color_hex = color_hex.lstrip("#")
    r, g, b = tuple(int(color_hex[i : i + 2], 16) for i in (0, 2, 4))

    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    R, G, B = linearize(r), linearize(g), linearize(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(l1, l2):
    """Calculate the contrast ratio between two luminance values."""
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def generate_color_pair_with_contrast(contrast_min, contrast_max):
    """Generate a pair of colors with a contrast ratio within the specified range."""
    max_attempts = 1000
    for _ in range(max_attempts):
        # Generate two random colors
        color1 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        color2 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        # Calculate luminance
        l1 = calculate_luminance(color1)
        l2 = calculate_luminance(color2)
        cr = contrast_ratio(l1, l2)
        if contrast_min <= cr <= contrast_max:
            return color1, color2
    raise Exception(
        f"Could not find color pair with contrast between {contrast_min} and {contrast_max}"
    )


def generate_item_config(difficulty: str) -> schemas.ItemConfig:
    """Generate an ItemConfig with parameters based on the difficulty level."""
    difficulty_ranges = {
        "easy": {
            "contrast_min": 1.08,
            "contrast_max": 1.11,
            "triangle_size_min": 50,
            "triangle_size_max": 100,
            "time_visible_min": 300,
            "time_visible_max": 500,
        },
        "medium": {
            "contrast_min": 1.05,
            "contrast_max": 1.07,
            "triangle_size_min": 30,
            "triangle_size_max": 70,
            "time_visible_min": 150,
            "time_visible_max": 300,
        },
        "hard": {
            "contrast_min": 1.03,
            "contrast_max": 1.05,
            "triangle_size_min": 8,
            "triangle_size_max": 15,
            "time_visible_min": 50,
            "time_visible_max": 100,
        },
    }
    if difficulty not in difficulty_ranges:
        raise ValueError(f"Unknown difficulty level: {difficulty}")
    ranges = difficulty_ranges[difficulty]

    # Generate triangle size
    triangle_size = random.randint(
        ranges["triangle_size_min"], ranges["triangle_size_max"]
    )
    # Generate time_visible_ms
    time_visible_ms = random.randint(
        ranges["time_visible_min"], ranges["time_visible_max"]
    )
    # Generate circle size between 300 and 600
    circle_size = random.randint(300, 600)
    # Generate colors with desired contrast ratio
    color1, color2 = generate_color_pair_with_contrast(
        ranges["contrast_min"], ranges["contrast_max"]
    )
    # Randomly assign triangle_color and circle_color
    if random.choice([True, False]):
        triangle_color = color1
        circle_color = color2
    else:
        triangle_color = color2
        circle_color = color1
    # Random orientation
    orientation = random.choice(["N", "E", "S", "W"])
    # Create ItemConfig schema object
    item_config = schemas.ItemConfig(
        triangle_size=triangle_size,
        triangle_color=triangle_color,
        circle_size=circle_size,
        circle_color=circle_color,
        time_visible_ms=time_visible_ms,
        orientation=orientation,
    )
    return item_config


def get_test_config_id_by_difficulty(difficulty: str):
    """Map difficulty levels to their corresponding TestConfig IDs."""
    mapping = {"easy": 1, "medium": 3, "hard": 4}
    return mapping.get(difficulty)


def get_item_config_count(db: Session, difficulty: str) -> int:
    """Get the count of ItemConfigs associated with a difficulty level."""
    test_config_id = get_test_config_id_by_difficulty(difficulty)
    count = (
        db.query(models.ItemConfig)
        .join(models.ItemConfig.test_configs)
        .filter(models.TestConfig.id == test_config_id)
        .count()
    )
    return count


def fill_item_configs(db: Session, target_count: int = 10_000):
    """Ensure there are at least `target_count` item configs for each difficulty level in the database,
    and make sure the required TestConfig entries are present."""
    difficulties = ["easy", "medium", "hard"]
    test_config_mapping = {"easy": 1, "medium": 3, "hard": 4}

    for difficulty in difficulties:
        current_count = get_item_config_count(db, difficulty)

        # Ensure TestConfig is present in the database
        test_config_id = test_config_mapping[difficulty]
        test_config = (
            db.query(models.TestConfig)
            .filter(models.TestConfig.id == test_config_id)
            .first()
        )

        # If the TestConfig entry is missing, create it
        if not test_config:
            test_config = models.TestConfig(
                id=test_config_id, name=f"{difficulty.capitalize()} TestConfig"
            )
            db.add(test_config)
            db.commit()

        # If current count is less than the target, add new ItemConfigs
        if current_count < target_count:
            items_to_create = target_count - current_count
            for _ in range(items_to_create):
                item_config_schema = generate_item_config(difficulty)
                # Convert schema to model
                item_config = models.ItemConfig(**item_config_schema.model_dump())
                db.add(item_config)
                # Associate item_config with test_config
                test_config.item_configs.append(item_config)
            db.commit()


def get_item_configs_by_difficulty(
    db: Session, difficulty: str, limit: int = 10
) -> List[models.ItemConfig]:
    """Retrieve a list of random ItemConfigs for a given difficulty level, generating more if needed."""
    # Get the current count of item configs for the given difficulty
    current_count = get_item_config_count(db, difficulty)

    # If there are not enough item configs, fill them up to ensure we have at least the requested limit
    if current_count < limit:
        fill_item_configs(db, target_count=limit)

    # Retrieve item configs after ensuring we have enough
    test_config_id = get_test_config_id_by_difficulty(difficulty)
    item_configs = (
        db.query(models.ItemConfig)
        .join(models.ItemConfig.test_configs)
        .filter(models.TestConfig.id == test_config_id)
        .order_by(func.random())  # Order by random
        .limit(limit)
        .all()
    )
    return item_configs
