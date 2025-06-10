import hourglass from "../assets/hourglass.svg";
import "./DurationBadge.css";

export function DurationBadge(props) {
  return (
    <div className="recipe-duration">
      <img src={hourglass} alt="hourglass icon" />
      {props.duration}
    </div>
  );
}
