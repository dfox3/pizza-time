import { useCallback, useEffect, useRef, useState } from "react";
import type { FieldDef } from "./FieldDef";
import { DataTable } from "./DataTable";
import { AddForm } from "./AddForm";

export interface LinkField {
  field: string;
  urlPrefix: string;
  pathParam: string;
}

export interface QueryParam {
  key: string;
  label: string;
  type: "number" | "text";
  defaultValue: string;
  step?: number;
}

interface ResourcePageProps<T extends Record<string, unknown>> {
  title: string;
  apiBase: string;
  idKey: keyof T & string;
  fields: FieldDef<T>[];
  linkFields?: LinkField[];
  /** Optional query params added to the list request (e.g. multiplier). */
  queryParams?: QueryParam[];
  /**
   * Returns a display label for a record used in the "Build from template" dropdown.
   * If omitted, the template feature is hidden.
   */
  templateLabel?: (item: T) => string;
}

export function ResourcePage<T extends Record<string, unknown>>({
  title,
  apiBase,
  idKey,
  fields,
  linkFields = [],
  queryParams = [],
  templateLabel,
}: ResourcePageProps<T>) {
  const [items, setItems] = useState<T[]>([]);
  const [editingId, setEditingId] = useState<unknown>(null);
  const [editingRecord, setEditingRecord] = useState<T | null>(null);
  const [params, setParams] = useState<Record<string, string>>(
    Object.fromEntries(queryParams.map((p) => [p.key, p.defaultValue])),
  );

  const paramsRef = useRef(params);
  paramsRef.current = params;

  const fetchItems = useCallback(
    async (overrideParams?: Record<string, string>) => {
      console.log(
        "fetchItems with params",
        overrideParams ?? paramsRef.current,
      );
      const cleanedParams = Object.fromEntries(
        Object.entries(overrideParams ?? paramsRef.current).filter(
          ([_, v]) => v !== "",
        ),
      );
      console.log("cleanedParams", cleanedParams);
      const qs = new URLSearchParams(cleanedParams).toString();
      const res = await fetch(`${apiBase}/list${qs ? `?${qs}` : ""}`);
      if (res.ok) setItems(await res.json());
    },
    [apiBase],
  );

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  async function handleEdit(id: unknown) {
    // Always fetch at multiplier=1.0 so the edit form shows DB values
    const res = await fetch(`${apiBase}/${id}`);
    if (res.ok) {
      setEditingRecord(await res.json());
      setEditingId(id);
    }
  }

  function handleSaved(updated: T) {
    setItems((prev) =>
      prev.map((item) => (item[idKey] === updated[idKey] ? updated : item)),
    );
    setEditingId(null);
    setEditingRecord(null);
  }

  function handleDelete(id: unknown) {
    if (!window.confirm("Are you sure you want to delete this record?")) return;
    fetch(`${apiBase}/${id}`, { method: "DELETE" }).then((res) => {
      if (res.ok) {
        setItems((prev) => prev.filter((item) => item[idKey] !== id));
        if (editingId === id) {
          setEditingId(null);
          setEditingRecord(null);
        }
      } else {
        alert("Failed to delete record");
      }
    });
  }

  function handleParamChange(key: string, value: string) {
    setParams((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <section className="resource-section">
      <h2>{title}</h2>

      {queryParams.length > 0 && (
        <div className="toolbar">
          {queryParams.map((qp) => (
            <label key={qp.key}>
              {qp.label}{" "}
              <input
                type={qp.type}
                step={qp.step}
                value={params[qp.key]}
                onChange={(e) => handleParamChange(qp.key, e.target.value)}
                style={{ width: 80 }}
              />
            </label>
          ))}
          <button onClick={() => fetchItems(params)}>Refresh</button>
        </div>
      )}

      <DataTable
        items={items}
        idKey={idKey}
        fields={fields}
        linkFields={linkFields}
        apiBase={apiBase}
        editingId={editingId}
        editingRecord={editingRecord}
        onEdit={handleEdit}
        onSaved={handleSaved}
        onDelete={handleDelete}
        onCancelEdit={() => {
          setEditingId(null);
          setEditingRecord(null);
        }}
        links={fields.filter((f) => f.link)}
      />

      <AddForm
        fields={fields}
        apiBase={apiBase}
        idKey={idKey}
        onAdd={(item) => setItems((prev) => [...prev, item])}
        templateItems={items}
        templateLabel={templateLabel}
      />
    </section>
  );
}
