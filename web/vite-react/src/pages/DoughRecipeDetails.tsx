import type {
  DoughPercentageDetails,
  IngredientDetails,
} from "../schemas/doughRecipe";
import type { DoughRecipeDetails } from "../schemas/doughRecipe";
import { useCallback, useEffect, useState } from "react";
import { IngredientsTable } from "../components/doughRecipe/IngredientsTable";
import { PercentagesTable } from "../components/doughRecipe/PercentagesTable";
import { Link } from "react-router";

// interface DoughRecipeDetailsProps {
//   apiBase: string
//   fields: FieldDef<DoughRecipe>[]
// }

// export function DoughRecipeIngredientsDetailsTable(items: DoughRecipeIngredientsDetails[], fields: FieldDef<DoughRecipe>[]) {
//   return (
//     <table>
//       <tbody>
//         {fields.map(f => (

export function DoughRecipeDetails({ apiBase }: { apiBase: string }) {
  const [basicDetails, setBasicDetails] = useState<DoughRecipeDetails | null>(
    null,
  );
  const [ingredients, setIngredients] = useState<IngredientDetails[]>([]);
  const [percentages, setPercentages] = useState<DoughPercentageDetails | null>(
    null,
  );
  const [editingIngredients, setEditingIngredients] = useState(false);
  //   const [ingredients, setIngredients] = useState<DoughRecipeIngredientsDetails[]>([])

  const fetchDetails = useCallback(
    async (id: string) => {
      const res = await fetch(`${apiBase}/${id}/details`);
      if (res.ok) {
        const data = await res.json();
        console.log("Fetched recipe details:", data.percentages);
        setBasicDetails(data.basic_details);
        setIngredients(data.ingredients);
        setPercentages(data.percentages);
        console.log("Set percentages state to:", percentages);
      }
    },
    [apiBase],
  );

  useEffect(() => {
    // Extract the recipe ID from the URL (e.g., /dough-recipe/123)
    const pathParts = window.location.pathname.split("/");
    console.log("Path parts:", pathParts);
    const id = pathParts[pathParts.length - 1];
    console.log("Extracted ID:", id);
    fetchDetails(id);
  }, [fetchDetails]);

  return (
    <div>
      <h2>
        Recipe:{" "}
        {basicDetails
          ? `${basicDetails.name} (${basicDetails.id})`
          : "Loading..."}
      </h2>
      <p>
        Date logged:{" "}
        {basicDetails?.created_at
          ? Intl.DateTimeFormat("en-US").format(
              new Date(basicDetails.created_at),
            )
          : "N/A"}
      </p>
      <p>{basicDetails?.notes}</p>
      <br />
      {basicDetails?.parent_id && (
        <Link to={`/dough-recipe/${basicDetails.parent_id}`}>
          View Parent Recipe ({basicDetails.parent_id})
        </Link>
      )}
      <br />
      <IngredientsTable items={ingredients} />
      <br />
      <PercentagesTable percentages={percentages} />
    </div>
  );
}
