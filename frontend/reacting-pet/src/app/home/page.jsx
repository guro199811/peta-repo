"use client";

import styles from "./HomePage.module.css";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/constants/config/config";

function HomePage() {
  const [userData, setUserData] = useState({});
  const [editMode, setEditMode] = useState(false);
  const { userToken } = useToken();
  const router = useRouter();

  const [phonePrefixes, setPhonePrefixes] = useState({
    prefixes: [{}],
  });

  // if user is not logged in throw 404
  useEffect(() => {
    if (!userToken) {
      // Redirect to login if no token
      router.push("/not_found");
    } else if (userToken) {
      fetch(`${API_BASE_URL}/user_data`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${userToken.access_token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data[2])
          setUserData(data[2]);
        })
        .catch((error) => {
          console.error(error);
        });

      fetch(`${API_BASE_URL}/auth/register`)
        .then((response) => response.json())
        .then((data) => {
          setPhonePrefixes(data);
        })
        .catch((error) => console.error("Error:", error));
    }
  }, [userToken, router]);

  if (!userToken) {
    return (
      <div
        className="flex w-full h-full text-center justify-center
      items-center text-black font-medium font-serif"
      >
        Redirecting...
      </div>
    );
  }
  return (
    <>
      <Image
        className="-z-10"
        src="/assets/owner-bg.jpg"
        alt="Background Image"
        layout="fill"
        objectFit="cover"
        priority
      />
      <div className={styles.owner_container}>
        <div className={styles.buttons}>
          <a className={styles.square_button}>Dashboard</a>
          {/* TODO: later implement "my pet history" into my pets */}
          <a className={styles.square_button}>My Pets</a>
          <a className={styles.square_button}>Clinic</a>
          <a className={styles.square_button}>Vet Numbers</a>
        </div>
        <div className={styles.box_menu}>
          <h1>Hello {userData.name}</h1>
          <a onClick={() => {setEditMode(true)}}>Change User Data</a>
          {editMode && (
            <div>
              <label>First name</label>
              <input type="text" value={userData.name} />
              <label>Last name</label>
              <input type="text" value={userData.lastname} />
              <label>Phone Number</label>
              <div className={styles.phone_input}>
                <select
                  className={styles.phone_select}
                  name="prefix"
                  defaultValue={userData.prefix}
                  required
                >
                  {phonePrefixes.prefixes.map((prefix) => (
                    <option key={prefix.prefix} value={prefix.prefix}>
                      {prefix.icon} {prefix.prefix}
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  name="phone"
                  minLength={9}
                  maxLength={9}
                  value={userData.phone}
                  required
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default HomePage;
