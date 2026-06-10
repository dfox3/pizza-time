from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import select

from dfizza.deps import SessionDep
from dfizza.models.pizza import DoughRecipe, DoughRecipeRead

router = APIRouter(prefix="/ui")


def _recipe_row(r: DoughRecipeRead) -> str:
    sugar = f"{r.sugar_grams:.1f}" if r.sugar_grams is not None else "—"
    oil = f"{r.oil_grams:.1f}" if r.oil_grams is not None else "—"
    return f"""<tr id="recipe-row-{r.id}">
  <td>{r.id}</td>
  <td>{r.name or "—"}</td>
  <td>{r.flour_type}</td>
  <td>{r.flour_brand or "—"}</td>
  <td>{r.flour_grams:.1f}</td>
  <td>{r.water_grams:.1f}</td>
  <td>{r.salt_grams:.1f}</td>
  <td>{r.yeast_grams:.1f}</td>
  <td>{sugar}</td>
  <td>{oil}</td>
  <td>{r.ball_weight:.1f}</td>
  <td>{r.hydration:.1f}%</td>
  <td>{r.diameter:.1f} cm</td>
  <td>
    <button hx-get="/ui/dough-recipe/{r.id}/edit-form"
            hx-target="#recipe-row-{r.id}"
            hx-swap="outerHTML">Edit</button>
  </td>
</tr>"""


@router.get("/dough-recipe/rows", response_class=HTMLResponse)
async def recipe_rows(session: SessionDep, multiplier: float = 1.0):
    result = await session.exec(select(DoughRecipe))
    rows = "".join(_recipe_row(DoughRecipeRead(**r.model_dump(), multiplier=multiplier)) for r in result.all())
    return HTMLResponse(rows or '<tr><td colspan="13">No recipes yet.</td></tr>')


@router.get("/dough-recipe/{recipe_id}/row", response_class=HTMLResponse)
async def recipe_row(recipe_id: int, session: SessionDep):
    recipe = await session.get(DoughRecipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return HTMLResponse(_recipe_row(DoughRecipeRead.model_validate(recipe)))


@router.get("/dough-recipe/{recipe_id}/edit-form", response_class=HTMLResponse)
async def recipe_edit_form(recipe_id: int, session: SessionDep):
    recipe = await session.get(DoughRecipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    r = recipe

    def opt(val, label):
        sel = "selected" if r.flour_type == val else ""
        return f'<option value="{val}" {sel}>{label}</option>'

    flour_opts = (
        opt("AP", "AP") + opt("Bread", "Bread") + opt("00", "00 (Double Zero)") + opt("Whole Wheat", "Whole Wheat")
    )
    return HTMLResponse(
        f"""<tr id="recipe-row-{r.id}">
  <form hx-patch="/ui/dough-recipe/{r.id}"
        hx-target="#recipe-row-{r.id}"
        hx-swap="outerHTML">
  <td>{r.id}</td>
  <td><input name="name" value="{r.name or ""}" placeholder="Name" size="10"></td>
  <td><select name="flour_type">{flour_opts}</select></td>
  <td><input name="flour_brand" value="{r.flour_brand or ""}" placeholder="Brand" size="8"></td>
  <td><input name="flour_grams" type="number" step="0.1" value="{r.flour_grams}" size="5"></td>
  <td><input name="water_grams" type="number" step="0.1" value="{r.water_grams}" size="5"></td>
  <td><input name="salt_grams" type="number" step="0.1" value="{r.salt_grams}" size="4"></td>
  <td><input name="yeast_grams" type="number" step="0.1" value="{r.yeast_grams}" size="4"></td>
  <td><input name="sugar_grams" type="number" step="0.1" value="{r.sugar_grams or ""}" size="4"></td>
  <td><input name="oil_grams" type="number" step="0.1" value="{r.oil_grams or ""}" size="4"></td>
  <td colspan="2"></td>
  <td>
    <button type="submit">Save</button>
    <button type="button"
            hx-get="/ui/dough-recipe/{r.id}/row"
            hx-target="#recipe-row-{r.id}"
            hx-swap="outerHTML">Cancel</button>
  </td>
  </form>
</tr>"""
    )


@router.post("/dough-recipe", response_class=HTMLResponse, status_code=201)
async def create_recipe_ui(
    session: SessionDep,
    name: str = Form(default=""),
    flour_type: str = Form(default="AP"),
    flour_brand: str = Form(default=""),
    flour_grams: float = Form(default=500),
    water_grams: float = Form(default=325),
    salt_grams: float = Form(default=10),
    yeast_grams: float = Form(default=2),
    sugar_grams: str = Form(default=""),
    oil_grams: str = Form(default=""),
):
    recipe = DoughRecipe(
        name=name or None,
        flour_type=flour_type,
        flour_brand=flour_brand or None,
        flour_grams=flour_grams,
        water_grams=water_grams,
        salt_grams=salt_grams,
        yeast_grams=yeast_grams,
        sugar_grams=float(sugar_grams) if sugar_grams else None,
        oil_grams=float(oil_grams) if oil_grams else None,
    )
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return HTMLResponse(_recipe_row(DoughRecipeRead.model_validate(recipe)), status_code=201)


@router.patch("/dough-recipe/{recipe_id}", response_class=HTMLResponse)
async def update_recipe_ui(
    recipe_id: int,
    session: SessionDep,
    name: str = Form(default=""),
    flour_type: str = Form(default="AP"),
    flour_brand: str = Form(default=""),
    flour_grams: float = Form(default=500),
    water_grams: float = Form(default=325),
    salt_grams: float = Form(default=10),
    yeast_grams: float = Form(default=2),
    sugar_grams: str = Form(default=""),
    oil_grams: str = Form(default=""),
):
    recipe = await session.get(DoughRecipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.name = name or None
    recipe.flour_type = flour_type
    recipe.flour_brand = flour_brand or None
    recipe.flour_grams = flour_grams
    recipe.water_grams = water_grams
    recipe.salt_grams = salt_grams
    recipe.yeast_grams = yeast_grams
    recipe.sugar_grams = float(sugar_grams) if sugar_grams else None
    recipe.oil_grams = float(oil_grams) if oil_grams else None
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return HTMLResponse(_recipe_row(DoughRecipeRead.model_validate(recipe)))
