import React, { useContext, useEffect, useState } from "react";
import {
  collection,
  query,
  where,
  getDocs,
  setDoc,
  doc,
  updateDoc,
  serverTimestamp,
  getDoc,
} from "firebase/firestore";
import { db } from "../firebase";
import { AuthContext } from "../context/AuthContext";
const Search = () => {
  const [username, setUsername] = useState("");
  const [user, setUser] = useState(null);
  const [err, setErr] = useState(false);

  const { currentUser } = useContext(AuthContext);

  const [ownerPublicKeyRSA, setOwnerPublickeyRSA] = useState();
  const [ownerPublicKeyDSA, setOwnerPublickeyDSA] = useState();
  const [ownerPublicKeyEG, setOwnerPublickeyEG] = useState();
  const [ownerPublicKeyRCS, setOwnerPublickeyRCS] = useState();

  const [loading, setLoading] = useState(false);

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

  const handleSearch = async () => {
    const q = query(
      collection(db, "users"),
      where("displayName", "==", username)
    );

    try {
      const querySnapshot = await getDocs(q);
      querySnapshot.forEach((doc) => {
        setUser(doc.data());
      });
    } catch (err) {
      setErr(true);
    }
  };

  const handleKey = (e) => {
    e.code === "Enter" && handleSearch();
  };

  const handleSelect = async () => {
    //check whether the group(chats in firestore) exists, if not create

    const combinedId =
      currentUser.uid > user.uid
        ? currentUser.uid + user.uid
        : user.uid + currentUser.uid;
    try {
      const res = await getDoc(doc(db, "chats", combinedId));

      if (!res.exists()) {
        //create a chat in chats collection
        await setDoc(doc(db, "chats", combinedId), { messages: [] });

        //create user chats
        await updateDoc(doc(db, "userChats", currentUser.uid), {
          [combinedId + ".userInfo"]: {
            uid: user.uid,
            displayName: user.displayName,
            photoURL: user.photoURL,
            publicKeyRSA: user.publicKeyRSA,
            publicKeyDSA: user.publicKeyDSA,
            publicKeyEG: user.publicKeyEG,
            publicKeyRCS: user.publicKeyRCS,
          },
          [combinedId + ".date"]: serverTimestamp(),
        });

        await updateDoc(doc(db, "userChats", user.uid), {
          [combinedId + ".userInfo"]: {
            uid: currentUser.uid,
            displayName: currentUser.displayName,
            photoURL: currentUser.photoURL,
            publicKeyRSA: ownerPublicKeyRSA,
            publicKeyDSA: ownerPublicKeyDSA,
            publicKeyEG: ownerPublicKeyEG,
            publicKeyRCS: ownerPublicKeyRCS,
          },
          [combinedId + ".date"]: serverTimestamp(),
        });
      }
    } catch (err) {
      console.log(err);
    }

    setUser(null);
    setUsername("");
  };
  return loading ? (
    <div>Loading</div>
  ) : (
    <div className="search">
      <div className="searchForm">
        <input
          type="text"
          placeholder="Find a user"
          onKeyDown={handleKey}
          onChange={(e) => setUsername(e.target.value)}
          value={username}
        />
      </div>
      {err && <span>User not found!</span>}
      {user && (
        <div className="userChat" onClick={handleSelect}>
          <img src={user.photoURL} alt="" />
          <div className="userChatInfo">
            <span>{user.displayName}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Search;
