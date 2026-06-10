import type { FieldDef } from "../components/FieldDef";
import type { QueryParam } from "../components/ResourcePage";

enum FlourType {
  AP = "AP",
  Bread = "Bread",
  DoubleZero = "00",
  WholeWheat = "Whole Wheat",
  Other = "Other",
}

enum SaltType {
  Iodized = "Iodized",
  Kosher = "Kosher",
  Sea = "Sea",
  Himalayan = "Himalayan",
  Other = "Other",
}

enum YeastType {
  ActiveDry = "Active Dry",
  Instant = "Instant",
  Fresh = "Fresh",
  Other = "Other",
}

enum SugarType {
  White = "White",
  Brown = "Brown",
  Honey = "Honey",
  Agave = "Agave",
  Raw = "Raw",
  Powdered = "Powdered",
  Other = "Other",
}

enum OilType {
  Olive = "Olive",
  Vegetable = "Vegetable Oil",
  Unrefined = "Unrefined Olive Oil",
  Butter = "Butter",
  Other = "Other",
}

export interface DoughRecipe {
  id: number;
  parent_id: number | null;
  name: string | null;
  created_at: string;
  flour_type: FlourType;
  flour_description: string | null;
  flour_grams: number;
  water_description: string | null;
  water_grams: number;
  salt_type: SaltType;
  salt_description: string | null;
  salt_grams: number;
  yeast_type: YeastType;
  yeast_description: string | null;
  yeast_grams: number;
  sugar_type: SugarType | null;
  sugar_description: string | null;
  sugar_grams: number | null;
  oil_type: OilType | null;
  oil_description: string | null;
  oil_grams: number | null;
  ball_weight: number;
  hydration: number;
  salt_percentage: number;
  yeast_percentage: number;
  oil_percentage: number;
  sugar_percentage: number;
  notes: string | null;
  poolish: number | null;
}

export interface DoughRecipeList {
  id: number;
  parent_id: number | null;
  name: string | null;
  created_at: string;
  flour_type: FlourType;
  flour_description: string | null;
  flour_grams: number;
  water_description: string | null;
  water_grams: number;
  salt_type: SaltType;
  salt_description: string | null;
  salt_grams: number;
  yeast_type: YeastType;
  yeast_description: string | null;
  yeast_grams: number;
  sugar_type: SugarType | null;
  sugar_description: string | null;
  sugar_grams: number | null;
  oil_type: OilType | null;
  oil_description: string | null;
  oil_grams: number | null;
  ball_weight: number;
  hydration: number;
  salt_percentage: number;
  yeast_percentage: number;
  oil_percentage: number;
  sugar_percentage: number;
  notes: string | null;
  poolish: number | null;
}

export interface DoughRecipeDetails {
  id: number;
  parent_id: number | null;
  name: string | null;
  created_at: string;
  flour_type: FlourType;
  flour_description: string | null;
  flour_grams: number;
  water_description: string | null;
  water_grams: number;
  salt_type: SaltType;
  salt_description: string | null;
  salt_grams: number;
  yeast_type: YeastType;
  yeast_description: string | null;
  yeast_grams: number;
  sugar_type: SugarType | null;
  sugar_description: string | null;
  sugar_grams: number | null;
  oil_type: OilType | null;
  oil_description: string | null;
  oil_grams: number | null;
  ball_weight: number;
  hydration: number;
  salt_percentage: number;
  yeast_percentage: number;
  oil_percentage: number;
  sugar_percentage: number;
  notes: string | null;
  poolish: number | null;
}

export interface IngredientDetails {
  ingredient: string;
  type: string | null;
  description: string | null;
  grams: number | null;
}
export interface DoughPercentageDetails {
  hydration: number;
  salt_percentage: number;
  yeast_percentage: number;
  sugar_percentage: number;
  oil_percentage: number;
}

export interface DoughRecipeIngredientsDetails {
  flour: IngredientDetails;
  water: IngredientDetails;
  salt: IngredientDetails;
  yeast: IngredientDetails;
  sugar?: IngredientDetails;
  oil?: IngredientDetails;
}

export interface DoughRecipeEditFields {
  name: string | null;
  flour_type: FlourType | null;
  flour_description: string | null;
  flour_grams: number | null;
  water_description: string | null;
  water_grams: number | null;
  salt_type: SaltType | null;
  salt_description: string | null;
  salt_grams: number | null;
  yeast_type: YeastType | null;
  yeast_description: string | null;
  yeast_grams: number | null;
  sugar_type?: SugarType | null;
  sugar_description?: string | null;
  sugar_grams?: number | null;
  oil_type?: OilType | null;
  oil_description?: string | null;
  oil_grams?: number | null;
  notes?: string | null;
  poolish?: number | null;
}

// const FLOUR_TYPES = ["AP", "Bread", "00", "Whole Wheat", "Other"] as const;
// const SALT_TYPES = ["Iodized", "Kosher", "Sea", "Himalayan", "Other"] as const;
// const YEAST_TYPES = ["Active Dry", "Instant", "Fresh", "Other"] as const;
// const SUGAR_TYPES = [
//   "White",
//   "Brown",
//   "Honey",
//   "Agave",
//   "Raw",
//   "Powdered",
//   "Other",
// ] as const;
// const OIL_TYPES = ["Olive", "Vegetable", "Canola", "Avocado", "Other"] as const;

