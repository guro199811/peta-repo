"use client"

import { useState } from "react";
import styles from "./Navbar.module.css";
import logo from "../../../public/assets/logo.png";
import Auth from "./Auth/Auth.jsx";
import { useToken } from "../Token/Token.jsx";
import Link from "next/link"


function Navbar() {
  const { userToken, setUserToken } = useToken();

  const [loginScreen, setLoginScreen] = useState(false);
  const [loginWrapper, setLoginWrapper] = useState(false);
  const [closingSignal, setClosingSignal] = useState(false);

  const openLogin = () => {
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

  const logOut = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUserToken(null);
  };

  return (
    <>
      <div className={styles.navbar}>
        <Link href="/" className={styles.logo}>
          <img src={logo.src} />
        </Link>
        <div className={styles.links}>
          <Link href="/">Home Page</Link>
          <Link href="/">Search</Link>
          <Link href="/about">About</Link>
          {userToken ? ( 
            <a className={styles.logoutBtn} onClick={() => logOut()}>Log-Out</a>
          ) : (
            <a className={styles.loginBtn} onClick={() => openLogin()}>
              Login
            </a>
          )}
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
