import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import Dropdown from "./components/Dropdown";

function App() {
  const serverAddress = `${window.location.hostname}`;
  const [variety, setVariety] = useState("Puyat");
  const [type, setType] = useState("Regular");
  const [showOptions, setShowOptions] = useState(false);

  const durian_variety = [
    { value: 1, label: "Puyat" },
    { value: 2, label: "Arancillo" },
    { value: 3, label: "Chanee" },
  ];

  const durian_type = [
    { value: 1, label: "Regular" },
    { value: 2, label: "Deformed" },
  ];

  const [image, setImage] = useState([
    {
      image: null,
      position: "Left",
      index: 1,
    },
    {
      image: null,
      position: "Top",
      index: 2,
    },
    {
      image: null,
      position: "Right",
      index: 3,
    },
  ]);

  const toggleVariety = () => {
    setShowOptions(!showOptions);
  };

  const selectVariety = (option) => {
    setVariety(option);
    toggleVariety();
  };

  const toggleType = () => {
    setShowOptions(!showOptions);
  };

  const selectType = (option) => {
    setType(option);
    toggleVariety();
  };

  const fetchImage = async (index) => {
    console.log(index);
    try {
      const response = await axios.post(`http://${serverAddress}/image`, {
        imageId: index,
      });
      setImage((prevState) => {
        const newImage = [...prevState];
        newImage[index].image = `data:image/jpeg;base64,${response.data}`;
        return newImage;
      });
    } catch (error) {
      console.error(error);
    }
  };

  const reset = async () => {
    setImage(
      image.map((img) => {
        return {
          ...img,
          image: null,
        };
      })
    );

    try {
      await axios.post(`http://${serverAddress}/reset`);
    } catch (error) {
      console.error(error);
    }
  };

  const saveImages = async () => {
    try {
      const response = await axios.post(`http://${serverAddress}/save`, {
        type: type,
        variety: variety,
      });
    } catch (error) {
      console.error(error);
    }
    setImage(
      image.map((img) => {
        return {
          ...img,
          image: null,
        };
      })
    );
  };

  const handleClick = () => {
    for (let i = 0; i < image.length; i++) {
      setTimeout(() => fetchImage(i), i * 1000);
    }
  };

  return (
    <div className="main">
      <div className="card_holder">
        {image.map((img, index) => {
          return (
            <div className="card">
              {img.image && (
                <img className="pic" src={img.image} alt={img.position} />
              )}
            </div>
          );
        })}
      </div>
      <div className="button_holder">
        <div className="get_reset">
          <button className="btn" onClick={handleClick}>
            Get
          </button>

          <button className="btn" onClick={reset}>
            Reset
          </button>
        </div>
        <div>
          <button className="btn save" onClick={() => saveImages()}>
            Save
          </button>
        </div>

        <div className="dropdown_holder">
          <Dropdown
            toggleOptions={toggleType}
            selectOption={selectType}
            data={durian_type}
            selected={type}
            showOptions={showOptions}
          />

          <Dropdown
            toggleOptions={toggleVariety}
            selectOption={selectVariety}
            data={durian_variety}
            selected={variety}
            showOptions={showOptions}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
