"use client";

import styles from "./HomePage.module.css";
import Image from "next/image";
import { useEffect } from "react";
import { useToken } from "@/components/Token/Token.jsx";
import { useRouter } from "next/navigation";

function HomePage() {
  const { userToken } = useToken();
  const router = useRouter();

  // if user is not logged in throw 404
  useEffect(() => {
    if (!userToken) {
      // Redirect to login if no token
      router.push("/not_found");
    }
  }, [userToken, router]);

  if (!userToken) {
    return (
      <div className="flex w-full h-full text-center justify-center
      items-center text-black font-medium font-serif">
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
          <a className={styles.square_button}>My Pets</a>
          {/* TODO: later implement "my pet history" into my pets */}
          <a className={styles.square_button}>My Pet History</a>
          <a className={styles.square_button}>Clinic Map</a>
          <a className={styles.square_button}>Vet Phone Numbers</a>
        </div>
        <div className={styles.box_menu}></div>
      </div>
    </>
  );
}

export default HomePage;
