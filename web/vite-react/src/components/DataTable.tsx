import { useState } from "react";
import Modal from "react-bootstrap/esm/Modal";
import type { FieldDef } from "./FieldDef";
import type { LinkField } from "./ResourcePage";
import { Link } from "react-router";
import Button from "react-bootstrap/esm/Button";
import { Table } from "react-bootstrap";
import type { DoughRecipeEditFields } from "../schemas/doughRecipe";

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
  onDelete,
  onSaved,
}: DataTableProps<T>) {
  const [editingRecord, setEditingRecord] =
    useState<DoughRecipeEditFields<T> | null>(null);
  const [editingId, setEditingId] = useState<unknown>(null);
  const [editShow, setEditShow] = useState(false);

  const fetchEditDoughRecipe = async (
    editingId: number,
  ): Promise<DoughRecipeEditFields<T>> => {
    const res = await fetch(`${apiBase}/${editingId}/update-fields`, {
      method: "GET",
    });
    if (res.ok) {
      return await res.json();
    } else {
      throw new Error(`Failed to fetch record with id ${editingId}`);
    }
  };

  const patchDoughRecipe = async (): Promise<T> => {
    const res = await fetch(`${apiBase}/${editingId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editingRecord),
    });
    if (res.ok) {
      return await res.json();
      onSaved;
    } else {
      throw new Error(`Failed to patch record with id ${editingId}`);
    }
  };

  const handleEditClose = () => {
    setEditShow(false);
    setEditingId(null);
    setEditingRecord(null);
  };
  const handleEditShow = (editingId: number) => {
    setEditingId(editingId);
    fetchEditDoughRecipe(editingId).then((data) => {
      setEditingRecord(data);
      setEditShow(true);
    });
  };

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
    <>
      <Modal
        show={editShow}
        onHide={handleEditClose}
        backdrop="static"
        keyboard={false}
      >
        <Modal.Header closeButton>
          <Modal.Title>
            Edit Recipe "{editingRecord ? String(editingRecord.name) : ""}"?
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Table>
            <thead>
              <tr>
                <th>Field</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {editingRecord &&
                Object.entries(editingRecord).map(([key, value]) => {
                  return (
                    <tr key={key}>
                      <td>{key}</td>
                      <td>
                        <input
                          type={typeof value === "number" ? "number" : "text"}
                          step={typeof value === "number" ? "any" : undefined}
                          value={value as string}
                          onChange={(e) =>
                            setEditingRecord({
                              ...editingRecord,
                              [key]:
                                typeof value === "number"
                                  ? Number(e.target.value)
                                  : e.target.value,
                            })
                          }
                        />
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </Table>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleEditClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={() =>
              patchDoughRecipe(editingRecord![idKey]).then((data) => {
                setEditingRecord(data);
                setEditShow(false);
              })
            }
          >
            Save
          </Button>
        </Modal.Footer>
      </Modal>
      <Table>
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
          {items.map((item) => (
            <tr key={String(item[idKey])}>
              {fields.map((f) => (
                <td key={f.key}>{formatCell(item, f)}</td>
              ))}
              <td>
                <Button
                  variant="primary"
                  onClick={() => handleEditShow(item[idKey])}
                >
                  Edit
                </Button>
                <Button variant="danger" onClick={() => onDelete(item[idKey])}>
                  Delete
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );
}
