import React, { useContext, useEffect, useRef, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { db } from "../firebase";
import { doc, getDoc } from "firebase/firestore";
import { ChatContext } from "../context/ChatContext";
import axios from "axios";

const Message = ({ message }) => {
  const { currentUser } = useContext(AuthContext);
  const { data } = useContext(ChatContext);
  const ref = useRef();
  const [decryptedText, setDecryptedText] = useState();
  const [loading, setLoading] = useState(false);
  const [verified, setVerified] = useState("pending");
  let senderDataNew;

  useEffect(() => {
    const fetchPublicKey = async () => {
      try {
        setLoading(true);
        const userDocRef = doc(db, "users", currentUser.uid);
        const senderDocRef = doc(db, "users", message.senderId);
        const userDocSnap = await getDoc(userDocRef);
        const senderDocSnap = await getDoc(senderDocRef);

        if (userDocSnap.exists) {
          const userData = userDocSnap.data();
          const senderData = senderDocSnap.data();
          senderDataNew = senderData;
          const publicKeyEG = userData.publicKeyEG;
          const publicKeyRCS = userData.publicKeyRCS;
          const publicKeyRSA = userData.publicKeyRSA;

          if (!decryptedText) {
            let decryptedMessage;

            switch (message.selectedOption) {
              case "RSA":
                decryptedMessage = await messageDecryptRSA(
                  message,
                  publicKeyRSA
                );
                break;
              case "ElGamal":
                decryptedMessage = await messageDecryptEG(message, publicKeyEG);
                break;
              case "RCS":
                decryptedMessage = await messageDecryptRCS(
                  message,
                  publicKeyRCS
                );
                break;
              default:
                break;
            }
            setDecryptedText(decryptedMessage);
          } else {
            if (message.senderId === currentUser.uid) {
              setVerified("verified");
            } else {
              const publicKeyDSA = senderDataNew.publicKeyDSA;
              const response_dsa = await axios.get(
                "http://3.120.205.90/verify_dsa",
                {
                  params: {
                    public_key1: publicKeyDSA[0],
                    public_key2: publicKeyDSA[1],
                    public_key3: publicKeyDSA[2],
                    public_key4: publicKeyDSA[3],
                    signature1: message.signature[0],
                    signature2: message.signature[1],
                    message: decryptedText,
                  },
                }
              );
              if (response_dsa.data.verified) {
                setVerified("verified");
              } else {
                setVerified("not verified");
              }
            }
          }
        } else {
          console.log("User document not found");
        }
      } catch (error) {
        console.error("Error fetching public key:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPublicKey();
    ref.current?.scrollIntoView({ behavior: "smooth" });
  }, [message]);

  const messageDecryptRSA = async (message, publicKey) => {
    let encryptedMessage;
    if (message.senderId === currentUser.uid) {
      encryptedMessage = message.encryptedOwner;
    } else {
      encryptedMessage = message.encryptedSender;
    }
    const response3 = await axios.get("http://3.120.205.90/decrypt_rsa", {
      params: {
        encrypted_message: encryptedMessage,
        n: publicKey[1],
        private_key: JSON.parse(localStorage.getItem("privateKeyRSA")),
      },
    });
    return response3.data.decrypted_message;
  };

  const messageDecryptEG = async (message, publicKey) => {
    let encryptedMessage;
    if (message.senderId === currentUser.uid) {
      encryptedMessage = message.encryptedOwner;
    } else {
      encryptedMessage = message.encryptedSender;
    }
    const response3 = await axios.get("http://3.120.205.90/decrypt_eg", {
      params: {
        encrypted_message1: encryptedMessage[0],
        encrypted_message2: encryptedMessage[1],
        public_key1: publicKey[0],
        public_key2: publicKey[1],
        public_key3: publicKey[2],
        private_key: JSON.parse(localStorage.getItem("privateKeyEG")),
      },
    });
    return response3.data.decrypted_message;
  };

  const messageDecryptRCS = async (message, publicKey) => {
    let encryptedMessage;
    if (message.senderId === currentUser.uid) {
      encryptedMessage = message.encryptedOwner;
    } else {
      encryptedMessage = message.encryptedSender;
    }
    const response3 = await axios.get("http://3.120.205.90/decrypt_rcs", {
      params: {
        encrypted_message: encryptedMessage,
        private_key1: JSON.parse(localStorage.getItem("privateKeyRCS"))[0],
        private_key2: JSON.parse(localStorage.getItem("privateKeyRCS"))[1],
        public_key: publicKey,
      },
    });
    return response3.data.decrypted_message;
  };

  return loading ? (
    <div>Loading</div>
  ) : (
    <div
      ref={ref}
      className={`message ${message.senderId === currentUser.uid && "owner"}`}
    >
      <div className="messageInfo">
        <img
          src={
            message.senderId === currentUser.uid
              ? currentUser.photoURL
              : data.user.photoURL
          }
          alt=""
        />
        <span>verified</span>
        <span>Type: {message.selectedOption}</span>
      </div>
      <div className="messageContent">
        <p>{decryptedText}</p>
        {message.img && <img src={message.img} alt="" />}
      </div>
    </div>
  );
};

export default Message;
