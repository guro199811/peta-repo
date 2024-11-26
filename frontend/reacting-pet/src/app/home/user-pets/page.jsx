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

  function capitalizeFirstLetter(val) {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
  }

  useEffect(() => {
    fetch(`${API_BASE_URL}/user_pets`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${userToken.access_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.code === 404) {
          return setUserPets([]);
        }
        setUserPets(data);
      })
      .catch((error) => console.error("Error fetching user pets:", error));
  }, []);

  const handleEdit = (petId) => {
    setIsEditing(petId); // Sets editing mode to the specific pet
  };

  const handleCancel = () => {
    setIsEditing(null); // Exits edit mode
  };

  const handleSave = (petId) => {
    const updatingPet = userPets.find((pet) => pet.pet_id === petId);
    if (!updatingPet) {
      console.error("Pet not found for editing");
      return;
    }
    // f_d stands for formatted date
    const f_dOfBirth= convertToISO8601(updatingPet.birth_date)
    const f_dOfVaccination = convertToISO8601(updatingPet.recent_vaccination)
    const updatedPet = {
      pet_species: updatingPet.pet_species.species_id,
      pet_breed: updatingPet.pet_breed.breed_id,
      gender: updatingPet.gender,
      medical_condition: updatingPet.medical_condition,
      current_treatment: updatingPet.current_treatment,
      recent_vaccination: f_dOfBirth,
      birth_date: f_dOfVaccination,
      owner_id: updatingPet.owner.id
    }
    fetch(`${API_BASE_URL}/pet/${petId}`, {
      method: "PUT",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken.access_token}`,
      },
      body: JSON.stringify({
        ...updatedPet
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.code === 200) {
          setUserPets((prev) =>
            prev.map((pet) =>
              pet.pet_id === petId ? { ...pet, ...data } : pet
            )
          );
          setIsEditing(null); // Exits edit mode after editing
        } else {
          console.log(data);
        }
      })
      .catch((error) => console.error("Error updating pet:", error));
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
        }
      })
      .catch((error) => console.error("Error deleting pet:", error));
  };

  function convertToISO8601(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split("T")[0];
  }

  return (
    <div>
      {userPets.length ? (
        <div>
          <ul key="outer" className="pet-grid">
            {userPets.map((pet) => {
              const isPetEditing = isEditing === pet.pet_id; // Changed: Isolates the editing mode to the specific pet
              return (
                <li key={pet.pet_id} className="pet-card">
                  <div className="pet-info">
                    <form>
                      <label htmlFor="name" className="block mb-2">
                        Name
                        <input
                          type="text"
                          value={
                            isPetEditing
                              ? pet.name
                              : capitalizeFirstLetter(pet.name) // Changed: Display static value for non-editing pets
                          }
                          disabled={!isPetEditing} // Changed: Input is only editable in edit mode
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

                      <label htmlFor="species" className="block mb-2">
                        Species
                        <input
                          type="text"
                          value={pet.pet_species.species}
                          readOnly
                          disabled
                          className="input-box"
                        />
                      </label>

                      <label htmlFor="breed" className="block mb-2">
                        Breed
                        <input
                          type="text"
                          value={pet.pet_breed.breed}
                          readOnly
                          disabled
                          className="input-box"
                        />
                      </label>

                      <label htmlFor="birth_date" className="block mb-2">
                        Birth Date
                        <input
                          type="text"
                          value={pet.birth_date}
                          disabled={!isPetEditing} // Changed: Input is only editable in edit mode
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
                          value={pet.recent_vaccination || ""} // Changed: Default empty value for non-editing mode
                          disabled={!isPetEditing} // Changed: Input is only editable in edit mode
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
                          className="style-button save-button mt-4 mr-4"
                          onClick={() => handleSave(pet.pet_id)}
                        >
                          Save
                        </button>
                        <button
                          className="style-button cancel-button mt-4"
                          onClick={handleCancel}
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <div>
                        <button
                          className="style-button edit-button mt-4"
                          onClick={() => handleEdit(pet.pet_id)}
                        >
                          Edit
                        </button>
                        <button
                          className="style-button delete-button mt-4 ml-4"
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
          <div className="add-pet-button-container mb-4">
            <a
              onClick={() => router.push("/home/user-pets/new-pet")}
              className="add-pet-button"
            >
              Add New Pet
            </a>
          </div>
        </div>
      ) : (
        <div>
          <p>No Pets Found</p>
          <a onClick={() => router.push("/home/user-pets/new-pet")}>
            Would you like to add new pets?
          </a>
        </div>
      )}
    </div>
  );
}

export default UserPets;
