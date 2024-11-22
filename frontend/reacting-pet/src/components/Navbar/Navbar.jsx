"use client";

import { useState } from "react";
import styles from "./Navbar.module.css";
import logo from "../../../public/assets/logo.png";
import Auth from "./Auth/Auth.jsx";
import { useToken } from "../Token/Token.jsx";
import Link from "next/link";

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

  // if (userToken) {
  //   CloseLogin();
  // }

  return (
    <>
      <div
        className={`${styles.navbar} flex justify-between w-full items-center
        h-16 bg-slate-100 bg-opacity-75 backdrop-blur-sm drop-shadow-2xl
        shadow-current rounded-xl z-40
        max-md:h-12`}
      >
        <Link
          href="/"
          className="
        flex float-left items-center justify-center max-w-24 max-h-24 ml-1 mt-3
        max-md:ml-4 max-md:scale-75"
        >
          <img draggable="false" src={logo.src} />
        </Link>
        <div
          className={`${styles.links} mb-1 float-right 
          max-sm:mb-1 max-sm:scale-50 max-sm:grid max-sm:grid-cols-2
          max-sm:min-w-48 text-center`}
        >
          {userToken && <Link href="/home">My Page</Link>}
          <Link href="/about">About</Link>
          {userToken ? (
            <a className={styles.logoutBtn} onClick={() => logOut()}>
              Logout
            </a>
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
