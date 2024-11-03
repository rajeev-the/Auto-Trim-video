/* eslint-disable no-unused-vars */
import  { useState } from 'react';
import axios from 'axios';
import "./App.css"
import { AiOutlineLoading3Quarters } from "react-icons/ai";



function App() {
  const [id, setId] = useState('');
  
  const [file, setFile] = useState(null); // State to store the selected file
  const [response, setResponse] = useState('');
  const [url,setUrl ] = useState("");
 
  const [load,setLoad] = useState(false);
 


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoad(true)

    // Create a FormData object to send form data along with the file
    const formData = new FormData();
    formData.append('id', id);
    
    formData.append('file', file); // Add the selected file to the FormData

    try {
      // Make POST request using Axios
      const res = await axios.post('http://localhost:8000/api/data/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set content type to multipart for file upload
        },
      });
     
      setResponse(res.data.message);
      setLoad(false)
      setUrl(`http://localhost:8000/api/download/${id}.mp4`)
      
    } catch (err) {
      console.error(err);
      setResponse('Error sending data');
    }
  };

  

  return (
    <div className="App">
      <h1>Video Trim </h1>

         <h3> 
         keyword(&quot;start triming&quot;,&quot;end triming&quot; )
          </h3>  
        
        <loadingpage/>
      
      <div className='main'>
      

      <form className='form' onSubmit={handleSubmit}>
        <div>
          <label>ID Youtube:</label>
          <input 
            type="text" 
            value={id} 
            onChange={(e) => setId(e.target.value)} 
            required 
          />
        </div>
       
        <div>
          <label>Upload File:</label>
          <input 
            type="file" 
            onChange={(e) => setFile(e.target.files[0])} 
            required 
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p>{response}</p>
     
     

{
  load ? <AiOutlineLoading3Quarters /> 
  : url.length == 0 
   ? "" :<div className='btn'> <a href={url}>Dowloading</a>  </div>
}
      
      
     

      


      </div>
     
    </div>
  );
}

export default App;
