"use client";

import styles from "./HomePage.module.css";
import { useEffect, useState } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { useRouter } from "next/navigation";
import { API_BASE_URL } from "@/constants/config/config";

function HomePage() {
  const [userData, setUserData] = useState({});
  const [editMode, setEditMode] = useState(false);
  const [selectedPrefix, setSelectedPrefix] = useState({
    icon: "🇬🇪",
    prefix: "+995",
    nums: 9,
  });
  const [updatedFields, setUpdatedFields] = useState({});
  const { userToken } = useToken();
  const router = useRouter();

  const [phonePrefixes, setPhonePrefixes] = useState({
    prefixes: [{}],
  });

  // if user is not logged in throw 404
  useEffect(() => {
    const cachedCurrentUser = localStorage.getItem("currentUser");

    if (cachedCurrentUser) {
      setUserData(JSON.parse(cachedCurrentUser));
    } else {
      fetch(`${API_BASE_URL}/user_data`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userToken.access_token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setUserData(data);
          localStorage.setItem("currentUser", JSON.stringify(data));
        })
        .catch((error) => {
          console.error(error);
        });
      }
      const cachedPrefixes = localStorage.getItem("phonePrefixes");
      // console.log(`Prefixes are: ${cachedPrefixes}`);
      // Fetch Phone prefixes from API
      if (cachedPrefixes) {
        setPhonePrefixes(JSON.parse(cachedPrefixes));
      } else {
        fetch(`${API_BASE_URL}/auth/register`)
          .then((response) => response.json())
          .then((data) => {
            setPhonePrefixes(data);
            localStorage.setItem("phonePrefixes", JSON.stringify(data));
          })
          .catch((error) => console.error("Error:", error));
      }
    }, [userToken, router]);

  // Handlers for field changes
  const handleInputChange = (field, value) => {
    setUserData((prev) => ({ ...prev, [field]: value }));
    setUpdatedFields((prev) => ({ ...prev, [field]: value }));
  };

  const handlePrefixChange = (event) => {
    const prefixValue = event.target.value;
    const selected = phonePrefixes.prefixes.find(
      (p) => p.prefix === prefixValue
    );
    setSelectedPrefix(selected);
    setUpdatedFields((prev) => ({ ...prev, prefix: prefixValue }));
    setUserData((prev) => ({ ...prev, prefix: prefixValue }));
  };

  // Update User data function
  const handleUpdateUserData = (e) => {
    e.preventDefault();
    fetch(`${API_BASE_URL}/user_data`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken.access_token}`,
      },
      body: JSON.stringify(updatedFields),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("User data updated successfully:", data);
        setEditMode(false);
        localStorage.removeItem("currentUser");
      })
      .catch((error) => {
        console.error("Error updating user data:", error);
      });
  };


  return (
    <>
      <h1 className={editMode ? "hidden" : ""}>Hello {userData.name}</h1>
      <a onClick={() => setEditMode(true)} className={editMode ? "hidden" : ""}>
        Change User Data
      </a>
      {editMode && (
        <form
          onSubmit={(e) => handleUpdateUserData(e)}
          className="flex flex-col justify-center
              space-y-4 pl-24 pr-24
              max-md:pl-4 max-md:pr-4
              lg:pl-60 lg:pr-60 
              2xl:pl-96 2xl:pr-96
              w-full h-full rounded-lg shadow-md"
        >
          <div>
            <label htmlFor="firstName" className="block font-medium">
              First name
            </label>
            <input
              id="firstName"
              type="text"
              value={userData.name || ""}
              onChange={(e) => handleInputChange("name", e.target.value)}
              className="border rounded-md w-full p-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>
          <div>
            <label htmlFor="lastName" className="block font-medium">
              Last name
            </label>
            <input
              id="lastName"
              type="text"
              value={userData.lastname || ""}
              onChange={(e) => handleInputChange("lastname", e.target.value)}
              className="border rounded-md w-full p-2 focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>
          <div>
            <label htmlFor="phone" className="block font-medium">
              Phone Number
            </label>
            <div className="flex items-center space-x-2">
              <select
                id="prefix"
                value={userData.prefix || ""}
                onChange={handlePrefixChange}
                required
                className="border rounded-md p-2 focus:outline-none
                focus:ring-2 focus:ring-amber-500 w-28"
              >
                {phonePrefixes.prefixes.map((prefix) => (
                  <option key={prefix.prefix} value={prefix.prefix}>
                    {prefix.icon} {prefix.prefix}
                  </option>
                ))}
              </select>
              <input
                id="phone"
                type="text"
                name="phone"
                value={userData.phone || ""}
                minLength={selectedPrefix.nums}
                maxLength={selectedPrefix.nums}
                onChange={(e) => {
                  const input = e.target.value;
                  if (/^\d*$/.test(input)) handleInputChange("phone", input);
                }}
                className={`border rounded-md p-2 w-full focus:outline-none transition-colors ${
                  userData.phone && userData.phone.length > selectedPrefix.nums
                    ? "border-red-600"
                    : "border-gray-300 focus:ring-2 focus:ring-amber-500"
                }`}
                required
                placeholder={`Enter ${selectedPrefix.nums}-digit phone number`}
                aria-invalid={
                  userData.phone && userData.phone.length > selectedPrefix.nums
                }
              />
            </div>
            {userData.phone && userData.phone.length > selectedPrefix.nums && (
              <span className="text-red-600 text-sm mt-1">
                Phone number must be {selectedPrefix.nums} digits long.
              </span>
            )}
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => {
                setEditMode(false);
                setUpdatedFields({});
              }}
              className="text-gray-500 px-4 py-2 hover:text-gray-700 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-amber-400 text-black px-4 py-2 
              rounded hover:bg-amber-500 hover:text-white transition"
            >
              Save
            </button>
          </div>
          {/* <button type="button" onClick={() => refreshCaches()}>
            refresh
          </button> */}
        </form>
      )}
    </>
  );
}

export default HomePage;
