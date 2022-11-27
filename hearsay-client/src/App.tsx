import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import * as $ from "jquery";

const endpoint : string = "http://127.0.0.1:5000";
const speechRoute : string = "/v1/speech"
const textRoute : string = "/v1/text"

const App: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [queryList, setQueryList] = useState<string[]>([]);
  const [responseList, setResponseList] = useState<string[]>([]);

  function sendQuery(query: string, speech_enabled: boolean) {
    // call backend - generate response and display on page
    setQueryList(queryList => [...queryList, query]);
    let url = `${endpoint}${textRoute}`;
    axios.post(url, {
      "query": query,
      "speech": speech_enabled
    })
    .then((response) => {
      setQuery('');
      setResponseList(responseList => [...responseList, response.data["response"]]);
    })
    .catch(console.error);
  }
  
  const onSubmit = () => {
    sendQuery(query, false);
  };

  const onMicClick = () => {
    // call backend - speech_manager.py
    $("#mic-message").show().delay(5000).fadeOut();
    let url = `${endpoint}${speechRoute}`;
    axios.get(url)
      .then(function (response) {
        sendQuery(response.data["query"], true);
      })
      .catch(function (error) {
        console.error(error);
      });
  };

  let conversation : JSX.Element[] = [];

  interface ChatBubbleProps {
    side: 'left' | 'right';
    subtitle: string;
    text: string;
    marginTop: number;
  }
  function ChatBubble(props: ChatBubbleProps) {
    const green = 'rgb(81, 156, 106)';
    const blue = 'rgb(60, 153, 165)';
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: props.side === 'left' ? 'start' : 'end',
        marginTop: props.marginTop
      }}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: props.side === 'left' ? 'start' : 'end'
        }}>
          <div className="chat-bubble" style={{ backgroundColor: props.side === 'left' ? blue : green }}>
            {
              (props.text == null || props.text === '')
              ? <div className="dot-typing" style={{ margin: '0 auto', bottom: '-7px'  }}>&nbsp;</div>
              : props.text
            }
          </div>
        </div>
      </div>
    );
  }
  for (let i = 0; i < queryList.length; i++) {
    conversation.push(<ChatBubble side="right" subtitle="User" text={queryList[i]} marginTop={i === 0 ? 0 : 16} key={i*2} />);
    conversation.push(<ChatBubble side="left" subtitle="HearSay" text={responseList[i] ?? ''} marginTop={16} key={i*2 + 1} />);
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
      {/* search bar */}
      <div>
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
        <div id="mic-message" style={{display: 'none', marginTop: '25px', fontSize: '16px'}}>Wait 1 second before speaking!</div>
        <button id="submit-button" onClick={onSubmit}>Submit</button>
      </div>
    </div>
  );

};

export default App;
