import { useRef, useState } from "react";
import axios from "axios";
import Webcam from 'react-webcam';

function App() {
  const [password, setPassword] = useState("");
  const webcamRef = useRef(null);
  const [email, setEmail] = useState("");
  const [imageSrc, setImageSrc] = useState(null);

  const capture = () => {
    const image = webcamRef.current.getScreenshot();
      console.log("Captured Image:", image);
    setImageSrc(image);
  };

 const handleLogin = async () => {
  try {
    const res = await axios.post("http://localhost:5001/login", {
      email: email,
      password: password,
      image: imageSrc,
    });

    console.log("Full Response:", res.data);

    if (res.data.success) {
      localStorage.setItem("token", res.data.token);  // 🔥 STORE TOKEN
      alert("Login Successful");
    } else {
      alert(res.data.status);
    }

  } catch (err) {
    console.error(err);
  }
};

  const handleRegister = async () => {
    try {
      const res = await axios.post("http://localhost:5001/register", {
        email: email,
        password:password,
        image: imageSrc,
      });
      alert(res.data.status);
    } catch (err) {
      console.error(err);
    }
  };
  const fetchProfile = async () => {
  try {
    const token = localStorage.getItem("token");

    const res = await axios.get("http://localhost:5001/profile", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log("Profile Data:", res.data);
    alert(res.data.message);

  } catch (err) {
    console.error(err);
    alert("Unauthorized");
  }
};

  return (
    <div style={{ padding: "40px" }}>
      <h2>Biometric Auth Login</h2>

      <input
        type="email"
        placeholder="Enter email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <br /> <br />
      <input
  type="password"
  placeholder="Enter password"
  onChange={(e) => setPassword(e.target.value)}
/>

      <br /><br /> <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={300}
      />
      <br /><br />
      <button onClick={capture}>Capture Photo</button>
       <br /><br />
       {imageSrc && (
        <img src={imageSrc} alt="Captured" width="200" />
      )}

      <br /><br />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>

    </div>
  );
}
export default App;