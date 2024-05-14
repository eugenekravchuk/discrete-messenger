import React, { useContext, useEffect, useState } from "react";
import Img from "../img/img.png";
import { AuthContext } from "../context/AuthContext";
import { ChatContext } from "../context/ChatContext";
import {
  arrayUnion,
  doc,
  serverTimestamp,
  Timestamp,
  updateDoc,
  getDoc,
} from "firebase/firestore";
import { db, storage } from "../firebase";
import { v4 as uuid } from "uuid";
import { getDownloadURL, ref, uploadBytesResumable } from "firebase/storage";
import axios from "axios";

const Input = () => {
  const [text, setText] = useState("");
  const [img, setImg] = useState(null);

  const { currentUser } = useContext(AuthContext);
  const { data } = useContext(ChatContext);
  const [ownerPublicKeyRSA, setOwnerPublickeyRSA] = useState();
  const [ownerPublicKeyDSA, setOwnerPublickeyDSA] = useState();
  const [ownerPublicKeyEG, setOwnerPublickeyEG] = useState();
  const [ownerPublicKeyRCS, setOwnerPublickeyRCS] = useState();
  const [signature, setSignature] = useState();
  const [loading, setLoading] = useState(false);
  const [selectedOption, setSelectedOption] = useState("RSA");

  useEffect(() => {
    // 1. Check if currentUser exists
    if (!currentUser || !currentUser.uid) {
      return; // Exit if currentUser is undefined
    }

    const fetchUserPublicKey = async (userId) => {
      try {
        setLoading(true);
        const userDocRef = doc(db, "users", userId);
        const userDocSnap = await getDoc(userDocRef); // Get the document snapshot

        if (userDocSnap.exists()) {
          const userData = userDocSnap.data();
          // 2. Check if publicKey exists in userData
          if (userData.publicKeyRSA) {
            setOwnerPublickeyRSA(userData.publicKeyRSA);
          }

          if (userData.publicKeyDSA) {
            setOwnerPublickeyDSA(userData.publicKeyDSA);
          }

          if (userData.publicKeyEG) {
            setOwnerPublickeyEG(userData.publicKeyEG);
          }

          if (userData.publicKeyRCS) {
            setOwnerPublickeyRCS(userData.publicKeyRCS);
          }
        } else {
          console.log("User document not found");
        }
      } catch (error) {
        console.error("Error fetching user public key:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserPublicKey(currentUser.uid);
  }, [currentUser?.uid]);

  const handleSend = async () => {
    let encryptedOwner, encryptedSender;

    if (selectedOption === "RSA") {
      const response1 = await axios.get("http://3.120.205.90/encrypt_rsa", {
        params: {
          message: text,
          public_key: data.user.publicKeyRSA[0],
          n: data.user.publicKeyRSA[1],
        },
      });
      encryptedSender = response1.data.encrypted_message;
      const response2 = await axios.get("http://3.120.205.90/encrypt_rsa", {
        params: {
          message: text,
          public_key: ownerPublicKeyRSA[0],
          n: ownerPublicKeyRSA[1],
        },
      });
      encryptedOwner = response2.data.encrypted_message;
    } else if (selectedOption === "ElGamal") {
      const response1 = await axios.get("http://3.120.205.90/encrypt_eg", {
        params: {
          message: text,
          public_key1: data.user.publicKeyEG[0],
          public_key2: data.user.publicKeyEG[1],
          public_key3: data.user.publicKeyEG[2],
        },
      });
      encryptedSender = response1.data.encrypted_message;
      const response2 = await axios.get("http://3.120.205.90/encrypt_eg", {
        params: {
          message: text,
          public_key1: ownerPublicKeyEG[0],
          public_key2: ownerPublicKeyEG[1],
          public_key3: ownerPublicKeyEG[2],
        },
      });
      encryptedOwner = response2.data.encrypted_message;
    } else if (selectedOption === "RCS") {
      const response1 = await axios.get("http://3.120.205.90/encrypt_rcs", {
        params: {
          message: text,
          public_key: data.user.publicKeyRCS,
        },
      });
      encryptedSender = response1.data.encrypted_message;
      const response2 = await axios.get("http://3.120.205.90/encrypt_rcs", {
        params: {
          message: text,
          public_key: ownerPublicKeyRCS,
        },
      });
      encryptedOwner = response2.data.encrypted_message;
    }

    // const responce_dsa = await axios.get("/sign_dsa", {
    //   params: {
    //     message: text,
    //     public_key1: ownerPublicKeyDSA[0],
    //     public_key2: ownerPublicKeyDSA[1],
    //     public_key3: ownerPublicKeyDSA[2],
    //     public_key4: ownerPublicKeyDSA[3],
    //     private_key: JSON.parse(localStorage.getItem("privateKeyDSA")),
    //   },
    // });
    setSignature("one");

    if (img) {
      const storageRef = ref(storage, uuid());

      await uploadBytesResumable(storageRef, img).then(() => {
        getDownloadURL(storageRef).then(async (downloadURL) => {
          try {
            await updateDoc(doc(db, "chats", data.chatId), {
              messages: arrayUnion({
                id: uuid(),
                encryptedSender,
                encryptedOwner,
                // signature,
                selectedOption,
                senderId: currentUser.uid,
                date: Timestamp.now(),
                img: downloadURL,
              }),
            });
          } catch (err) {
            console.log(err);
            setLoading(false);
          }
        });
      });
    } else {
      await updateDoc(doc(db, "chats", data.chatId), {
        messages: arrayUnion({
          id: uuid(),
          encryptedSender,
          encryptedOwner,
          // signature,
          selectedOption,
          senderId: currentUser.uid,
          date: Timestamp.now(),
        }),
      });
    }

    await updateDoc(doc(db, "userChats", currentUser.uid), {
      [data.chatId + ".lastMessageSender"]: encryptedSender,
      [data.chatId + ".lastMessageOwner"]: encryptedOwner,
      [data.chatId + ".lastMessageType"]: selectedOption,
      [data.chatId + ".date"]: serverTimestamp(),
    });

    await updateDoc(doc(db, "userChats", data.user.uid), {
      [data.chatId + ".lastMessageSender"]: encryptedSender,
      [data.chatId + ".lastMessageOwner"]: encryptedOwner,
      [data.chatId + ".lastMessageType"]: selectedOption,
      [data.chatId + ".date"]: serverTimestamp(),
    });

    setText("");
    setImg(null);
  };
  return loading ? (
    <div>Loading</div>
  ) : (
    <div className="input">
      <input
        type="text"
        placeholder="Type something..."
        onChange={(e) => setText(e.target.value)}
        value={text}
      />
      <div className="dropdown">
        <select
          value={selectedOption}
          onChange={(e) => setSelectedOption(e.target.value)}
        >
          <option value="RSA">RSA</option>
          <option value="ElGamal">ElGamal</option>
          <option value="RCS">RCS</option>
        </select>
      </div>
      &nbsp;
      <div className="send">
        <input
          type="file"
          style={{ display: "none" }}
          id="file"
          onChange={(e) => setImg(e.target.files[0])}
        />
        <label htmlFor="file">
          <img src={Img} alt="" />
        </label>
        <button onClick={handleSend} disabled={!text}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Input;
