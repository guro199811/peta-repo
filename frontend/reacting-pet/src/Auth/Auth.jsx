import { useState } from "react";

import styles from "./Auth.module.css";
import { useAuth } from "../AuthContext.jsx"

function Auth({ onClose }) {

  const { setUserToken } = useAuth();

  const [loginBoxShow, setLoginBoxShow] = useState(true);
  const [registerBoxShow, setRegisterBoxShow] = useState(false);
  const [registerWrapper, setRegisterWrapper] = useState(false);

  const [loginFormData, setLoginFormData] = useState({
    username: '',
    password: '',
  });

  const [registerFormData, setRegisterFormData] = useState(
    {
      username: '',
      fullname: '',
      password: '',
      password_confirmation: ''
    }
  )


  const handleLoginChange = (event) => {
    const { name, value } = event.target;
    setLoginFormData({ ...loginFormData, [name]: value });
  };

  const handleLoginForm = async (event) => {
    event.preventDefault();

    try {
      const urlEncodedData = new URLSearchParams(loginFormData).toString();
      const response = await fetch('http://0.0.0.0:8000/auth/token', {
        method: 'POST',
        body: urlEncodedData,
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
          "Access-Control-Allow-Origin": "*"
        },
      });
      const data = await response.json();
      setUserToken(data);
      onClose();

    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  const handleRegisterChange = (event) => {
    const { name, value } = event.target;
    setRegisterFormData({ ...registerFormData, [name]: value });
  };

  const handleRegisterForm = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('http://0.0.0.0:8000/auth/register', {
        method: 'POST',
        body: JSON.stringify(registerFormData),
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
      });
      const data = await response.json();

    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  const handleLogin = () => {
    setLoginBoxShow(true);
    setRegisterBoxShow(false);
    setRegisterWrapper(false);
  };

  const handleRegister = () => {
    setLoginBoxShow(false);
    setRegisterBoxShow(true);
    setRegisterWrapper(true);
  };


  const showPasswordToggle = (e) => {
    const pass = document.getElementById('pass');
    e.target.checked ? pass.type = 'text' : pass.type = 'password';
  }

  const showPasswordToggleRegister = (e) => {
    const password = document.getElementById('password');
    const password2 = document.getElementById('repeatpassword')
    e.target.checked? password.type = 'text' : password.type = 'password';
    e.target.checked? password2.type = 'text' : password2.type = 'password';
  }


  return (
    <>
        <div className={`${styles.wrapper}
          ${registerWrapper ? styles.register : '' }`}>
          <span className={styles.iconClose} onClick={ onClose }>
          <i className='bx bx-x'></i>
          </span>

          <div className={`${styles.loginBox}
            ${loginBoxShow ? styles.active : ''}`}>
            <form onSubmit={handleLoginForm} method="POST">
              <h1 className={styles.title}>Login</h1>
              <div className={styles.inputBox}>
                <input
                  type="text"
                  placeholder="Username"
                  name="username"
                  value={loginFormData.username}
                  onChange={handleLoginChange}
                  required
                />
                <i className="bx bx-user"></i>
              </div>
              <div className={styles.inputBox}>
                <input
                  type="password"
                  placeholder="******"
                  name="password"
                  id="pass"
                  value={loginFormData.password}
                  onChange={handleLoginChange}
                  required
                />
                <i className="bx bx-lock-alt"></i>
              </div>
              <div className={styles.additionalSection}>
                <label>
                  <input type="checkbox" id="showPassword"
                  onClick={(e) => showPasswordToggle(e)} />
                  Reveal Password
                </label>
                <a href="/">Forgot password?</a>
              </div>
              <button className={styles.submitbtn} type="submit">
                Login
              </button>

              <div className={styles.logRegLink}>
                <p>
                  Don't have an account?
                  <a className={styles.registerLink} onClick={() => handleRegister()}>Register</a>
                </p>
              </div>
            </form>
          </div>

          <div className={`${styles.registerBox}
            ${registerBoxShow ? styles.active : ''}`}>
            <form onSubmit={handleRegisterForm} method="POST">
              <h1 className={styles.title}>Registration</h1>
              <div className={styles.inputBox}>
                <input
                  type="text"
                  placeholder="Username"
                  name="username"
                  value={registerFormData.username}
                  onChange={handleRegisterChange}
                  required
                />
                <i className="bx bx-user"></i>
              </div>
              <div className={styles.inputBox}>
                <input
                  type="text"
                  placeholder="Full Name"
                  name="fullname"
                  id="fullName"
                  value={registerFormData.fullname}
                  onChange={handleRegisterChange}
                  required
                />
                <i className='bx bx-user-check'></i>
              </div>
              <div className={styles.inputBox}>
                <input
                  type="password"
                  placeholder="Password"
                  name="password"
                  id="password"
                  value={registerFormData.password}
                  onChange={handleRegisterChange}
                  required
                />
                <i className="bx bx-lock-alt"></i>
              </div>
              <div className={styles.inputBox}>
                <input
                  type="password"
                  placeholder="Repeat Password"
                  name="password_confirmation"
                  id="repeatpassword"
                  value={registerFormData.password_confirmation}
                  onChange={handleRegisterChange}
                  required
                />
                <i className="bx bx-lock-alt"></i>
              </div>
              <div className={styles.additionalSection}>
                <label>
                  <input type="checkbox" id="revealPassword"
                  onClick={(e) => showPasswordToggleRegister(e)} />
                  Reveal Password
                </label>
              </div>
              <button className={styles.submitbtn} type="submit">
                Register
              </button>

              <div className={styles.logRegLink}>
                <p>
                  Already Have an Account?
                  <a className={styles.loginLink} onClick={() => handleLogin()}>Login</a>
                </p>
              </div>
            </form>
          </div>
        </div>
    </>
  );
}

export default Auth;
