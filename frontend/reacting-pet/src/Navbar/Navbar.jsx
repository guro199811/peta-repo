import styles from "./Navbar.module.css";
import logo from '../assets/logo.png';

function Navbar() {
  return (
    <div className={styles.navbar}>
      <a href="/" className={styles.logo}><img src={logo} /></a>
      <div className={styles.links}>
        <a href="/">Home Page</a>
        <a href="/">Search</a>
        <a href="/" className={styles.loginBtn}>Login</a>
      </div>
    </div>
  );
}

export default Navbar;
