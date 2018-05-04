import React, { Component } from 'react';
import SkillDB from './skillDb';
import CategoriesDB from './categoriesDb';
import SigDB from './sigs';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      category: '',
      categoryFilter: '',
      username: '',
      sigMembers: [],
      overRequestedPeople: [
        "Leesha",
        "Yongsung",
        "Kapil",
        "Ryan",
      ]
    }

    this.handleFilterClick = this.handleFilterClick.bind(this);
    this.handleNameClick = this.handleNameClick.bind(this);
  };

  handleFilterClick(filterName, category) {
    this.setState({
      categoryFilter: filterName,
      category: category,
    })
  };

  handleNameClick(name) {
    var sigMembers = [];
    Object.keys(SigDB["groups"]).map(sigName => {
      if (SigDB["groups"][sigName].includes(name)){
        sigMembers = sigMembers.concat(SigDB["groups"][sigName]);
      }
    });

    this.setState({
      username: name,
      sigMembers,
    });
  }
  
  


  render() {
    if(this.state.username === '') {
      return (
        <div>
        <h1>What's your name?</h1>
        {
          Object.keys(SkillDB).map( personName => (
            <button style={{margin: '20px'}} onClick={() => this.handleNameClick(personName)}><h1>{personName}</h1></button>
          ))
        }
        </div>
      )
    }
    return (
      <div className="App">
        <header className="App-header">
          <h1>Hi {this.state.username}, Welcome to Douglas</h1>
          <p>✨ indicates people outside your SIG, and could offer a new perspective on your work!</p>
          <p>😫 indicates people who are normally overrequested for help in DTR, and might have limited availablilty this week!</p>
        </header>
        <h1>{this.state.categoryFilter}</h1>
        <div style={{display:'grid', gridTemplateColumns:'1fr 2fr', gridTemplateAreas: "categories names", minWidth:'100%', backgroundColor:'lightGrey'}} >
          <div className="categories" style={{backgroundColor: 'grey'}}>
          <button onClick={() => this.handleFilterClick('', '')} ><h1>Clear</h1></button>
            {
              Object.keys(CategoriesDB).map( category =>(
                <div>
                  <h1>
                    {category}
                  </h1>
                  {
                    CategoriesDB[category].map( categoryDetail => (
                      <button onClick={() => this.handleFilterClick(categoryDetail, category)}><p>{categoryDetail}</p></button>
                    ))
                  }
                </div>
              ))
            }
          </div>
          <div className="names" style={{}}>
            {
              Object.keys(SkillDB).map( personName => (
                <div>
                  { 
                    this.state.category === '' ? // If no filter, show everyone
                    <h3 key={personName}> {personName} </h3> : 
                    (SkillDB[personName][this.state.category].includes(this.state.categoryFilter) && // If the category has the person
                    (this.state.overRequestedPeople.includes(personName) ? // If person is overrequested
                    <h3 key={personName} ><span role="img">😫</span> {personName} <span role="img">😫</span></h3> :
                    (this.state.sigMembers.includes(personName) ? // If the person is in the same sig
                    <h3 key={personName} >{personName}</h3> :
                    <h3 key={personName} ><span role="img">✨</span> {personName} <span role="img">✨</span></h3>)))
                  }
                </div>
              ))
            }
          </div>
        </div>
      </div>
    );
  }
};

export default App;
