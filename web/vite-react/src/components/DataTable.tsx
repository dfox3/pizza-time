import type { FieldDef } from "./FieldDef";
import { EditRow } from "./EditRow";
import type { LinkField } from "./ResourcePage";
import { Link } from "react-router";

interface DataTableProps<T extends Record<string, unknown>> {
  items: T[];
  idKey: keyof T & string;
  fields: FieldDef<T>[];
  linkFields?: LinkField[];
  apiBase: string;
  editingId: unknown;
  /** The canonical (unscaled) record to populate the edit form with. */
  editingRecord: T | null;
  onEdit: (id: unknown) => void;
  onSaved: (updated: T) => void;
  onCancelEdit: () => void;
  onDelete: (id: unknown) => void;
}

export function DataTable<T extends Record<string, unknown>>({
  items,
  idKey,
  fields,
  linkFields,
  apiBase,
  editingId,
  editingRecord,
  onEdit,
  onSaved,
  onCancelEdit,
  onDelete,
}: DataTableProps<T>) {
  function constructLink(item: T, linkField: LinkField): string {
    const val = item[linkField.field];
    if (val == null) return "#";
    return `${linkField.urlPrefix}${val}`;
  }

  function formatCell(item: T, field: FieldDef<T>): string {
    const val = item[field.key];
    if (field.format) return field.format(val as T[typeof field.key]);
    if (val == null) return "—";
    if (linkFields?.some((f) => f.field === field.key)) {
      return (
        <Link
          to={constructLink(
            item,
            linkFields.find((f) => f.field === field.key)!,
          )}
        >
          {String(val)}
        </Link>
      );
    }
    return String(val);
  }

  return (
    <table>
      <thead>
        <tr>
          {fields.map((f) => (
            <th key={f.key}>{f.label}</th>
          ))}
          <th />
        </tr>
      </thead>
      <tbody>
        {items.length === 0 && (
          <tr>
            <td colSpan={fields.length + 1}>No records yet.</td>
          </tr>
        )}
        {items.map((item) =>
          item[idKey] === editingId && editingRecord ? (
            <EditRow
              key={String(item[idKey])}
              record={editingRecord}
              idKey={idKey}
              fields={fields}
              apiBase={apiBase}
              onSave={onSaved}
              onCancel={onCancelEdit}
            />
          ) : (
            <tr key={String(item[idKey])}>
              {fields.map((f) => (
                <td key={f.key}>{formatCell(item, f)}</td>
              ))}
              <td>
                <button onClick={() => onEdit(item[idKey])}>Edit</button>
                <button onClick={() => onDelete(item[idKey])}>Delete</button>
              </td>
            </tr>
          ),
        )}
      </tbody>
    </table>
  );
}
