import { useState, useEffect } from "react";
import styles from "./Navbar.module.css";
import logo from "../assets/logo.png";
import Auth from "../Auth/Auth.jsx";

function Navbar() {
  const [loginScreen, setLoginScreen] = useState(false);
  const [loginWrapper, setLoginWrapper] = useState(false);
  const [closingSignal, setClosingSignal] = useState(false);

  const LoginNow = () => {
    setLoginScreen(true);
    setTimeout(() => {
      setLoginWrapper(true);
    }, 0);
    setTimeout(() => {
      setClosingSignal(false);
    }, 200);
  };
  const CloseLogin = () => {
    setClosingSignal(true);
    setTimeout(() => {
      setLoginWrapper(false);
    }, 0);
    setTimeout(() => {
      setLoginScreen(false);
    }, 500);
  };

  return (
    <>
      <div className={styles.navbar}>
        <a href="/" className={styles.logo}>
          <img src={logo} />
        </a>
        <div className={styles.links}>
          <a href="/">Home Page</a>
          <a href="/">Search</a>
          <a className={styles.loginBtn} onClick={() => LoginNow()}>
            Login
          </a>
        </div>
      </div>
      {loginScreen && (
        <div
          className={loginWrapper ? "loginWrapper active" : "loginWrapper"}
          onClick={() => CloseLogin()}
        >
          {/* Prevent click events inside the box from closing it */}
          <div
            className="loginModalContent"
            onClick={(e) => e.stopPropagation()}
          >
            <Auth closingSignal={closingSignal} />
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;
