import { Modal, Form, FormGroup, FormControl } from "react-bootstrap";
import { useState } from "react";

export function AddCategoryModal(props) {
  const [categoryName, setCategoryName] = useState("");
  const [categoryColor, setCategoryColor] = useState("");

  const saveCategory = async () => {
    const data = { name: categoryName, color: categoryColor };
    await fetch(`${import.meta.env.VITE_API_URL}/categories`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    setCategoryName("");
    setCategoryColor("");
    props.handleClose();
  };

  return (
    <Modal show={props.show} onHide={props.handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Add Category</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <Form>
          <FormGroup>
            <Form.Label>Category Name</Form.Label>
            <FormControl
              placeholder="Enter category name"
              value={categoryName}
              onChange={(e) => setCategoryName(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Form.Label>Category Color</Form.Label>
            <FormControl
              type="color"
              value={categoryColor}
              onChange={(e) => setCategoryColor(e.target.value)}
            />
          </FormGroup>
        </Form>

        <button onClick={saveCategory}>Add Category</button>
      </Modal.Body>
    </Modal>
  );
}
