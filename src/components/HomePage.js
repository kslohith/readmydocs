import React, { useState, useEffect } from 'react';
import Input from '@mui/joy/Input';
import Textarea from '@mui/joy/Textarea';
import Typography from '@mui/joy/Typography';
import Button from '@mui/joy/Button';

function HomePage() {
  const [getQuestion, setGetQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [withEva, setWithEva] = useState('');
  const [withoutEva, setWithoutEva] = useState('');

  const callEvaDb = () => {
    console.log(getQuestion);
    const apiUrl = `http://127.0.0.1:5000/getAnswerContext?question=${getQuestion}`;
    // Make a GET request to the API
    setIsLoading(true);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setWithEva(data); // Update the state with the fetched data
        setIsLoading(false); // Set loading to false
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
        setIsLoading(false); // Set loading to false in case of an error
      });
  }

  return (
        <>
        {isLoading && <Button loading variant="plain">
            Plain
        </Button>
        }
        <div style={{margin: '8px', padding: '8px', display: 'flex'}}>
        <div style={{flex: '8'}}>
            <Input placeholder="Type your Question here... " onChange={(e) => {setGetQuestion(e.target.value)}}/>
        </div>
        <div style={{flex: '1'}}>
            <Button onClick={callEvaDb}>Search</Button>
        </div>
        
        </div>
           <div style={{display: 'flex', margin: '8px'}}>
           <div  style={{ flex: '1', padding: '8px'}}>
           <Typography level="h2" fontSize="xl" sx={{ mb: 0.5 }}>
                With EvaDB Context
            </Typography>
           <Textarea minRows={3} />
           </div>
           <div  style={{ flex: '1', padding: '8px'}}>
           <Typography level="h2" fontSize="xl" sx={{ mb: 0.5 }}>
                Without EvaDB Context
            </Typography>
           <Textarea minRows={3} />
           </div>
           </div>
           
        </>
  );
}

export default HomePage;
