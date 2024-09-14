import { useState, useEffect } from "react";
import { API_BASE_URL } from "../config/config.js";

const Auth = (props) => {
  const [isLogin, setIsLogin] = useState(true); // State to manage form visibility

  const toggleForm = () => {
    setIsLogin(!isLogin); // Toggle between login and register
  };

  // Usestate for phone prefixes
  const [phonePrefixes, setPhonePrefixes] = useState({
    prefixes: [
      {
        prefix: "+995",
        nums: 9,
        icon: "🇬🇪",
      },
    ],
  });

  useEffect(() => {
    // Fetch Phone prefixes from API
    fetch(`${API_BASE_URL}/auth/register`)
      .then((response) => response.json()) // Return parsed JSON
      .then((data) => {
        setPhonePrefixes(data);
        console.log("data: ", data); // Logging the data for inspection
      })
      .catch((error) => console.error("Error:", error));
  }, []);

  const showPassword = () => {
    const passwordInput = document.getElementById("password");
    passwordInput.type =
      passwordInput.type === "password" ? "text" : "password";
  };

  return (
    <div className={props.closingSignal? "authBox close" : "authBox"}>
      <div className={`auth login ${isLogin ? "visible" : "hidden"}`}>
        <form className="login-form">
          <h1>Sign in</h1>
          <input type="email" placeholder="Email" required />
          <input
            type="password"
            placeholder="Password"
            id="password"
            required
          />
          <div>
            <input
              type="checkbox"
              id="show-password-login"
              className="show-password-checkbox"
              onClick={() => {
                showPassword();
              }}
            />
            <label htmlFor="show-password-login">Show Password</label>
            <a
              href="#"
              className="forgot-password"
              style={{
                float: "right",
                margin: "6px",
              }}
            >
              Forgot password?
            </a>
          </div>
          <a href="#" className="submit-button">
            Login
          </a>
        </form>
        <span className="switch-link" onClick={toggleForm}>
          Don't have an account? Register now!
        </span>
      </div>

      <div className={`auth register ${isLogin ? "hidden" : "visible"}`}>
        <form className="register-form">
          <h1>Create Account</h1>
          <input type="text" placeholder="First Name" required />
          <input type="text" placeholder="Last Name" required />
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />
          <input type="password" placeholder="Confirm Password" required />
          <div>
            <input
              type="checkbox"
              id="show-password-register"
              className="show-password-checkbox"
            />
            <label htmlFor="show-password-register">Show Password</label>
          </div>
          <div className="phone-input">
            <select
              name="country_code"
              id="countryCode"
              className="phone-select"
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
              required
            />
          </div>
          <a href="#" className="submit-button">
            Register
          </a>
        </form>
        <span className="switch-link" onClick={toggleForm}>
          Already have an account? Sign in
        </span>
      </div>
    </div>
  );
};

export default Auth;
