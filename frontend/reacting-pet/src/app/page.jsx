import styles from "./Home.module.css";

function Home() {
  return (
    <div className="homeBg">
      <div className={styles.home}>
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
