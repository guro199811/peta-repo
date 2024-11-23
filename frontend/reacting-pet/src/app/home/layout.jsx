import styles from "./HomePage.module.css";
import Image from "next/image";
import Link from "next/link";

function HomePageLayout({ children}) {
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
