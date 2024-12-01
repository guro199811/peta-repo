function getSubFromJWT(token) {
  const payload = token.split(".")[1];
  const decodedPayload = JSON.parse(atob(payload));
  return decodedPayload.sub;
}

export default getSubFromJWT;
