import React, { useState } from 'react';
import './App.css';

const App: React.FC = () => {

  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  let responseDiv = <div></div>
  if (response != '') {
    responseDiv = <div id="responseDiv">
      {response}
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
        <input id="search-bar" placeholder="Type a question, or click the microphone and ask one!" value={query} onChange={e => setQuery(e.target.value)}/>
        <div id="mic-button"><img id="mic-img" src="mic.png" alt="" /></div>
      </div>
      {responseDiv}
    </div>
  );

};

export default App;
