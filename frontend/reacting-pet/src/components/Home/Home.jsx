"use client"

import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "@/constants/config/config";
import styles from "./Home.module.css";

function Home() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(API_BASE_URL)
      .then((response) =>  response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error:", error));
  }, []);

  if (!data) {
    return <div className={styles.home}>Loading...</div>;
  }

  return (
    <>
    <div className={styles.home}>
      <h1>{data.welcome}</h1>
      <p>
        {data.home_text}
      </p>
    </div>
    <div className={styles.posts}>
      {/* Posts Here */}
    </div>
    </>
  );
}

export default Home;