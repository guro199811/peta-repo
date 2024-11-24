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
        <ul>
          {userPets.map((userPet) => (
            <li key={userPet.id}>{userPet.name}</li>
          ))}
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
