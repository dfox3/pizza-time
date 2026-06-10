import type { FieldDef, FormState } from "./FieldDef";

/** Renders the editable <td> cells for both EditRow and AddForm. */
interface FormFieldsProps<T extends Record<string, unknown>> {
  fields: FieldDef<T>[];
  form: FormState;
  /** Called with (fieldKey, newValue) on every change. */
  onChange: (key: string, value: string) => void;
  /** When true, renders <td> cells; when false renders <label> blocks. */
  asCells?: boolean;
}

function FieldInput<T extends Record<string, unknown>>({
  field,
  value,
  onChange,
}: {
  field: FieldDef<T>;
  value: string;
  onChange: (v: string) => void;
}) {
  if (field.readOnly) return <span>{value || "—"}</span>;

  if (field.type === "select" && field.options) {
    return (
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {field.options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    );
  }

  return (
    <input
      type={field.type === "number" ? "number" : "text"}
      step={field.step}
      value={value}
      placeholder={field.optional ? "optional" : undefined}
      onChange={(e) => onChange(e.target.value)}
      required={!field.optional}
    />
  );
}

export function FormFields<T extends Record<string, unknown>>({
  fields,
  form,
  onChange,
  asCells = true,
}: FormFieldsProps<T>) {
  const editableFields = fields.filter((f) => !f.readOnly);

  if (asCells) {
    return (
      <>
        {editableFields.map((f) => (
          <td key={f.key}>
            <FieldInput
              field={f}
              value={form[f.key] ?? ""}
              onChange={(v) => onChange(f.key, v)}
            />
          </td>
        ))}
      </>
    );
  }

  return (
    <>
      {editableFields.map((f) => (
        <label key={f.key}>
          {f.label}
          <FieldInput
            field={f}
            value={form[f.key] ?? ""}
            onChange={(v) => onChange(f.key, v)}
          />
        </label>
      ))}
    </>
  );
}
