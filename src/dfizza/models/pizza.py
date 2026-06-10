from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import computed_field, model_validator
from sqlalchemy import Column
from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class FlourTypes(StrEnum):
    AP = "AP"
    BREAD = "Bread"
    DOUBLE_ZERO = "00"
    WHOLE_WHEAT = "Whole Wheat"
    OTHER = "Other"


class SaltTypes(StrEnum):
    IODIZED = "Iodized"
    SEA = "Sea"
    KOSHER = "Kosher"
    HIMALAYAN = "Himalayan"
    OTHER = "Other"


class YeastTypes(StrEnum):
    ACTIVE_DRY = "Active Dry"
    INSTANT = "Instant"
    FRESH = "Fresh"
    OTHER = "Other"


class SugarTypes(StrEnum):
    WHITE = "White"
    BROWN = "Brown"
    HONEY = "Honey"
    AGAVE = "Agave"
    RAW = "Raw"
    POWDERED = "Powdered"
    OTHER = "Other"


class OilTypes(StrEnum):
    EVOO = "EVOO"
    UNREFINED_OLIVE_OIL = "Unrefined Olive Oil"
    VEGETABLE_OIL = "Vegetable Oil"
    BUTTER = "Butter"
    OTHER = "Other"


# --- DoughRecipe ---


class DoughRecipeBase(SQLModel):
    name: Optional[str] = Field(default=None, description="Name of the dough recipe")
    flour_type: FlourTypes = Field(
        default=FlourTypes.BREAD,
        sa_column=Column(SqlAlchemyEnum(FlourTypes, values_callable=lambda x: [i.value for i in x]), nullable=False),
        description="Type of flour used in the dough",
    )
    flour_description: Optional[str] = Field(default=None, description="Brand of flour used")
    flour_grams: float = Field(default=500, description="Amount of flour in grams")
    water_description: Optional[str] = Field(default=None, description="Description of the water used, if desired")
    water_grams: float = Field(default=325, description="Amount of water in grams")
    salt_type: SaltTypes = Field(
        default=SaltTypes.IODIZED,
        sa_column=Column(SqlAlchemyEnum(SaltTypes, values_callable=lambda x: [i.value for i in x]), nullable=False),
        description="Type of salt used in the dough",
    )
    salt_description: Optional[str] = Field(
        default=None, description="Additional description of the salt used, if desired"
    )
    salt_grams: float = Field(default=10, description="Amount of salt in grams")
    yeast_type: YeastTypes = Field(
        default=YeastTypes.ACTIVE_DRY,
        sa_column=Column(SqlAlchemyEnum(YeastTypes, values_callable=lambda x: [i.value for i in x]), nullable=False),
        description="Type of yeast used in the dough, if desired",
    )
    yeast_description: Optional[str] = Field(
        default=None, description="Additional description of the yeast used, if desired"
    )
    yeast_grams: float = Field(default=2, description="Amount of yeast in grams")
    sugar_type: Optional[SugarTypes] = Field(
        default=SugarTypes.WHITE,
        sa_column=Column(SqlAlchemyEnum(SugarTypes, values_callable=lambda x: [i.value for i in x]), nullable=False),
        description="Type of sugar used in the dough, if used",
    )
    sugar_description: Optional[str] = Field(
        default=None, description="Additional description of the sugar used, if desired"
    )
    sugar_grams: Optional[float] = Field(default=None, description="Amount of sugar in grams, if used")
    oil_type: Optional[OilTypes] = Field(
        default=OilTypes.EVOO,
        sa_column=Column(SqlAlchemyEnum(OilTypes, values_callable=lambda x: [i.value for i in x]), nullable=False),
        description="Type of oil used in the dough, if used",
    )
    oil_description: Optional[str] = Field(
        default=None, description="Additional description of the oil used, if desired"
    )
    oil_grams: Optional[float] = Field(default=None, description="Amount of oil in grams, if used")
    poolish: Optional[int] = Field(
        foreign_key="doughrecipe.id", default=None, description="ID of the poolish recipe used for this dough, if any"
    )
    notes: Optional[str] = Field(default=None, description="Additional notes about the dough recipe")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the recipe was created")
    parent_id: Optional[int] = Field(
        foreign_key="doughrecipe.id",
        default=None,
        description="ID of the parent recipe if this recipe was derived from another",
    )

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
        return 0.0

    @computed_field
    @property
    def oil_percentage(self) -> Optional[float]:
        if self.oil_grams is not None:
            return round((self.oil_grams / self.flour_grams) * 100, 2)
        return 0.0


