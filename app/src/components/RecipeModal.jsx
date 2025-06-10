import { Modal, Carousel, FormControl } from "react-bootstrap";
import { CategoryList } from "./CategoryList";
import { DurationBadge } from "./DurationBadge";
import { useState } from "react";
import "./RecipeModal.css";

export function RecipeModal(props) {
  const [ingredientMultiplier, setIngredientMultiplier] = useState(1);

  return (
    <Modal
      centered
      scrollable
      show={props.show}
      onHide={() => {
        setIngredientMultiplier(1);
        props.handleCloseRecipeModal();
      }}
    >
      <Modal.Header closeButton>
        <Modal.Title>{props.recipe.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Carousel
          className="mb-4"
          controls={props.recipe.pictures.length > 1}
          indicators={props.recipe.pictures.length > 1}
          wrap
          touch
        >
          {props.recipe.pictures.map((pic, index) => {
            return (
              <Carousel.Item key={`recipe-${props.recipe.id}-pic-${index}`}>
                <img
                  className="d-block w-100"
                  height={300}
                  src={pic}
                  alt={`${props.recipe.name}-${index}`}
                />
              </Carousel.Item>
            );
          })}
        </Carousel>
        <CategoryList categories={props.recipe.categories} />
        <DurationBadge duration={props.recipe.duration} />
        <h5 className="mt-2">Ingredients:</h5>
        <ul>
          {props.recipe.ingredients.map((ingredient, index) => {
            return (
              <li key={`ingredient-${props.recipe.id}-${index}`}>
                {ingredientMultiplier * ingredient.quantity} {ingredient.unit}{" "}
                {ingredient.name}
              </li>
            );
          })}
        </ul>

        <FormControl
          placeholder="Multiplier"
          type="number"
          value={ingredientMultiplier}
          onChange={(e) => setIngredientMultiplier(e.target.value)}
          size="sm"
          min={1}
          className="w-25"
        />
        <h5 className="mt-3">Instructions:</h5>
        <p>{props.recipe.instructions}</p>
      </Modal.Body>
    </Modal>
  );
}
