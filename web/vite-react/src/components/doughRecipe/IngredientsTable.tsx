import type { IngredientDetails } from "../../schemas/doughRecipe";

export function IngredientsTable({ items }: { items: IngredientDetails[] }) {
  return (
    <div>
      <table>
        <caption>Dough Ingredients</caption>
        <thead>
          <tr>
            <th>Name</th>
            <th>Grams</th>
            <th>Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, idx) => (
            <tr key={idx}>
              <td>{item.ingredient}</td>
              <td>{item.grams?.toFixed(1) ?? "-"}</td>
              <td>{item.type ?? "-"}</td>
              <td>{item.description ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function EditableIngredientsTable({
  items,
}: {
  items: IngredientDetails[];
}) {
  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Grams</th>
            <th>Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, idx) => (
            <tr key={idx}>
              <td>{item.ingredient}</td>
              <td>
                <input type="number" value={item.grams?.toFixed(1) ?? ""} />
              </td>
              <td>
                <input type="text" value={item.type ?? ""} />
              </td>
              <td>
                <input type="text" value={item.description ?? ""} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
