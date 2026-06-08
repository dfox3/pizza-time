from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from dfizza.deps import SessionDep
from dfizza.models.pizza import (
    BulkDough,
    BulkDoughCreate,
    BulkDoughRead,
    DoughBall,
    DoughBallCreate,
    DoughBallRead,
    DoughRecipe,
    DoughRecipeCreate,
    DoughRecipeRead,
    Pizza,
    PizzaCreate,
    PizzaRead,
    PizzaTopping,
    Rating,
    RatingCreate,
    RatingRead,
    Topping,
    ToppingCreate,
    ToppingRead,
)

router = APIRouter()


# --- DoughRecipe ---


@router.post("/dough-recipe", response_model=DoughRecipeRead, status_code=201, tags=["recipe"])
async def create_recipe(payload: DoughRecipeCreate, session: SessionDep) -> DoughRecipe:
    recipe = DoughRecipe.model_validate(payload)
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return recipe


@router.patch("/dough-recipe/{recipe_id}", response_model=DoughRecipeRead, tags=["recipe"])
async def update_recipe(recipe_id: int, payload: DoughRecipeCreate, session: SessionDep) -> DoughRecipe:
    recipe = await session.get(DoughRecipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(recipe, field, value)
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return recipe


@router.get("/dough-recipe/list", response_model=list[DoughRecipeRead], tags=["recipe"])
async def list_recipes(
    session: SessionDep, multiplier: float = Query(1.0, gt=0, description="Scale all gram amounts by this factor"),
) -> list[DoughRecipeRead]:
    result = await session.exec(select(DoughRecipe))
    return [DoughRecipeRead(**r.model_dump(), multiplier=multiplier) for r in result.all()]


@router.get("/dough-recipe/{recipe_id}", response_model=DoughRecipeRead, tags=["recipe"])
async def get_recipe(
    recipe_id: int,
    session: SessionDep,
    multiplier: float = Query(1.0, gt=0, description="Scale all gram amounts by this factor"),
) -> DoughRecipeRead:
    recipe = await session.get(DoughRecipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return DoughRecipeRead(**recipe.model_dump(), multiplier=multiplier)


# --- BulkDough ---


@router.post("/bulk-dough", response_model=BulkDoughRead, status_code=201, tags=["bulk-dough"])
async def create_bulk_dough(payload: BulkDoughCreate, session: SessionDep) -> BulkDough:
    bulk_dough = BulkDough.model_validate(payload)
    session.add(bulk_dough)
    await session.commit()
    await session.refresh(bulk_dough)
    return bulk_dough


@router.get("/bulk-dough/list", response_model=list[BulkDoughRead], tags=["bulk-dough"])
async def list_bulk_doughs(session: SessionDep) -> list[BulkDough]:
    result = await session.exec(select(BulkDough))
    return list(result.all())


@router.get("/bulk-dough/{bulk_dough_id}", response_model=BulkDoughRead, tags=["bulk-dough"])
async def get_bulk_dough(bulk_dough_id: int, session: SessionDep) -> BulkDough:
    bulk_dough = await session.get(BulkDough, bulk_dough_id)
    if not bulk_dough:
        raise HTTPException(status_code=404, detail="Bulk dough not found")
    return bulk_dough


# --- DoughBall ---


@router.post("/dough-ball", response_model=DoughBallRead, status_code=201, tags=["dough-ball"])
async def create_dough_ball(payload: DoughBallCreate, session: SessionDep) -> DoughBall:
    dough_ball = DoughBall.model_validate(payload)
    session.add(dough_ball)
    await session.commit()
    await session.refresh(dough_ball)
    return dough_ball


@router.get("/dough-ball/list", response_model=list[DoughBallRead], tags=["dough-ball"])
async def list_dough_balls(session: SessionDep) -> list[DoughBall]:
    result = await session.exec(select(DoughBall))
    return list(result.all())


@router.get("/dough-ball/{dough_ball_id}", response_model=DoughBallRead, tags=["dough-ball"])
async def get_dough_ball(dough_ball_id: int, session: SessionDep) -> DoughBall:
    dough_ball = await session.get(DoughBall, dough_ball_id)
    if not dough_ball:
        raise HTTPException(status_code=404, detail="Dough ball not found")
    return dough_ball


# --- Topping ---


@router.post("/topping", response_model=ToppingRead, status_code=201, tags=["topping"])
async def create_topping(payload: ToppingCreate, session: SessionDep) -> Topping:
    topping = Topping.model_validate(payload)
    session.add(topping)
    await session.commit()
    await session.refresh(topping)
    return topping


@router.get("/topping/list", response_model=list[ToppingRead], tags=["topping"])
async def list_toppings(session: SessionDep) -> list[Topping]:
    result = await session.exec(select(Topping))
    return list(result.all())


@router.get("/topping/{name}", response_model=ToppingRead, tags=["topping"])
async def get_topping(name: str, session: SessionDep) -> Topping:
    topping = await session.get(Topping, name)
    if not topping:
        raise HTTPException(status_code=404, detail="Topping not found")
    return topping


# --- Pizza ---


@router.post("/pizza", response_model=PizzaRead, status_code=201, tags=["pizza"])
async def create_pizza(payload: PizzaCreate, session: SessionDep) -> PizzaRead:
    pizza = Pizza.model_validate(payload)
    session.add(pizza)
    await session.flush()

    toppings = []
    for topping_name in payload.topping_names:
        topping = await session.get(Topping, topping_name)
        if not topping:
            raise HTTPException(status_code=422, detail=f"Topping '{topping_name}' does not exist")
        session.add(PizzaTopping(pizza_id=pizza.id, topping_name=topping_name))
        toppings.append(topping)

    await session.commit()
    await session.refresh(pizza)
    return PizzaRead(**pizza.model_dump(), toppings=toppings)


@router.get("/pizza/list", response_model=list[PizzaRead], tags=["pizza"])
async def list_pizzas(session: SessionDep) -> list[PizzaRead]:
    pizzas = list((await session.exec(select(Pizza))).all())
    result = []
    for pizza in pizzas:
        topping_links = list((await session.exec(select(PizzaTopping).where(PizzaTopping.pizza_id == pizza.id))).all())
        toppings = [await session.get(Topping, link.topping_name) for link in topping_links]
        result.append(PizzaRead(**pizza.model_dump(), toppings=[t for t in toppings if t]))
    return result


@router.get("/pizza/{pizza_id}", response_model=PizzaRead, tags=["pizza"])
async def get_pizza(pizza_id: int, session: SessionDep) -> PizzaRead:
    pizza = await session.get(Pizza, pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    topping_links = list((await session.exec(select(PizzaTopping).where(PizzaTopping.pizza_id == pizza_id))).all())
    toppings = [await session.get(Topping, link.topping_name) for link in topping_links]
    return PizzaRead(**pizza.model_dump(), toppings=[t for t in toppings if t])


@router.get("/pizza/{pizza_id}/rating/list", response_model=list[RatingRead], tags=["pizza"])
async def list_pizza_ratings(pizza_id: int, session: SessionDep) -> list[Rating]:
    result = await session.exec(select(Rating).where(Rating.pizza_id == pizza_id))
    return list(result.all())


@router.get("/pizza/{pizza_id}/rating/average", response_model=float, tags=["pizza"])


# --- Rating ---


@router.post("/rating", response_model=RatingRead, status_code=201, tags=["rating"])
async def create_rating(payload: RatingCreate, session: SessionDep) -> Rating:
    pizza = await session.get(Pizza, payload.pizza_id)
    if not pizza:
        raise HTTPException(status_code=422, detail=f"Pizza {payload.pizza_id} does not exist")
    rating = Rating.model_validate(payload)
    session.add(rating)
    await session.commit()
    await session.refresh(rating)
    return rating


@router.get("/rating/list", response_model=list[RatingRead], tags=["rating"])
async def list_ratings(session: SessionDep) -> list[Rating]:
    result = await session.exec(select(Rating))
    return list(result.all())


@router.get("/rating/{rating_id}", response_model=RatingRead, tags=["rating"])
async def get_rating(rating_id: int, session: SessionDep) -> Rating:
    rating = await session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating
