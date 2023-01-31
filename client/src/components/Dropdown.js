import React from "react";

function Dropdown({
  toggleOptions,
  selectOption,
  data,
  selected,
  showOptions,
}) {
  return (
    <div className="dropdown">
      <div className="dropdown-button" onClick={toggleOptions}>
        {selected}
      </div>
      {showOptions ? (
        <div className="dropdown-content">
          {data.map((data, index) => {
            return (
              <div
                className="dropdown-item"
                onClick={() => selectOption(data.label)}
              >
                {data.label}
              </div>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}

export default Dropdown;
