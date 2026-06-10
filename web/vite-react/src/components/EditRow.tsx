import { useState } from "react";
import type { FieldDef, FormState } from "./FieldDef";
import { buildPayload, recordToForm } from "./FieldDef";
import { FormFields } from "./FormFields";

interface EditRowProps<T extends Record<string, unknown>> {
  record: T;
  idKey: keyof T & string;
  fields: FieldDef<T>[];
  apiBase: string;
  onSave: (updated: T) => void;
  onCancel: () => void;
}

export function EditRow<T extends Record<string, unknown>>({
  record,
  idKey,
  fields,
  apiBase,
  onSave,
  onCancel,
}: EditRowProps<T>) {
  const [form, setForm] = useState<FormState>(recordToForm(fields, record));
  const [error, setError] = useState<string | null>(null);

  function handleChange(key: string, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSave() {
    setError(null);
    const res = await fetch(`${apiBase}/${record[idKey]}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildPayload(fields, form)),
    });
    if (res.ok) {
      onSave(await res.json());
    } else {
      const data = await res.json().catch(() => ({}));
      setError(data?.detail ?? `Error ${res.status}`);
    }
  }

  return (
    <tr>
      <td>{record[idKey]}</td>
      <td>
        {record["created_at"]
          ? new Date(record["created_at"] as string).toLocaleString()
          : "—"}
      </td>
      <FormFields fields={fields} form={form} onChange={handleChange} />
      <td>
        <button onClick={handleSave}>Save</button>{" "}
        <button onClick={onCancel}>Cancel</button>
        {error && <span className="row-error"> {error}</span>}
      </td>
    </tr>
  );
}