class DoughRecipe(DoughRecipeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint(
            "flour_type",
            "flour_description",
            "flour_grams",
            "water_grams",
            "water_description",
            "salt_type",
            "salt_description",
            "salt_grams",
            "yeast_grams",
            "sugar_type",
            "sugar_description",
            "sugar_grams",
            "oil_type",
            "oil_description",
            "oil_grams",
            "poolish",
            "notes",
            name="uq_doughrecipe_ingredients3",
        ),
    )


class DoughRecipeCreate(DoughRecipeBase):
    pass


class DoughRecipeUpdate(SQLModel):
    name: Optional[str] = Field(default=None, description="Name of the dough recipe")
    flour_type: Optional[FlourTypes] = Field(default=None, description="Type of flour used in the dough")
    flour_description: Optional[str] = Field(default=None, description="Brand of flour used")
    flour_grams: Optional[float] = Field(default=None, description="Amount of flour in grams")
    water_description: Optional[str] = Field(default=None, description="Description of the water used, if desired")
    water_grams: Optional[float] = Field(default=None, description="Amount of water in grams")
    salt_type: Optional[SaltTypes] = Field(default=None, description="Type of salt used in the dough")
    salt_description: Optional[str] = Field(
        default=None, description="Additional description of the salt used, if desired"
    )
    salt_grams: Optional[float] = Field(default=None, description="Amount of salt in grams")
    yeast_type: Optional[YeastTypes] = Field(default=None, description="Type of yeast used in the dough, if desired")
    yeast_description: Optional[str] = Field(
        default=None, description="Additional description of the yeast used, if desired"
    )
    yeast_grams: Optional[float] = Field(default=None, description="Amount of yeast in grams")
    sugar_type: Optional[SugarTypes] = Field(default=None, description="Type of sugar used in the dough, if used")
    sugar_description: Optional[str] = Field(
        default=None, description="Additional description of the sugar used, if desired"
    )
    sugar_grams: Optional[float] = Field(default=None, description="Amount of sugar in grams, if used")
    oil_type: Optional[OilTypes] = Field(default=None, description="Type of oil used in the dough, if used")
    oil_description: Optional[str] = Field(
        default=None, description="Additional description of the oil used, if desired"
    )
    oil_grams: Optional[float] = Field(default=None, description="Amount of oil in grams, if used")
    poolish: Optional[int] = Field(
        foreign_key="doughrecipe.id", default=None, description="ID of the poolish recipe used for this dough, if any"
    )
    notes: Optional[str] = Field(default=None, description="Additional notes about the dough recipe")


