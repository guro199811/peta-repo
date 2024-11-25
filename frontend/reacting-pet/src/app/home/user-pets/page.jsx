"use client";

import { useEffect, useState } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { API_BASE_URL } from "@/constants/config/config";
import { useRouter } from "next/navigation";

function UserPets() {
  const router = useRouter();

  const [userPets, setUserPets] = useState();
  const { userToken } = useToken();

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
          return setUserPets(null);
        }
        setUserPets(data);
      })
      .catch((error) => console.error("Error fetching user pets:", error));
  }, []);

  return (
    <div>
      {userPets ? (
        <ul key="outer">
          {userPets.map((pet) => (
            <li key={pet.id}>
              <div className="pet-info">
                <form>
                  <label htmlFor="name">
                    Name:{" "}
                    <input type="text" value={pet.name} required disabled />
                  </label>

                  <label htmlFor="species">
                    Species:{" "}
                    <input type="text" value={pet.pet_species} readOnly />
                  </label>

                  <label htmlFor="breed">
                    Breed:{" "}
                    <input type="text" value={pet.pet_breed} readOnly />
                  </label>

                  <label htmlFor="birth_date">
                    Birth Date:{" "}
                    <input
                      type="text"
                      value={pet.birth_date}
                      required
                      disabled
                    />
                  </label>

                  <label htmlFor="recent_vaccination">
                    Recent vaccination:{" "}
                    <input
                      type="date"
                      value={pet.recent_vaccination}
                      disabled
                    />
                  </label>
                </form>
              </div>
            </li>
          ))}
          <li>
            <a onClick={() => router.push("/home/user-pets/new-pet")}>
              Add New Pet
            </a>
          </li>
        </ul>
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
