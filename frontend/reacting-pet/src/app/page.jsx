import styles from "./MainPage.module.css";
import Image from "next/image";

function MainPage() {
  return (
    <div
      className="absolute w-full h-full bg-cover 
    bg-no-repeat bg-center bg-fixed z-0 items-center justify-center "
    >
      <Image
        src="/assets/main-bg.jpg"
        alt="Background Image"
        layout="fill"
        objectFit="cover"
        priority
      />
      <div
        className={`${styles.main} relative flex flex-col 
      items-center justify-center h-auto
      text-black font-serif bg-slate-50 bg-opacity-80 backdrop-blur-sm drop-shadow-2xl
        shadow-current rounded-xl z-30`}
      >
        <h1>Welcome to our website!</h1>
        <p className="pl-2 pr-2 text-center text-balance">
          Our website is created for your lovely pets and they're veterinary
          care needs.
        </p>
      </div>
      <div className={styles.posts}>{/* Posts Here */}</div>
    </div>
  );
}

export default MainPage;
