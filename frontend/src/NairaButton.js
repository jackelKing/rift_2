import "./NairaButton.css";

export default function NairaButton({ text, icon, onClick }) {
  return (
    <button
      className="button button--naira button--naira-up"
      onClick={onClick}
    >
      <span>{text}</span>
      <div className="button__icon">
        {icon}
      </div>
      
    </button>
  );
}
