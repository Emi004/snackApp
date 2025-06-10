import React, { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import "./HomePage.css";
import { CategoryList } from "../components/CategoryList";
import { DurationBadge } from "../components/DurationBadge";
import { RecipeModal } from "../components/RecipeModal";

export function HomePage() {
  const [recipes, setRecipes] = useState([]);
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/recipes`).then((response) =>
      response.json().then((data) => {
        setRecipes(data);
      })
    );
  }, []);

  const [currentRecipe, setCurrentRecipe] = useState(0);

  const [showRecipeModal, setShowRecipeModal] = useState(false);
  const onClickRecipe = (e) => {
    setCurrentRecipe(e.currentTarget.getAttribute("index"));
    setShowRecipeModal(true);
  };

  return (
    <>
      <h1>My Recipes</h1>
      <div>recipe count: {recipes.length}</div>
      <div className="recipes-container">
        {recipes.map((recipe, index) => {
          return (
            <Card
              key={`recipe-${recipe.id}`}
              index={index}
              onClick={onClickRecipe}
            >
              <Card.Img src={recipe.pictures[0]} height={300} />
              <Card.Body>
                <Card.Title>{recipe.name}</Card.Title>
                <CategoryList categories={recipe.categories} />
                <DurationBadge duration={recipe.duration} />
              </Card.Body>
            </Card>
          );
        })}
      </div>
      <RecipeModal
        show={showRecipeModal}
        recipe={
          recipes[currentRecipe]
            ? recipes[currentRecipe]
            : {
                categories: [],
                duration: "",
                pictures: [],
                id: null,
                name: "",
                ingredients: [],
                instructions: "",
              }
        }
        handleCloseRecipeModal={() => {
          setShowRecipeModal(false);
        }}
      />
    </>
  );
}
