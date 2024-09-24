from sqlalchemy.orm import Session
from backend import models
from backend.database import SessionLocal

users_to_insert = [
    models.User(
        username="john_doe",
        email="john.doe@company.com",
        password="testpassword",  # TODO: Hash this password when merged with the login feature branch
    ),
    models.User(
        username="jane_doe",
        email="jane.doe@company.com",
        password="testpassword",  # TODO: Hash this password when merged with the login feature branch
    ),
]

item_configs_to_insert = [
    models.ItemConfig(
        triangle_size=220,
        triangle_color="#c3f322",
        circle_size=266,
        circle_color="#0dae61",
        time_visible_ms=4191,
        orientation="N",
    ),
    models.ItemConfig(
        triangle_size=100,
        triangle_color="red",
        circle_size=200,
        circle_color="blue",
        time_visible_ms=10000,
        orientation="S",
    ),
    models.ItemConfig(
        triangle_size=100,
        triangle_color="orange",
        circle_size=200,
        circle_color="blue",
        time_visible_ms=10000,
        orientation="N",
    ),
    models.ItemConfig(
        triangle_size=100,
        triangle_color="yellow",
        circle_size=1000,
        circle_color="green",
        time_visible_ms=4000,
        orientation="W",
    ),
    models.ItemConfig(
        triangle_size=10,
        triangle_color="green",
        circle_size=1000,
        circle_color="blue",
        time_visible_ms=4000,
        orientation="S",
    ),
    models.ItemConfig(
        triangle_size=136,
        triangle_color="#41d27c",
        circle_size=436,
        circle_color="#8601a7",
        time_visible_ms=4912,
        orientation="E",
    ),
    models.ItemConfig(
        triangle_size=220,
        triangle_color="#c3f322",
        circle_size=266,
        circle_color="#0dae61",
        time_visible_ms=4191,
        orientation="N",
    ),
    models.ItemConfig(
        triangle_size=154,
        triangle_color="#dd2677",
        circle_size=377,
        circle_color="#7f0a3e",
        time_visible_ms=660,
        orientation="S",
    ),
]

test_configs_to_insert = [
    models.TestConfig(
        name="easy",
        item_configs=item_configs_to_insert[:6],
    ),
    models.TestConfig(
        name="medium",
        item_configs=item_configs_to_insert[6:8],
    ),
    models.TestConfig(
        name="hard",
        item_configs=item_configs_to_insert[4:6],
    ),
    models.TestConfig(
        name="super-hard",
        item_configs=item_configs_to_insert[4:6],
    ),
    models.TestConfig(
        name="expert",
        item_configs=item_configs_to_insert[4:6],
    ),
    models.TestConfig(
        name="impossible",
        item_configs=item_configs_to_insert[4:6],
    ),
]


# Define your seed data
def seed_data():
    db: Session = SessionLocal()

    # insert the users
    for user in users_to_insert:
        db.add(user)

    # insert the item configs
    for item_config in item_configs_to_insert:
        db.add(item_config)

    # insert the test configs
    for test_config in test_configs_to_insert:
        db.add(test_config)

    db.commit()
    db.close()
