import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import "./App.css";
import { NavBar } from "./components/NavBar.jsx";
import { HomePage } from "./pages/HomePage.jsx";
import { AddRecipeModal } from "./components/AddRecipeForm.jsx";
import { AddCategoryModal } from "./components/AddCategoryModal.jsx";

function App() {
  const [showAddModal, setShowAddModal] = useState(false);
  const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);

  return (
    <>
      <NavBar
        onAddRecipe={() => setShowAddModal(true)}
        onAddCategory={() => setShowAddCategoryModal(true)}
      />

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </BrowserRouter>

      <AddRecipeModal
        showAddModal={showAddModal}
        setShowAddModal={setShowAddModal}
      />
      <AddCategoryModal
        show={showAddCategoryModal}
        handleClose={() => setShowAddCategoryModal(false)}
      />
    </>
  );
}

export default App;
