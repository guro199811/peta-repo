import styles from "./Home.module.css";
import Image from "next/image";
// import Image from "../../public/assets/main-bg.jpg"

function Home() {
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
        className={`${styles.home} relative flex flex-col 
      items-center justify-center h-auto
       text-black font-serif border border-black 
       bg-white/75 rounded-2xl backdrop-blur-sm z-50`}
      >
        <h1>Welcome to our website!</h1>
        <p>
          Our website is created for your lovely pets and they're veterinary
          care needs.
        </p>
      </div>
      <div className={styles.posts}>{/* Posts Here */}</div>
    </div>
  );
}

export default Home;
