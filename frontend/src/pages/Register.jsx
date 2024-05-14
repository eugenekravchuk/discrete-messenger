import React, { useEffect, useState } from "react";
import Add from "../img/addAvatar.png";
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { auth, db, storage } from "../firebase";
import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { doc, setDoc } from "firebase/firestore";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

const Register = () => {
  const [err, setErr] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [myPublicKeyRSA, setMyPublicKeyRSA] = useState(null);
  const [myPrivateKeyRSA, setMyPrivateKeyRSA] = useState(null);
  const [myPublicKeyElGamal, setMyPublicKeyElGamal] = useState(null);
  const [myPrivateKeyElGamal, setMyPrivateKeyElGamal] = useState(null);
  const [myPublicKeyRCS, setMyPublicKeyRCS] = useState(null);
  const [myPrivateKeyRCS, setMyPrivateKeyRCS] = useState(null);
  const [myPublicKeyDSA, setMyPublicKeyDSA] = useState(null);
  const [myPrivateKeyDSA, setMyPrivateKeyDSA] = useState(null);

  useEffect(() => {
    const generateKeys = async () => {
      try {
        setLoading(true);
        // RSA
        const response_rsa = await axios.get(
          "http://3.120.205.90/generate_keys_rsa"
        );
        setMyPublicKeyRSA([response_rsa.data.public_key, response_rsa.data.n]);
        setMyPrivateKeyRSA(response_rsa.data.private_key);

        // ElGamal
        const response_eg = await axios.get(
          "http://3.120.205.90/generate_keys_eg"
        );
        setMyPublicKeyElGamal(response_eg.data.public_key);
        setMyPrivateKeyElGamal(response_eg.data.private_key);

        //RCS
        const response_rcs = await axios.get(
          "http://3.120.205.90/generate_keys_rcs"
        );
        setMyPublicKeyRCS(response_rcs.data.public_key);
        setMyPrivateKeyRCS(response_rcs.data.private_key);

        const response_dsa = await axios.get(
          "http://3.120.205.90/generate_keys_dsa"
        );
        setMyPublicKeyDSA(response_dsa.data.public_key);
        setMyPrivateKeyDSA(response_dsa.data.private_key);
      } catch (error) {
        console.error("Error generating keys:", error);
      } finally {
        setLoading(false);
      }
    };
    generateKeys();
  }, []);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    const displayName = e.target[0].value;
    const email = e.target[1].value;
    const password = e.target[2].value;
    const file = e.target[3].files[0];

    try {
      //Create user
      const res = await createUserWithEmailAndPassword(auth, email, password);

      //Create a unique image name
      const date = new Date().getTime();
      const storageRef = ref(storage, `${displayName + date}`);

      localStorage.setItem("privateKeyRSA", JSON.stringify(myPrivateKeyRSA));

      localStorage.setItem("privateKeyDSA", JSON.stringify(myPrivateKeyDSA));

      localStorage.setItem("privateKeyEG", JSON.stringify(myPrivateKeyElGamal));

      localStorage.setItem("privateKeyRCS", JSON.stringify(myPrivateKeyRCS));

      await uploadBytesResumable(storageRef, file).then(() => {
        getDownloadURL(storageRef).then(async (downloadURL) => {
          try {
            await updateProfile(res.user, {
              displayName,
              photoURL: downloadURL,
            });
            await setDoc(doc(db, "users", res.user.uid), {
              uid: res.user.uid,
              displayName,
              email,
              photoURL: downloadURL,
              publicKeyRSA: myPublicKeyRSA,
              publicKeyDSA: myPublicKeyDSA,
              publicKeyEG: myPublicKeyElGamal,
              publicKeyRCS: myPublicKeyRCS,
            });

            await setDoc(doc(db, "userChats", res.user.uid), {});
            navigate("/");
          } catch (err) {
            console.log(err);
            setErr(true);
            setLoading(false);
          }
        });
      });
    } catch (err) {
      setErr(true);
      setLoading(false);
    }
  };

  return loading ? (
    <div>Loading</div>
  ) : (
    <div className="formContainer">
      <div className="formWrapper">
        <span className="logo">Discrete Chat</span>
        <span className="title">Register</span>
        <form onSubmit={handleSubmit}>
          <input required type="text" placeholder="display name" />
          <input required type="email" placeholder="email" />
          <input required type="password" placeholder="password" />
          <input required style={{ display: "none" }} type="file" id="file" />
          <label htmlFor="file">
            <img src={Add} alt="" />
            <span>Add an avatar</span>
          </label>
          <button disabled={loading}>Sign up</button>
          {loading && "Uploading and compressing the image please wait..."}
          {err && <span>Something went wrong</span>}
        </form>
        <p>
          You do have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
