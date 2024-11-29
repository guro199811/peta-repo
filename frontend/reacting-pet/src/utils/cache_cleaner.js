"use client";


/**
 * Clears specified cache items from localStorage.
 * 
 * @param {Object} options - The options object.
 * @param {string[]} [options.keep=[]] - An array of keys to retain in localStorage.
 * @param {string} [options.specific=""] - A specific key to remove from localStorage.
 * 
 * @returns {void}
 * 
 * @example
 * // Clear all except access_token and user_settings
 * clearCache({ keep: ["user_settings"] });
 * 
 * @example
 * // Clear a specific key
 * clearCache({ specific: "some_key" });
 *//**
 * Clears specified cache items from localStorage.
 * 
 * @param {Object} options - The options object.
 * @param {string[]} [options.keep=[]] - An array of keys to retain in localStorage.
 * @param {string} [options.specific=""] - A specific key to remove from localStorage.
 * 
 * @returns {void}
 * 
 * @example
 * // Clear all except access_token and user_settings
 * clearCache({ keep: ["user_settings"] });
 * 
 * @example
 * // Clear a specific key
 * clearCache({ specific: "some_key" });
 */
function clearCache({ keep = [], specific = "" } = {}) {
  if (!specific) {
    const keysToKeep = ["access_token", "refresh_token", ...keep];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (!keysToKeep.includes(key)) {
        localStorage.removeItem(key);
        i--;
      }
    }
  } else {
    localStorage.removeItem(specific);
  }
}

export default clearCache;
