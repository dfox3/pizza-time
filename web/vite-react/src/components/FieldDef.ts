/** Describes one field/column for a resource. */
export interface FieldDef<T extends Record<string, unknown>> {
  /** Must match the JSON key returned by the API. */
  key: keyof T & string;
  label: string;
  type: "text" | "number" | "select";
  options?: readonly string[];
  /** Optional field — empty string or null is allowed. */
  optional?: boolean;
  /** Shown in the table but never included in create/edit forms (e.g. computed fields). */
  readOnly?: boolean;
  /** Default value for the add form (stored as string; converted on submit). */
  defaultValue?: string;
  /** Step for number inputs. */
  step?: number;
  /** Custom display formatter for the table cell. */
  format?: (val: T[keyof T & string]) => string;
}

/** Convert a raw API value to the string used inside form state. */
export function toFormValue(val: unknown): string {
  if (val == null) return "";
  return String(val);
}

/** Convert form state strings back to the right JS type for the JSON payload. */
export function fromFormValue(
  val: string,
  type: "text" | "number" | "select",
  optional?: boolean,
): string | number | null {
  if (optional && val === "") return null;
  if (type === "number") return val === "" ? 0 : Number(val);
  return val || (optional ? null : "");
}

export type FormState = Record<string, string>;

export function buildInitialForm<T extends Record<string, unknown>>(
  fields: FieldDef<T>[],
): FormState {
  return Object.fromEntries(
    fields.filter((f) => !f.readOnly).map((f) => [f.key, f.defaultValue ?? ""]),
  );
}

export function buildPayload<T extends Record<string, unknown>>(
  fields: FieldDef<T>[],
  form: FormState,
): Partial<T> {
  return Object.fromEntries(
    fields
      .filter((f) => !f.readOnly)
      .map((f) => [
        f.key,
        fromFormValue(form[f.key] ?? "", f.type, f.optional),
      ]),
  ) as Partial<T>;
}

export function recordToForm<T extends Record<string, unknown>>(
  fields: FieldDef<T>[],
  record: T,
): FormState {
  return Object.fromEntries(
    fields
      .filter((f) => !f.readOnly)
      .map((f) => [f.key, toFormValue(record[f.key])]),
  );
}
