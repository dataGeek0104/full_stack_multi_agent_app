import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hey👋! This is the frontend for 🤖<strong>Multi Agentic</strong> Application.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn <strong>React</strong>
        </a>
        <a
          className="App-link"
          href="https://www.langchain.com/"
          target="_blank"
          rel="noopener noreferrer"
          style={{ marginTop: '1rem' }}
        >
          Learn <strong>Langchain</strong> and <strong>Langgraph</strong>
        </a>
      </header>
    </div>
  );
}

export default App;
