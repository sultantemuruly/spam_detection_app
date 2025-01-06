import { useState } from 'react';
import api from './api';
import ClipLoader from "react-spinners/ClipLoader";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [emailText, setEmailText] = useState('');
  const [spamData, setSpamData] = useState({
    spam: "",
    ham: "", 
  });

  const handleChange = async (event) => {
    const { value } = event.target;
    setEmailText(value);
  };

  const handleSubmit = async (event) => {
    try {
      event.preventDefault();

      setSpamData({
        spam: '',
        ham: '',
      })
      
      setIsLoading(true);

      const response = await api.post('/email/predict', {"text": emailText});
      console.log(response.data);

      setSpamData({
        spam: Math.round(response.data.Spam * 100).toString(),
        ham: Math.round(response.data.Ham * 100).toString(),
      })
      setIsLoading(false);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <div className='flex justify-center items-center h-screen'>
        <form onSubmit={handleSubmit}>
          <div className=''>
            <h1 className="text-4xl font-bold">Spam Detector</h1>
            <label className='text-gray-500'>Enter your text below to check if it's spam</label>
            <div className='pt-4'>
              <textarea
                type="text"
                id="emailText"
                name="emailText"
                value={emailText}
                onChange={handleChange}
                className="border border-gray-300 p-2 rounded focus:outline-none focus:ring focus:ring-blue-300 w-[512px] h-36"
                placeholder="Paste email here..."
              />
            </div>
          </div>

          {spamData.spam !== '' ? 
            <div>
              <div>The probability that the message is spam is {spamData.spam} %</div>
            </div> : 
            <div className='flex justify-center'>
              <ClipLoader
                color={"#0081fd"}
                loading={isLoading}
                size={25}
                aria-label="Loading Spinner"
                data-testid="loader"
              />
            </div>
          }
          <div className='pt-6 flex justify-center'>
            <button type="submit" className='w-[164px] h-[48px] bg-gray-500 text-white rounded-lg hover:scale-105 hover:bg-blue-600 transition-all duration-100'>Check for Spam</button>
          </div>
        </form>
      </div>
      <footer className='text-center'>
      <p>
        Created by{' '}
        <a
          href="https://github.com/sultantemuruly"
          target="_blank"
          rel="noopener noreferrer"
          style={{ textDecoration: 'none', color: '#007bff' }}
        >
          @sultantemuruly
        </a>
      </p>
    </footer>
    </div>
  );
}

export default App;
