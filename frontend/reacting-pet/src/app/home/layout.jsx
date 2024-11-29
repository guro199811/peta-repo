"use client"

import styles from "./HomePage.module.css";
import Image from "next/image";
import Link from "next/link";
import { useToken } from "@/components/Token/Token.jsx"
import { useEffect } from "react"
import { useRouter } from "next/navigation"; 

function HomePageLayout({ children}) {
  const { userToken } = useToken()
  const router = useRouter();

  useEffect(() => {
    if (!userToken) {
      // Redirect to login if no token
      router.push("/");
    }  
  }, [])

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
          <Link href="/home" className={styles.square_button}>Dashboard</Link>
          {/* TODO: later implement "my pet history" into my pets */}
          <Link href="/home/user-pets" className={styles.square_button}>My Pets</Link>
          <Link href="/home" className={styles.square_button}>Clinic</Link>
          <Link href="/home" className={styles.square_button}>Vet Numbers</Link>
        </div>
        <div className={styles.box_menu}>
            {children}
        </div>
      </div>
    </>
  );
}

export default HomePageLayout;
