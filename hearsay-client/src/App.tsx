import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const endpoint: string = "http://127.0.0.1:5000";
const textRoute: string = "/v1/text"

interface ChatMessage {
  side: 'left' | 'right';
  text: string;
}

const App: React.FC = () => {
  const [query, setQuery] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [awaitingResponse, setAwaitingResponse] = useState(false);

  function addMessage(side: 'left' | 'right', text: string) {
    const message: ChatMessage = { side, text };
    setMessages(arr => [...arr, message]);
    return message;
  }

  const addUserMessage = useCallback((text: string) => addMessage('right', text), []);
  const addBotMessage = useCallback((text: string) => addMessage('left', text), []);

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    console.warn('Browser does not support speech recognition');
  }

  const sendQuery = useCallback((query: string) => {
    // call backend - generate response and display on page
    addUserMessage(query);
    let url = `${endpoint}${textRoute}`;
    setAwaitingResponse(true);
    axios.post(url, { "query": query })
      .then((response) => {
        setAwaitingResponse(false);
        addBotMessage(response.data["response"]);
      })
      .catch(console.error);
    setQuery('');
  }, [addBotMessage, addUserMessage]);

  const onSubmit = () => {
    sendQuery(query);
  };

  // handle transition from listening to not listening
  const [transitionHandled, setTransitionHandled] = useState(true);

  const onMicClick = () => {
    resetTranscript();
    SpeechRecognition.startListening();
    setTimeout(() => setTransitionHandled(false), 400);
  };

  useEffect(() => {
    if (!listening && !transitionHandled) {
      setTransitionHandled(true);
      sendQuery(transcript);
      resetTranscript();
    }
  }, [listening, transitionHandled, sendQuery, transcript, resetTranscript]);

  function ChatBubble(props: ChatMessage) {
    const green = 'rgb(81, 156, 106)';
    const blue = 'rgb(60, 153, 165)';
    return (
      <div
        className="chat-bubble-container"
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: props.side === 'left' ? 'start' : 'end'
        }}
      >
        <div className="chat-bubble" style={{ backgroundColor: props.side === 'left' ? blue : green }}>
          {
            (props.text == null || props.text === '')
              ? (
                <div style={{ margin: '0 16px' }}>
                  <div className="dot-typing" style={{ margin: '0 auto', bottom: '-7px' }} />
                </div>
              )
              : props.text
          }
        </div>
      </div>
    );
  }

  return (
    <div className="App" style={{ marginTop: messages.length < 1 ? '10%' : '2%' }}>
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
        {messages.map((message, idx) =>
        (
          <ChatBubble side={message.side} text={message.text} key={idx} />
        ))}
        {
          awaitingResponse &&
          <ChatBubble side="left" text="" />
        }
        {
          transcript !== '' &&
          <ChatBubble side="right" text={transcript} />
        }
      </div>
      {listening && <div style={{ marginBottom: 24 }}>You are speaking...</div>}
      {/* search bar */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'end', alignItems: 'center', }}>
          <input
            id="search-bar"
            placeholder="Type a question, or click the microphone and ask one!"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onSubmit={onSubmit}
            onKeyPress={(e) => e.key === 'Enter' ? onSubmit() : null}
          />
          <div id="mic-button" onClick={onMicClick}>
            <img id="mic-img" src="mic.png" alt="" />
          </div>
        </div>
        <button id="submit-button" onClick={onSubmit}>Submit</button>
      </div>
    </div>
  );
};

export default App;