export const doughRecipeGridFields: FieldDef<DoughRecipe>[] = [
  { key: "id", label: "ID", type: "number", readOnly: true },
  {
    key: "created_at",
    label: "Created",
    type: "text",
    readOnly: true,
    format: (v) => new Date(v as string).toLocaleString(),
  },
  {
    key: "name",
    label: "Name",
    type: "text",
    optional: true,
    defaultValue: "",
  },
  {
    key: "flour_grams",
    label: "Flour (g)",
    type: "number",
    step: 0.1,
    defaultValue: "500",
  },
  {
    key: "water_grams",
    label: "Water (g)",
    type: "number",
    step: 0.1,
    defaultValue: "325",
  },
  {
    key: "salt_grams",
    label: "Salt (g)",
    type: "number",
    step: 0.1,
    defaultValue: "10",
  },
  {
    key: "yeast_grams",
    label: "Yeast (g)",
    type: "number",
    step: 0.1,
    defaultValue: "2",
  },
  {
    key: "sugar_grams",
    label: "Sugar (g)",
    type: "number",
    step: 0.1,
    optional: true,
    defaultValue: "",
  },
  {
    key: "oil_grams",
    label: "Oil (g)",
    type: "number",
    step: 0.1,
    optional: true,
    defaultValue: "",
  },
  {
    key: "ball_weight",
    label: "Ball Wt",
    type: "number",
    readOnly: true,
    format: (v) => (v as number)?.toFixed(1) ?? "—",
  },
  {
    key: "hydration",
    label: "Hydration",
    type: "number",
    readOnly: true,
    format: (v) => `${(v as number)?.toFixed(1)}%`,
  },
  {
    key: "diameter",
    label: "Diameter",
    type: "number",
    readOnly: true,
    format: (v) => (v as number)?.toFixed(1) ?? "—",
  },
];
// export const doughRecipeDetailFields: FieldDef<DoughRecipe>[] = [
//   { key: "id", label: "ID", type: "number", readOnly: true },
//   { key: "parent_id", label: "Parent ID", type: "number", readOnly: true },
//   {
//     key: "name",
//     label: "Name",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "created_at",
//     label: "Created",
//     type: "text",
//     readOnly: true,
//     format: (v) => new Date(v as string).toLocaleString(),
//   },
//   {
//     key: "flour_type",
//     label: "Flour Type",
//     type: "select",
//     options: FlourType,
//     defaultValue: "AP",
//   },
//   {
//     key: "flour_description",
//     label: "Flour Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "flour_grams",
//     label: "Flour (g)",
//     type: "number",
//     step: 0.1,
//     defaultValue: "500",
//   },
//   {
//     key: "water_description",
//     label: "Water Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "water_grams",
//     label: "Water (g)",
//     type: "number",
//     step: 0.1,
//     defaultValue: "325",
//   },
//   {
//     key: "salt_type",
//     label: "Salt Type",
//     type: "text",
//     defaultValue: "iodized",
//   },
//   {
//     key: "salt_description",
//     label: "Salt Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "salt_grams",
//     label: "Salt (g)",
//     type: "number",
//     step: 0.1,
//     defaultValue: "10",
//   },
//   {
//     key: "yeast_type",
//     label: "Yeast Type",
//     type: "text",
//     defaultValue: "active_dry",
//   },
//   {
//     key: "yeast_description",
//     label: "Yeast Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "yeast_grams",
//     label: "Yeast (g)",
//     type: "number",
//     step: 0.1,
//     defaultValue: "2",
//   },
//   {
//     key: "sugar_type",
//     label: "Sugar Type",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "sugar_description",
//     label: "Sugar Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "sugar_grams",
//     label: "Sugar (g)",
//     type: "number",
//     step: 0.1,
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "oil_type",
//     label: "Oil Type",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "oil_description",
//     label: "Oil Desc",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "oil_grams",
//     label: "Oil (g)",
//     type: "number",
//     step: 0.1,
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "ball_weight",
//     label: "Ball Wt",
//     type: "number",
//     readOnly: true,
//     format: (v) => (v as number)?.toFixed(1) ?? "—",
//   },
//   {
//     key: "hydration",
//     label: "Hydration",
//     type: "number",
//     readOnly: true,
//     format: (v) => `${(v as number)?.toFixed(1)}%`,
//   },
//   {
//     key: "salt_percentage",
//     label: "Salt %",
//     type: "number",
//     readOnly: true,
//     format: (v) => `${(v as number)?.toFixed(2)}%`,
//   },
//   {
//     key: "yeast_percentage",
//     label: "Yeast %",
//     type: "number",
//     readOnly: true,
//     format: (v) => `${(v as number)?.toFixed(2)}%`,
//   },
//   {
//     key: "oil_percentage",
//     label: "Oil %",
//     type: "number",
//     readOnly: true,
//     format: (v) => `${(v as number)?.toFixed(2)}%`,
//   },
//   {
//     key: "sugar_percentage",
//     label: "Sugar %",
//     type: "number",
//     readOnly: true,
//     format: (v) => `${(v as number)?.toFixed(2)}%`,
//   },
//   {
//     key: "notes",
//     label: "Notes",
//     type: "text",
//     optional: true,
//     defaultValue: "",
//   },
//   {
//     key: "poolish",
//     label: "Poolish",
//     type: "number",
//     step: 0.1,
//     optional: true,
//     defaultValue: "",
//   },
// ];

export const doughRecipeQueryParams: QueryParam[] = [
  {
    key: "multiplier",
    label: "Multiplier",
    type: "number",
    defaultValue: "1.0",
    step: 0.1,
  },
  {
    key: "target_diameter",
    label: "Target Diameter",
    type: "number",
    defaultValue: "",
  },
];
