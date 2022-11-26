import React, { useState } from 'react';
import './App.css';
import axios from 'axios';


const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [queryList, setQueryList] = useState([""]);
  const [responseList, setResponseList] = useState([""]);

  const onMicClick = () => {
    // call backend - speech_manager.py
    /*
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
    */
  }

  const onSubmit = () => {
    // call backend - generate response and display on page
    setQueryList(queryList => [...queryList, query]);
    let endpoint = "http://localhost:5000/v1/text";
    axios.post(endpoint, {
      query: query
    })
      .then(function (response) {
        setQuery('');
        setResponseList(responseList => [...responseList, response.data]);
      })
      .catch(function (error) {
        console.error(error);
      });
  }


  let conversation : JSX.Element[] = [];

  let searchBar = <div></div>
  if (queryList.length === 0) {
    searchBar = 
    <div>
        <div style={{ display: 'flex', justifyContent: 'end', alignItems: 'center' }}>
        <input
          id="search-bar"
          placeholder="Type a question, or click the microphone and ask one!"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onSubmit={onSubmit}
        />
        <div id="mic-button" onClick={onMicClick}>
          <img id="mic-img" src="mic.png" alt="" />
        </div>
      </div>
      <button id="submit-button" onClick={onSubmit}>Submit</button>
    </div>;
  }
  else {
    for (let i = 0; i < queryList.length; i++) {
      conversation.push(<div><div id="query">{queryList[i]}</div><p id="query-name">User</p></div>);
      conversation.push(<div><div id="response">{responseList[i]}</div><p id="response-name">HearSay</p></div>);
    }
    searchBar = 
    <div style={{marginBottom: '100px'}}>
      <div style={{display: 'flex', justifyContent: 'end', alignItems: 'center', }}>
      <input
        id="search-bar"
        placeholder="Type a question, or click the microphone and ask one!"
        value={query}
        onChange={e => setQuery(e.target.value)}
        onSubmit={onSubmit}
      />
      <div id="mic-button" onClick={onMicClick}>
        <img id="mic-img" src="mic.png" alt="" />
      </div>
      </div>
      <button id="submit-button" onClick={onSubmit}>Submit</button>
    </div>;
  }

  return (
    <div className="App">
      <div style={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: 72 }}>
          HearSay
        </h1>
        <img src="logo.png" alt="" style={{
          margin: 0,
          height: 100,
          width: 75
        }} />
      </div>
      <h3 style={{ fontSize: 16, marginBottom: 25 }}>
        Rumor has it we've got all the answers you need.
      </h3>
      <div id="conversation">
        {conversation}
      </div>
      {searchBar}
    </div>
  );

};

export default App;
