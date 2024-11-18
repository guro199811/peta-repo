import React, { createContext, useContext, useState, useEffect } from "react";

/* 
Expected Token structure is as follows:

{
  "access_token": "TOKEN",
  "message": "Login successful",
  "refresh_token": "REFRESH TOKEN",
  "token_type": "Bearer"
}

Provides access to tokens in all child components
with virtual DOM capabilities
*/



const TokenContext = createContext();

// Helper function to check token expiration
function isTokenExpired(token) {
  try {
    // Decoding the payload from provided token
    const { exp } = JSON.parse(atob(token.split(".")[1]));
    return Date.now() >= exp * 1000; // Check if current time >= expiration time
  } catch (error) {
    console.error("Invalid token format:", error);
    return true;
  }
}

// Hypothetical function to refresh tokens using the refresh token
// TODO: might not work as expected
const refreshAuthToken = async (refreshToken) => {
  try {
    const response = await fetch("/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) throw new Error("Failed to refresh token");
    return await response.json();
  } catch (error) {
    console.error("Error refreshing token:", error);
    return null;
  }
};

export function TokenProvider({ children }) {
  const [userToken, setUserToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize tokens from localStorage on app load
  useEffect(() => {
    try {
      const storedAccessToken = localStorage.getItem("access_token");
      const storedRefreshToken = localStorage.getItem("refresh_token");

      if (storedAccessToken) {
        if (!isTokenExpired(storedAccessToken)) {
          setUserToken({
            access_token: storedAccessToken,
            refresh_token: storedRefreshToken,
          });
        } else if (storedRefreshToken) {
          // Refreshing token if access token is expired
          refreshAuthToken(storedRefreshToken).then((newTokens) => {
            if (newTokens) {
              setUserToken(newTokens);
              localStorage.setItem("access_token", newTokens.access_token);
              localStorage.setItem("refresh_token", newTokens.refresh_token);
            } else {
              localStorage.removeItem("access_token");
              localStorage.removeItem("refresh_token");
            }
          });
        } else {
          localStorage.removeItem("access_token");
        }
      }
    } catch (error) {
      console.error("Error accessing localStorage:", error);
    } finally {
      setIsLoading(false); // Mark as done loading
    }
  }, []);

  // Automatically refreshes tokens before expiration
  useEffect(() => {
    if (!userToken?.access_token) return;

    const { exp } = JSON.parse(atob(userToken.access_token.split(".")[1]));
    // Refresh 1 minute before expiration
    const timeUntilExpiration = exp * 1000 - Date.now() - 60000;

    const timeoutId = setTimeout(async () => {
      console.log("Refreshing")
      const newTokens = await refreshAuthToken(userToken.refresh_token);
      if (newTokens) {
        setUserToken(newTokens);
        localStorage.setItem("access_token", newTokens.access_token);
        localStorage.setItem("refresh_token", newTokens.refresh_token);
      } else {
        setUserToken(null);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      }
    }, Math.max(0, timeUntilExpiration));

    return () => clearTimeout(timeoutId); // Cleanup timeout on unmount
  }, [userToken]);

  // Keeps localStorage synchronized with userToken
  useEffect(() => {
    if (userToken) {
      localStorage.setItem("access_token", userToken.access_token);
      localStorage.setItem("refresh_token", userToken.refresh_token);
    } else {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  }, [userToken]);

  // Shows a loading placeholder until token initialization is complete (its optional)
  // TODO: revisit this (maybe add some animations?)
  if (isLoading) {
    return <div className="token-loading">Loading...</div>;
  }

  return (
    <TokenContext.Provider value={{ userToken, setUserToken }}>
      {children}
    </TokenContext.Provider>
  );
}

// Hook to use the token context
export function useToken() {
  return useContext(TokenContext);
}
