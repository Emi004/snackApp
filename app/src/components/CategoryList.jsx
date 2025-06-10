import "./CategoryList.css";

export function CategoryList(props) {
  return (
    <div className="recipe-categories">
      {props.categories.map((cat) => {
        return (
          <div
            className="category-badge"
            style={{ backgroundColor: cat.color }}
            key={`category-${cat.id}`}
          >
            {cat.name}
          </div>
        );
      })}
    </div>
  );
}
