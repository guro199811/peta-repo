"use client";

import { useState, useEffect } from "react";
import { API_BASE_URL } from "@/constants/config/config.js";
import { useToken } from "../../Token/Token.jsx";
import styles from "./Auth.module.css";

const Auth = (props) => {
  const { setUserToken } = useToken();

  // State to manage form visibility
  const [isLogin, setIsLogin] = useState(true);
  // Toggle between login and register
  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  // Usestate for phone prefixes (+Some Data incase fetch fails).
  const [phonePrefixes, setPhonePrefixes] = useState({
    prefixes: [
      {
        prefix: "+995",
        nums: 9,
        icon: "🇬🇪",
      },
    ],
  });

  // Gethering user data in state
  const [loginData, setLoginData] = useState({
    mail: "",
    password: "",
  });

  const [registerData, setRegisterData] = useState({
    name: "",
    lastname: "",
    password: "",
    repeat_password: "",
    mail: "",
    prefix: "+995", // Prefix predefined because it would does not require onchange event
    phone: "",
  });

  const handleLoginData = (e) => {
    const { name, value } = e.target;
    setLoginData({ ...loginData, [name]: value });
  };

  const handleRegisterData = (e) => {
    const { name, value } = e.target;
    setRegisterData({ ...registerData, [name]: value });
  };

  useEffect(() => {
    // Fetch Phone prefixes from API
    fetch(`${API_BASE_URL}/auth/register`)
      .then((response) => response.json()) // Return parsed JSON
      .then((data) => {
        setPhonePrefixes(data);
        // console.log("data: ", data); // Logging the data for inspection
      })
      .catch((error) => console.error("Error:", error));
  }, []);

  const showPassword = () => {
    const passwordInput = document.getElementById("password");
    passwordInput.type =
      passwordInput.type === "password" ? "text" : "password";
  };

  const showRegisterPassword = () => {
    const passwordInput = document.getElementById("reg-password");
    const repeatPasswordInput = document.getElementById("reg-password-repeat");
    passwordInput.type =
      passwordInput.type === "password" ? "text" : "password";
    repeatPasswordInput.type =
      repeatPasswordInput.type === "password" ? "text" : "password";
  };

  // Authentification Section
  // Log-In
  const handleLogin = (event) => {
    event.preventDefault(); // Prevents default refreshing behavior
    // const urlEncodedData = new URLSearchParams(loginData).toString();
    // Send login request to API
    console.log(loginData);
    fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    })
      .then((response) => response.json())
      .then((data) => {
        // console.log("Login response => ", data)
        if (data.access_token){
          setUserToken(data);
        } else {
          alert(data.message)
        }
        // Force clicks element to close login
        document.querySelector(".loginWrapper").click();
      }) // Show error message
      .catch((error) => console.error("Error:", error));
  };

  const handleRegistration = (event) => {
    event.preventDefault(); // Prevents default refreshing behavior
    console.log(JSON.stringify(registerData));
    alert("Stop");
    fetch(`${API_BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Registration response => ", data);
        alert("Registration Successful");
        window.location.reload();
      })
      .catch((error) => alert(error.message));
  };

  return (
    <div
      className={`${styles.authBox} ${props.closingSignal ? styles.close : ""}`}
    >
      <div
        className={`${styles.auth} ${isLogin ? styles.login : styles.register}`}
      >
        <form className={styles.login_form} onSubmit={handleLogin}>
          <h1 className="text-center mb-6 text-2xl 
          font-serif font-bold">Sign in</h1>
          <input
            type="email"
            placeholder="Email"
            name="mail"
            value={loginData.mail}
            onChange={handleLoginData}
            required
          />
          <input
            type="password"
            placeholder="Password"
            id="password"
            name="password"
            value={loginData.password}
            onChange={handleLoginData}
            required
          />
          <div>
            <input
              type="checkbox"
              id="show-password-login"
              className={styles.show_password_checkbox}
              onClick={() => {
                showPassword();
              }}
            />
            <label htmlFor="show-password-login">Show Password</label>
            <a
              className={styles.forgot_password}
              style={{
                float: "right",
                margin: "6px",
              }}
            >
              Forgot password?
            </a>
          </div>
          <button type="submit" className={styles.submit_button}>
            Login
          </button>
        </form>
        <span className={styles.switch_link} onClick={toggleForm}>
          Don't have an account? Register now!
        </span>
      </div>

      <div
        className={`${styles.auth} ${isLogin ? styles.register : styles.login}`}
      >
        <form className={styles.register_form} onSubmit={handleRegistration}>
          <h1 className="text-center mb-6 text-2xl 
          font-serif font-bold">Create Account</h1>
          <input
            type="text"
            placeholder="First Name"
            name="name"
            value={registerData.name}
            onChange={handleRegisterData}
            required
          />
          <input
            type="text"
            placeholder="Last Name"
            name="lastname"
            value={registerData.lastname}
            onChange={handleRegisterData}
            required
          />
          <input
            type="email"
            placeholder="Email"
            name="mail"
            value={registerData.mail}
            onChange={handleRegisterData}
            required
          />
          <input
            type="password"
            placeholder="Password"
            id="reg-password"
            name="password"
            value={registerData.password}
            onChange={handleRegisterData}
            required
          />
          <input
            type="password"
            placeholder="Confirm Password"
            id="reg-password-repeat"
            name="repeat_password"
            onChange={handleRegisterData}
            required
          />
          <div>
            <input
              type="checkbox"
              id="show-password-register"
              className={styles.show_password_checkbox}
              onClick={() => {
                showRegisterPassword();
              }}
            />
            <label htmlFor="show-password-register">Show Password</label>
          </div>
          <div className={styles.phone_input}>
            <select
              id="countryCode"
              className={styles.phone_select}
              name="prefix"
              value={registerData.prefix}
              onChange={handleRegisterData}
              required
            >
              {phonePrefixes.prefixes.map((prefix) => (
                <option key={prefix.prefix} value={prefix.prefix}>
                  {prefix.icon} {prefix.prefix}
                </option>
              ))}
            </select>
            <input
              type="number"
              id="phone"
              name="phone"
              minLength={9}
              maxLength={9}
              placeholder="Phone Number"
              value={registerData.phone}
              onChange={handleRegisterData}
              required
            />
          </div>
          <button type="submit" className={styles.submit_button}>
            Register
          </button>
        </form>
        <span className={styles.switch_link} onClick={toggleForm}>
          Already have an account? Sign in
        </span>
      </div>
    </div>
  );
};

export default Auth;
