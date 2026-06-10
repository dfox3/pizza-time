import "./App.css";
import { ResourcePage } from "./components/ResourcePage";
import {
  doughRecipeGridFields,
  doughRecipeQueryParams,
  doughRecipeDetailFields,
} from "./schemas/doughRecipe";
import type { DoughRecipe } from "./schemas/doughRecipe";
import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import { DoughRecipeDetails } from "./pages/DoughRecipeDetails";

export default function App() {
  return (
    <BrowserRouter>
      <div className="page">
        <h1>dFizza</h1>
        <Routes>
          <Route path="/" element={<Navigate to="/dough-recipe" replace />} />
          <Route
            path="/dough-recipe"
            element={
              <ResourcePage<DoughRecipe>
                title="Dough Recipes"
                apiBase="/api/dough-recipe"
                idKey="id"
                fields={doughRecipeGridFields}
                linkFields={[{ field: "id", urlPrefix: "/dough-recipe/" }]}
                queryParams={doughRecipeQueryParams}
                templateLabel={(r) =>
                  r.name ? `${r.name} (#${r.id})` : `Recipe #${r.id}`
                }
              />
            }
          />
          <Route
            path="/dough-recipe/:id"
            element={<DoughRecipeDetails apiBase="/api/dough-recipe" />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
