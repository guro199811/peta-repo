"use client";

import { useEffect, useState } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { API_BASE_URL } from "@/constants/config/config";
import { useRouter } from "next/navigation";
import "./user-pets.css";

function UserPets() {
  const router = useRouter();
  const [userPets, setUserPets] = useState([]);
  const [isEditing, setIsEditing] = useState(null);
  const { userToken } = useToken();

  const [speciesData, setSpeciesData] = useState([]);

  useEffect(() => {
    // caches
    const cachedSpecies = localStorage.getItem("pet_species");
    // Fetch user pets
    fetch(`${API_BASE_URL}/user_pets`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${userToken.access_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.code === 404) {
          setUserPets([]);
        } else {
          setUserPets(data);
        }
      })
      .catch((error) => console.error("Error fetching user pets:", error));

    // Fetch species data
    if (!cachedSpecies) {
      fetch(`${API_BASE_URL}/pet_types`)
        .then((response) => response.json())
        .then((data) => {
          setSpeciesData(data);
          localStorage.setItem("pet_species", JSON.stringify(data));
        })
        .catch((error) => console.error("Error fetching species:", error));
    } else {
      setSpeciesData(JSON.parse(cachedSpecies));
    }
  }, [userToken.access_token]);

  const handleSpeciesChange = (e, petId) => {
    const speciesId = parseInt(e.target.value);
    const species = speciesData.find((type) => type.species_id === speciesId);
    setUserPets((prev) =>
      prev.map((pet) =>
        pet.pet_id === petId
          ? { ...pet, pet_species: species, pet_breed: species.breeds[0] }
          : pet
      )
    );
  };

  const handleEdit = (petId) => {
    setIsEditing(petId); // Enable edit mode for the specific pet
  };

  const handleCancel = () => {
    setIsEditing(null); // Exit edit mode
  };

  const handleSave = (petId) => {
    const pet = userPets.find((p) => p.pet_id === petId);
    if (!pet) {
      console.error("Pet not found for saving");
      return;
    }

    const formattedPet = {
      pet_species: pet.pet_species.species_id,
      pet_breed: pet.pet_breed.breed_id,
      gender: pet.gender,
      medical_condition: pet.medical_condition,
      current_treatment: pet.current_treatment,
      recent_vaccination: convertToISO8601(pet.recent_vaccination),
      birth_date: convertToISO8601(pet.birth_date),
      owner_id: pet.owner.id,
    };

    fetch(`${API_BASE_URL}/pet/${petId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken.access_token}`,
      },
      body: JSON.stringify(formattedPet),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.code === 200) {
          setUserPets((prev) =>
            prev.map((p) => (p.pet_id === petId ? { ...p, ...data } : p))
          );
          setIsEditing(null); // Exit edit mode
        } else {
          console.error("Error updating pet:", data);
        }
      })
      .catch((error) => console.error("Error saving pet:", error));
  };

  const handleDelete = (petId) => {
    fetch(`${API_BASE_URL}/pet/${petId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken.access_token}`,
      },
    })
      .then((response) => {
        if (response.ok) {
          setUserPets((prev) => prev.filter((pet) => pet.pet_id !== petId));
        } else {
          console.error("Failed to delete pet");
        }
      })
      .catch((error) => console.error("Error deleting pet:", error));
  };

  function convertToISO8601(dateString) {
    if (dateString) {
      const date = new Date(dateString);
      return date.toISOString().split("T")[0];
    }
    return null;
  }

  function capitalizer(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
  }

  return (
    <div>
      {userPets.length ? (
        <div>
          <ul className="pet-grid">
            {userPets.map((pet) => {
              const isPetEditing = isEditing === pet.pet_id;
              const capitalizedName = capitalizer(pet.name);
              const formattedBdate = convertToISO8601(pet.birth_date);
              const formattedVac = convertToISO8601(pet.recent_vaccination);

              return (
                <li key={pet.pet_id} className="pet-card">
                  <div className="pet-info">
                    <form>
                      <label className="block mb-2">
                        Name
                        <input
                          type="text"
                          value={capitalizedName}
                          disabled={!isPetEditing}
                          onChange={(e) =>
                            setUserPets((prev) =>
                              prev.map((p) =>
                                p.pet_id === pet.pet_id
                                  ? { ...p, name: e.target.value }
                                  : p
                              )
                            )
                          }
                          className="input-box"
                        />
                      </label>

                      <label className="block mb-2">
                        Species
                        <select
                          value={pet.pet_species.species_id}
                          disabled={!isPetEditing}
                          onChange={(e) => handleSpeciesChange(e, pet.pet_id)}
                          className="input-box"
                        >
                          {speciesData.map((species) => (
                            <option
                              key={species.species_id}
                              value={species.species_id}
                            >
                              {species.species}
                            </option>
                          ))}
                        </select>
                      </label>

                      <label className="block mb-2">
                        Breed
                        <select
                          value={pet.pet_breed?.breed_id || ""}
                          disabled={!isPetEditing}
                          onChange={(e) =>
                            setUserPets((prev) =>
                              prev.map((p) =>
                                p.pet_id === pet.pet_id
                                  ? {
                                      ...p,
                                      pet_breed: {
                                        ...p.pet_breed,
                                        breed_id: parseInt(e.target.value),
                                        breed: speciesData
                                          .find(
                                            (species) =>
                                              species.species_id ===
                                              pet.pet_species.species_id
                                          )
                                          ?.breeds.find(
                                            (b) =>
                                              b.breed_id ===
                                              parseInt(e.target.value)
                                          )?.breed,
                                      },
                                    }
                                  : p
                              )
                            )
                          }
                          className="input-box"
                        >
                          {speciesData
                            .find(
                              (species) =>
                                species.species_id ===
                                pet.pet_species.species_id
                            )
                            ?.breeds.map((breed) => (
                              <option
                                key={breed.breed_id}
                                value={breed.breed_id}
                              >
                                {breed.breed}
                              </option>
                            ))}
                        </select>
                      </label>

                      <label className="block mb-2">
                        Birth Date
                        <input
                          type="date"
                          value={formattedBdate}
                          disabled={!isPetEditing}
                          onChange={(e) =>
                            setUserPets((prev) =>
                              prev.map((p) =>
                                p.pet_id === pet.pet_id
                                  ? { ...p, birth_date: e.target.value }
                                  : p
                              )
                            )
                          }
                          className="input-box"
                        />
                      </label>
                      <label
                        htmlFor="recent_vaccination"
                        className="block mb-2"
                      >
                        Recent Vaccination
                        <input
                          type="date"
                          value={formattedVac || ""}
                          disabled={!isPetEditing}
                          onChange={(e) =>
                            setUserPets((prev) =>
                              prev.map((p) =>
                                p.pet_id === pet.pet_id
                                  ? { ...p, recent_vaccination: e.target.value }
                                  : p
                              )
                            )
                          }
                          className="input-box"
                        />
                      </label>
                    </form>

                    {isPetEditing ? (
                      <div>
                        <button
                          className="style-button mr-4 save-button"
                          onClick={() => handleSave(pet.pet_id)}
                        >
                          Save
                        </button>
                        <button
                          className="style-button cancel-button"
                          onClick={handleCancel}
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <div>
                        <button
                          className="style-button mr-4 edit-button"
                          onClick={() => handleEdit(pet.pet_id)}
                        >
                          Edit
                        </button>
                        <button
                          className="style-button delete-button"
                          onClick={() => handleDelete(pet.pet_id)}
                        >
                          Delete
                        </button>
                      </div>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
          <div className="add-pet-button-container">
            <button
              onClick={() => router.push("/home/user-pets/new-pet")}
              className="add-pet-button mb-6"
            >
              Add New Pet
            </button>
          </div>
        </div>
      ) : (
        <div>
          <p>No pets found.</p>
          <button onClick={() => router.push("/home/user-pets/new-pet")}>
            Add a New Pet
          </button>
        </div>
      )}
    </div>
  );
}

export default UserPets;
