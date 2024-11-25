"use client";

import { useState, useEffect } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { API_BASE_URL } from "@/constants/config/config.js";

const NewPet = () => {
  const [speciesData, setSpeciesData] = useState([]);
  const [selectedSpecies, setSelectedSpecies] = useState(null);
  const { userToken } = useToken();

  const [petData, setPetData] = useState({
    name: "",
    pet_species: "",
    pet_breed: "",
    gender: "",
    birth_date: "",
  });

  useEffect(() => {
    fetch(`${API_BASE_URL}/pet_types`)
      .then((response) => response.json())
      .then((data) => {
        setSpeciesData(data);
        setSelectedSpecies(data[0]); // Automatically select the first species
      })
      .catch((error) => console.error("Error:", error));
  }, []);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setPetData({ ...petData, [id]: value });
  };

  const handleSpeciesChange = (e) => {
    const species = speciesData.find(
      (type) => type.species_id === parseInt(e.target.value)
    );
    setSelectedSpecies(species);
    setPetData({ ...petData, pet_species: e.target.value, pet_breed: "" });
  };

  const handleBreedChange = (e) => {
    setPetData({ ...petData, pet_breed: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitted Pet Data:", petData);
    fetch(`${API_BASE_URL}/register_pet`,{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${userToken.access_token}`
      },
      body: JSON.stringify(petData)
    })
     .then((response) => response.json())
     .then((data) => {
        console.log("Pet registration response:", data);
        // Handle success or error
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="new_pet_box p-6 rounded-lg max-w-lg mx-auto">
      <h1 className="text-xl font-bold text-center text-gray-800 mb-4">
        Register Your Companion 🐾
      </h1>
      <form onSubmit={handleSubmit} className="space-y-2">
        <div>
          <label htmlFor="name" className="block text-gray-600 mb-1">
            Pet Name
          </label>
          <input
            type="text"
            id="name"
            required
            value={petData.name}
            onChange={handleInputChange}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>
        <div>
          <label htmlFor="birth_date" className="block text-gray-600 mb-1">
            Birth Date
          </label>
          <input
            type="date"
            id="birth_date"
            required
            value={petData.birth_date}
            onChange={handleInputChange}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>
        <div>
          <label htmlFor="gender" className="block text-gray-600 mb-1">
            Gender
          </label>
          <select
            id="gender"
            required
            value={petData.gender}
            onChange={handleInputChange}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>        
        <div>
          <label htmlFor="pet_species" className="block text-gray-600 mb-1">
            Select a Type
          </label>
          <select
            id="pet_species"
            required
            value={petData.pet_species}
            onChange={handleSpeciesChange}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="">Select a Type</option>
            {speciesData.map((type) => (
              <option key={type.species_id} value={type.species_id}>
                {type.species}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="breed" className="block text-gray-600 mb-1">
            Select a Breed
          </label>
          <select
            id="breed"
            required
            value={petData.pet_breed}
            onChange={handleBreedChange}
            className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="">Select a Breed</option>
            {selectedSpecies &&
              selectedSpecies.breeds.map((breed) => (
                <option key={breed.breed_id} value={breed.breed_id}>
                  {breed.breed}
                </option>
              ))}
          </select>
        </div>
        <div className="text-center">
          <button
            type="submit"
            className="bg-white border border-amber-900 shadow-sm shadow-amber-950
             text-amber-950 px-4 py-2 rounded-md hover:border-amber-400 hover:shadow-amber-400
             hover:text-amber-950 hover:bg-amber-400 focus:outline-none focus:ring-2
             focus:ring-amber-500 focus:ring-offset-2 transition-all"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewPet;
