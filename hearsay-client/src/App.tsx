import React, { useState } from 'react';
import './App.css';
import axios from 'axios';


const App: React.FC = () => {

  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const onMicClick = () => {
    // call backend - speech_manager.py
    let endpoint = "/v1/speech";
    axios.post(endpoint, {
      query: query
    })
    .then(function (response) {
      setResponse(response.data);
    })
    .catch(function (error) {
      console.error(error);
    });
  }

  const onSubmit = () => {
    // call backend - generate response and display on page
    let endpoint = "/v1/text";
    axios.post(endpoint, {
      query: query
    })
    .then(function (response) {
      setResponse(response.data);
    })
    .catch(function (error) {
      console.error(error);
    });
  }

  let responseDiv = <div></div>
  if (response !== '') {
    responseDiv = <div id="responseDiv">
      <p id="response">{response}</p>
    </div>
  }

  return (
    <div className="App">
      <div id="title">
        <h1>HearSay</h1>
        <img id="logo" src="logo.png" alt="" />
      </div>
      <h3>Rumor has it we've got all the answers you need.</h3>
      <div id="search-bar-section">
        <input id="search-bar"
        placeholder="Type a question, or click the microphone and ask one!" 
        value={query} 
        onChange={e => setQuery(e.target.value)}
        onSubmit={onSubmit}/>
        <div id="mic-button" onClick={onMicClick}>
          <img id="mic-img" src="mic.png" alt="" />
        </div>
      </div>
      <button id="submit-button" onClick={onSubmit}>Submit</button>
      {responseDiv}
    </div>
  );

};

export default App;