class DoughRecipeRead(DoughRecipeBase):
    id: int
    multiplier: float = Field(default=1.0, exclude=True, description="Scale factor applied to gram amounts")
    target_diameter: Optional[float] = Field(
        default=None, exclude=True, description="Diameter to scale to when multiplier is applied"
    )
    ball_weight: float = 0.0
    original_ball_weight: float = 0.0
    diameter: float = 0.0

    def get_diameter(self, ball_weight: float = 250) -> Optional[float]:
        """Estimate the diameter of a pizza that can be made from this dough recipe."""
        target_dough_ball_weight = 250
        num_dough_balls = ball_weight / target_dough_ball_weight
        base_diameter = 12
        estimated_diameter = base_diameter * (num_dough_balls ** 0.5)
        return round(estimated_diameter, 2)

    def multiplier_for_diameter(self, target_diameter: float) -> float:
        """Return the multiplier needed to scale this recipe to produce a pizza of target_diameter inches."""
        current_ball_weight = self.flour_grams + self.water_grams + self.salt_grams + self.yeast_grams
        if self.sugar_grams:
            current_ball_weight += self.sugar_grams
        if self.oil_grams:
            current_ball_weight += self.oil_grams
        target_ball_weight = 250 * (target_diameter / 12) ** 2
        return target_ball_weight / current_ball_weight if current_ball_weight else 1.0

    @model_validator(mode="after")
    def apply_multiplier(self) -> "DoughRecipeRead":
        print(self.name)
        print(self.original_ball_weight)
        self.original_ball_weight = self.flour_grams + self.water_grams + self.salt_grams + self.yeast_grams
        if self.sugar_grams:
            self.original_ball_weight += self.sugar_grams
        if self.oil_grams:
            self.original_ball_weight += self.oil_grams

        if self.target_diameter is not None:
            multiplier = self.multiplier_for_diameter(self.target_diameter)
            self.diameter = self.target_diameter
            self.original_ball_weight = self.original_ball_weight * multiplier
            self.flour_grams *= multiplier
            self.water_grams *= multiplier
            self.salt_grams *= multiplier
            self.yeast_grams *= multiplier
            if self.sugar_grams is not None:
                self.sugar_grams *= multiplier
            if self.oil_grams is not None:
                self.oil_grams *= multiplier
            print(f"if target_diameter: {self.original_ball_weight}")

        print(self.original_ball_weight)
        if self.multiplier != 1.0:
            # Snapshot original ball_weight before scaling
            # self.ball_weight = self.original_ball_weight
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

            print(f"if multiplier: {self.original_ball_weight}")
        self.ball_weight = self.original_ball_weight
        self.diameter = self.get_diameter(ball_weight=self.ball_weight)
        print(self.original_ball_weight)
        self.sigfig_values()
        return self

    def sigfig_values(self, sigfig: int = 2) -> "DoughRecipeRead":
        """Return a copy of this recipe with all gram amounts rounded to significant figures for display purposes."""
        self.flour_grams = round(self.flour_grams, sigfig)
        self.water_grams = round(self.water_grams, sigfig)
        self.salt_grams = round(self.salt_grams, sigfig)
        self.yeast_grams = round(self.yeast_grams, sigfig)
        if self.sugar_grams is not None:
            self.sugar_grams = round(self.sugar_grams, sigfig)
        if self.oil_grams is not None:
            self.oil_grams = round(self.oil_grams, sigfig)
        self.ball_weight = round(self.ball_weight, sigfig)
        self.diameter = round(self.diameter, sigfig)


class IngredientsBase(SQLModel):
    ingredient: str = Field(description="Name of the ingredient")
    type: Optional[str] = None
    description: Optional[str] = None
    grams: Optional[float] = None


class DoughRecipeIngredientsRead(SQLModel):
    ingredients: list[IngredientsBase] = Field(description="List of ingredients with details")


class DoughRecipePercentagesRead(SQLModel):
    hydration: float = 0.0
    salt_percentage: float = 0.0
    yeast_percentage: float = 0.0
    sugar_percentage: float = 0.0
    oil_percentage: float = 0.0


class DoughRecipeBasicDetailsRead(SQLModel):
    id: int
    name: Optional[str] = Field(default=None, description="Name of the dough recipe")
    notes: Optional[str] = Field(default=None, description="Additional notes about the dough recipe")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the recipe was created")
    parent_id: Optional[int] = Field(
        foreign_key="doughrecipe.id",
        default=None,
        description="ID of the parent recipe if this recipe was derived from another",
    )
    diameter: float = 0.0
    ball_weight: float = 0.0
    num_dough_balls: float = 0.0


class DoughRecipeDetailsRead(SQLModel):
    basic_details: DoughRecipeBasicDetailsRead = Field(description="Basic details about the recipe")
    ingredients: list[IngredientsBase] = Field(description="List of ingredients with details")
    percentages: DoughRecipePercentagesRead = Field(description="Baker's percentages for the recipe")


def convert_to_ingredients(recipe: DoughRecipeRead) -> DoughRecipeIngredientsRead:
    return DoughRecipeIngredientsRead(
        ingredients=[
            IngredientsBase(
                ingredient="Flour",
                type=recipe.flour_type,
                description=recipe.flour_description,
                grams=recipe.flour_grams,
            ),
            IngredientsBase(ingredient="Water", description=recipe.water_description, grams=recipe.water_grams,),
            IngredientsBase(
                ingredient="Salt", type=recipe.salt_type, description=recipe.salt_description, grams=recipe.salt_grams,
            ),
            IngredientsBase(
                ingredient="Yeast",
                type=recipe.yeast_type,
                description=recipe.yeast_description,
                grams=recipe.yeast_grams,
            ),
            IngredientsBase(
                ingredient="Sugar",
                type=recipe.sugar_type,
                description=recipe.sugar_description,
                grams=recipe.sugar_grams,
            )
            if recipe.sugar_grams is not None
            else None,
            IngredientsBase(
                ingredient="Oil", type=recipe.oil_type, description=recipe.oil_description, grams=recipe.oil_grams,
            )
            if recipe.oil_grams is not None
            else None,
        ]
    )


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
