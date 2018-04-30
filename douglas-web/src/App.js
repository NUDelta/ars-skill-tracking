import React, { Component } from 'react';
import logo from './logo.svg';
import Design from './design'
import './App.css';

console.log(Design);

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        {
          Object.keys(Design).map( user_key => (
            <div>
              <h3>{user_key}</h3>
              <div>
              <ul>
                {
                  Object.keys(Design[user_key]).map( skill_key => (
                    <div>
                    { 
                      Design[user_key][skill_key] == true &&
                      <div>
                        <p>{skill_key}</p>
                      </div>
                    }
                  </div>
                  ))
                }
              </ul>
              </div>
            </div>
          ))
        }
      </div>
    );
  }
}

export default App;
