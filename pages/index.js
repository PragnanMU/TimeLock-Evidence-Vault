import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [ipfsHash, setIpfsHash] = useState("");

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });
    
    const data = await res.json();
    setIpfsHash(data.ipfs_hash);
  };

  return (
    <div>
      <h1>TimeLock Evidence Vault</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload Evidence</button>

      {ipfsHash && <p>IPFS Hash: {ipfsHash}</p>}
    </div>
  );
}
