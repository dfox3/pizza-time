import type { DoughPercentageDetails } from "../../schemas/doughRecipe";

export function PercentagesTable({
  percentages,
}: {
  percentages: DoughPercentageDetails | null;
}) {
  console.log("Rendering PercentagesTable with percentages:", percentages);
  return (
    <div>
      <table>
        <caption>Dough Ingredient Percentages</caption>
        <thead>
          <tr>
            <th>Ingredient</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Water (Hydration)</td>
            <td>
              {percentages?.hydration != null
                ? `${percentages.hydration.toFixed(1)}%`
                : "-"}
            </td>
          </tr>
          <tr>
            <td>Salt</td>
            <td>
              {percentages?.salt_percentage != null
                ? `${percentages.salt_percentage.toFixed(1)}%`
                : "-"}
            </td>
          </tr>
          <tr>
            <td>Yeast</td>
            <td>
              {percentages?.yeast_percentage != null
                ? `${percentages.yeast_percentage.toFixed(2)}%`
                : "-"}
            </td>
          </tr>
          <tr>
            <td>Sugar</td>
            <td>
              {percentages?.sugar_percentage != null
                ? `${percentages.sugar_percentage.toFixed(2)}%`
                : "-"}
            </td>
          </tr>
          <tr>
            <td>Oil</td>
            <td>
              {percentages?.oil_percentage != null
                ? `${percentages.oil_percentage.toFixed(2)}%`
                : "-"}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
