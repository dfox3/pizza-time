from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import computed_field, model_validator
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class FlourTypes(StrEnum):
    AP = "AP"
    BREAD = "Bread"
    DOUBLE_ZERO = "00"
    WHOLE_WHEAT = "Whole Wheat"


# --- DoughRecipe ---


class DoughRecipeBase(SQLModel):
    name: Optional[str] = Field(default=None, description="Name of the dough recipe")
    flour_type: str = Field(default=FlourTypes.AP, description="Type of flour used in the dough")
    flour_brand: Optional[str] = Field(default=None, description="Brand of flour used")
    flour_grams: float = Field(default=500, description="Amount of flour in grams")
    water_grams: float = Field(default=325, description="Amount of water in grams")
    salt_grams: float = Field(default=10, description="Amount of salt in grams")
    yeast_grams: float = Field(default=2, description="Amount of yeast in grams")
    sugar_grams: Optional[float] = Field(default=None, description="Amount of sugar in grams, if used")
    oil_grams: Optional[float] = Field(default=None, description="Amount of oil in grams, if used")

    @computed_field
    @property
    def hydration(self) -> float:
        return round((self.water_grams / self.flour_grams) * 100, 2)

    @computed_field
    @property
    def salt_percentage(self) -> float:
        return round((self.salt_grams / self.flour_grams) * 100, 2)

    @computed_field
    @property
    def yeast_percentage(self) -> float:
        return round((self.yeast_grams / self.flour_grams) * 100, 2)

    @computed_field
    @property
    def sugar_percentage(self) -> Optional[float]:
        if self.sugar_grams is not None:
            return round((self.sugar_grams / self.flour_grams) * 100, 2)
        return None

    @computed_field
    @property
    def oil_percentage(self) -> Optional[float]:
        if self.oil_grams is not None:
            return round((self.oil_grams / self.flour_grams) * 100, 2)
        return None


class DoughRecipe(DoughRecipeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint(
            "flour_type",
            "flour_brand",
            "flour_grams",
            "water_grams",
            "salt_grams",
            "yeast_grams",
            "sugar_grams",
            "oil_grams",
            name="uq_doughrecipe_ingredients",
        ),
    )


class DoughRecipeCreate(DoughRecipeBase):
    pass


class DoughRecipeRead(DoughRecipeBase):
    id: int
    multiplier: float = Field(default=1.0, exclude=True, description="Scale factor applied to gram amounts")
    ball_weight: float = 0.0
    diameter: float = 0.0

    def get_diameter(self, ball_weight: float = 250) -> Optional[float]:
        """Estimate the diameter of a pizza that can be made from this dough recipe."""
        target_dough_ball_weight = 250
        num_dough_balls = ball_weight / target_dough_ball_weight
        base_diameter = 12
        estimated_diameter = base_diameter * (num_dough_balls ** 0.5)
        return round(estimated_diameter, 2)

    @model_validator(mode="after")
    def apply_multiplier(self) -> "DoughRecipeRead":
        if self.multiplier != 1.0:
            # Snapshot original ball_weight before scaling
            self.ball_weight = (
                self.flour_grams
                + self.water_grams
                + self.salt_grams
                + self.yeast_grams
                + (self.sugar_grams or 0)
                + (self.oil_grams or 0)
            )
            self.diameter = self.get_diameter(ball_weight=self.ball_weight)
            self.flour_grams *= self.multiplier
            self.water_grams *= self.multiplier
            self.salt_grams *= self.multiplier
            self.yeast_grams *= self.multiplier
            if self.sugar_grams is not None:
                self.sugar_grams *= self.multiplier
            if self.oil_grams is not None:
                self.oil_grams *= self.multiplier
            # Reset so FastAPI's re-validation pass is a no-op
            self.multiplier = 1.0
        elif self.ball_weight == 0.0:
            # First validation with no scaling: still need to set ball_weight
            self.ball_weight = (
                self.flour_grams
                + self.water_grams
                + self.salt_grams
                + self.yeast_grams
                + (self.sugar_grams or 0)
                + (self.oil_grams or 0)
            )
            self.diameter = self.get_diameter(ball_weight=self.ball_weight)
        return self


# --- BulkDough ---


class BulkDoughBase(SQLModel):
    recipe_id: int = Field(foreign_key="doughrecipe.id", description="ID of the dough recipe used")
    date_made: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None, description="Additional notes about the dough")


class BulkDough(BulkDoughBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BulkDoughCreate(BulkDoughBase):
    pass


class BulkDoughRead(BulkDoughBase):
    id: int


# --- DoughBall ---


class DoughBallBase(SQLModel):
    bulk_dough_id: int = Field(
        foreign_key="bulkdough.id", description="ID of the bulk dough this ball came from",
    )
    weight_grams: int = Field(default=250, description="Weight of the dough ball in grams")
    cold_fermentation: bool = Field(
        default=True, description="Whether the dough ball is undergoing cold fermentation",
    )
    fermentation_time: Optional[int] = Field(default=None, description="Fermentation time in hours, if known")
    proof_time: Optional[int] = Field(default=None, description="Proofing time in hours, if known")
    notes: Optional[str] = Field(default=None, description="Additional notes about the dough ball")


class DoughBall(DoughBallBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class DoughBallCreate(DoughBallBase):
    pass


class DoughBallRead(DoughBallBase):
    id: int


# --- Topping ---


class ToppingBase(SQLModel):
    description: Optional[str] = Field(default=None, description="Description of the topping")


class Topping(ToppingBase, table=True):
    name: str = Field(description="Name of the topping", primary_key=True)


class ToppingCreate(ToppingBase):
    name: str


class ToppingRead(ToppingBase):
    name: str


# --- Pizza / PizzaTopping link table ---


class PizzaTopping(SQLModel, table=True):
    """Link table for the many-to-many relationship between Pizza and Topping."""

    pizza_id: int = Field(foreign_key="pizza.id", primary_key=True)
    topping_name: str = Field(foreign_key="topping.name", primary_key=True)


class PizzaBase(SQLModel):
    name: Optional[str] = Field(default=None, description="Name of the pizza")
    dough_ball_id: int = Field(
        foreign_key="doughball.id", description="ID of the dough ball used for this pizza",
    )
    bake_time_seconds: Optional[int] = Field(default=None, description="Bake time in seconds, if known")
    bake_temperature_celsius: Optional[int] = Field(default=None, description="Bake temperature in Celsius, if known")
    date_baked: Optional[datetime] = Field(default=None, description="Date and time when the pizza was baked")
    notes: Optional[str] = Field(default=None, description="Additional notes about the pizza")


class Pizza(PizzaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    toppings: list[Topping] = Relationship(link_model=PizzaTopping)


class PizzaCreate(PizzaBase):
    topping_names: list[str] = Field(default_factory=list, description="Names of toppings to add")


class PizzaRead(PizzaBase):
    id: int
    toppings: list[ToppingRead] = []


# --- Rating ---


class RatingBase(SQLModel):
    pizza_id: int = Field(foreign_key="pizza.id", description="ID of the pizza being rated")
    score: float = Field(default=5.0, ge=0.0, le=10.0, description="Rating score from 0 to 10")
    comment: Optional[str] = Field(default=None, description="Additional comments about the pizza")
    date_rated: datetime = Field(default_factory=datetime.utcnow)


class Rating(RatingBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class RatingCreate(RatingBase):
    pass


class RatingRead(RatingBase):
    id: int
