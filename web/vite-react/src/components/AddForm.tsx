import { useId, useState } from "react";
import type { FieldDef, FormState } from "./FieldDef";
import { buildInitialForm, buildPayload, recordToForm } from "./FieldDef";
import { FormFields } from "./FormFields";

interface AddFormProps<T extends Record<string, unknown>> {
  fields: FieldDef<T>[];
  apiBase: string;
  idKey: string;
  onAdd: (created: T) => void;
  /** Existing records available as templates. */
  templateItems?: T[];
  /** Returns the display label for a template item (shown in the dropdown). */
  templateLabel?: (item: T) => string;
}

export function AddForm<T extends Record<string, unknown>>({
  fields,
  apiBase,
  idKey,
  onAdd,
  templateItems = [],
  templateLabel,
}: AddFormProps<T>) {
  const [form, setForm] = useState<FormState>(buildInitialForm(fields));
  const [templateSearch, setTemplateSearch] = useState("");
  const [error, setError] = useState<string | null>(null);
  const datalistId = useId();

  function handleChange(key: string, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleTemplateInput(value: string) {
    setTemplateSearch(value);
    if (!templateLabel) return;
    const match = templateItems.find((item) => templateLabel(item) === value);
    if (match) {
      // Fetch unscaled (multiplier=1.0 default) record from the API
      const res = await fetch(`${apiBase}/${match[idKey as keyof T]}`);
      if (res.ok) {
        setForm(recordToForm(fields, await res.json()));
      } else {
        setForm(recordToForm(fields, match));
      }
      setTemplateSearch("");
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    const res = await fetch(apiBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildPayload(fields, form)),
    });
    if (res.ok) {
      onAdd(await res.json());
      setForm(buildInitialForm(fields));
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data?.detail ?? `Error ${res.status}`);
    }
  }

  return (
    <form className="add-form" onSubmit={handleSubmit}>
      <div className="add-form-header">
        <h3>Add Record</h3>
        {templateItems.length > 0 && templateLabel && (
          <label className="template-label">
            Build from template
            <input
              list={datalistId}
              value={templateSearch}
              placeholder="Search existing…"
              onChange={(e) => handleTemplateInput(e.target.value)}
            />
            <datalist id={datalistId}>
              {templateItems.map((item) => (
                <option
                  key={String(item["id" as keyof T])}
                  value={templateLabel(item)}
                />
              ))}
            </datalist>
          </label>
        )}
      </div>
      <div className="add-grid">
        <FormFields
          fields={fields}
          form={form}
          onChange={handleChange}
          asCells={false}
        />
        <label className="submit-cell">
          <button type="submit">Add</button>
        </label>
      </div>
      {error && <p className="form-error">{error}</p>}
    </form>
  );
}
