import React, { Component } from 'react';
// SkillDB is the dictionary of everyone's name, and their respective skills listed on the Guru List
import SkillDB from './skillDb';
// CategoriesDB is the list of all categories and subcategories in DTR
import CategoriesDB from './categoriesDb';
// SigDB is the list of all students and the SIGs they belong to
import SigDB from './sigs';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ping: '',
      category: '',
      categoryList: [], // For multiple categories
      apiCategories: [],
      categoryFilter: '',
      task: '',
      username: '',
      sigMembers: [],
      displayNodes: [],
      overRequestedPeople: [
        "Leesha",
        "Yongsung",
        "Kapil",
        "Ryan",
      ],
      requestData: {},
    }

    this.handleFilterClick = this.handleFilterClick.bind(this);
    this.handleNameClick = this.handleNameClick.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleTaskSubmit = this.handleTaskSubmit.bind(this);
    this.getRequestedData = this.getRequestedData.bind(this);
    this.updateRequestedData = this.updateRequestedData.bind(this);
    this.updateDisplayNodes = this.updateDisplayNodes.bind(this);
  };

  // Takes in a person's name, and the category they need help with
  // Returns the people who can help from the Douglas API
  callApi = async (name, category) => {
    var response;
    if(category === undefined){
      response = await fetch(`/api/${name}`);
    } else {
      response = await fetch(`/api/${name}/${category}`);
    }
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    return body;
  }

  // Given a task, returns the categories the task is a part of
  getTaskCategories = async (name, task) => {
    var response = [];
    if (name && task) {
      response = await fetch(`/api/getHelpers/${name}/${task}`);
    }
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    return body;
  };

  // Grabs the availability numbers from the server
  getRequestedData = async (testInput) => {
    var response;
    response = await fetch('/api/requestData');
    const body = await response.json();
    if(response.status !== 200) throw Error(body.message);
    return body;
  };

  // Wrapper function around getRequestedData
  updateRequestedData(testInput) {
    var requestData;
    this.getRequestedData()
    .then(res => this.setState({requestData: res}))
    .catch(err => console.log(err))
  };

  // Handles clicking on an additional filter in the Douglas UI
  async handleFilterClick(filterName, category) {
    this.callApi(this.state.username, filterName)
      .then(res => this.setState({ping: res}))
      .catch(err => console.log(err));

    await this.setState({
      categoryFilter: filterName,
      category: category,
      categoryList: (filterName !== '' ? this.state.categoryList.concat([filterName]) : []),
      displayNodes: (filterName !== '' ? this.state.displayNodes : [])
    })
    this.updateDisplayNodes();
    window.scrollTo(0, 0);
  };
  
  // Given a change in categories, update the names displayed to match the set filter
  updateDisplayNodes() {
    if (this.state.category === ''){
      return;
    } else {
      for (var name in SkillDB){
        if(this.state.username === name) {
          continue;
        }
        if (SkillDB[name][this.state.category].includes(this.state.categoryFilter)) {
          this.setState({
            displayNodes: this.state.displayNodes.concat(name)
          })
        }

      }
    }
    
  }

  // Handles the initial splash page where users "log in" by clicking their name
  handleNameClick(name) {
    this.callApi(name, undefined)
      .then(res => this.setState({ping: res}))
      .catch(err => console.log(err));

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

  // Handles change in the task entry box
  handleInputChange(e) {
    this.setState({task: e.target.value});
  }

  // Handles clicking the submit button on the task entry box
  handleTaskSubmit(e) {
    e.preventDefault();
    this.getTaskCategories(this.state.username, this.state.task)
      .then(res => this.setState({
        apiCategories: res
      }))
      .catch(err => console.log(err));
  }

  // When the page finishes loading, request new availability data every 100ms
  componentDidMount() {
    setInterval(this.updateRequestedData, 100);
  }

  render() {
    // If no username set, show the initial splash page
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

    // Once a user logs in, show this UI
    // MAIN DOUGLAS APPLICATION
    return (
      <div className="App">
        <header className="App-header">
          <h1>Hi {this.state.username}, Welcome to Douglas</h1>
          <p>Douglas highlights additional people on the Guru List who can help you on certain tasks</p>
        </header>
        {/* 
          For each category chosen, list it at the top of the UI
        */}
        {
          this.state.categoryList.map(category => 
            <p>{category}</p>
          )
        }
        <div className="resultContainer" >
          <div className="categories">
            {/* 

            TEXT INPUT FORM, COULDN'T GET IT WORKING BEFORE STATUS UPDATE

            <form onSubmit={this.handleTaskSubmit}>
              <label>
              Enter your task:
              <textarea value={this.state.task} onChange={this.handleInputChange} style={{display: "block", width: "100%"}}/>
              </label>
              <input type="submit" value="Submit" />
            </form> */}
          <button onClick={() => this.handleFilterClick('', '')} ><h1>Clear</h1></button>
            {
              Object.keys(CategoriesDB).map( category =>(
                <div>
                  <h1>
                    {category}
                  </h1>
                  {
                    // For each higher leve category (Design, Tech, Research), list the subcategories underneath it (IOS, Android, Python)
                    CategoriesDB[category].map( categoryDetail => (
                      <button onClick={() => this.handleFilterClick(categoryDetail, category)}><p>{categoryDetail}</p></button>
                    ))
                  }
                </div>
              ))
            }
          </div>
          <div className="names">
          {

          }
            {
              this.state.displayNodes.map( personName => (
                <div>
                  {
                    <p key={personName}>{personName}<span> - {this.state.requestData[personName]}</span></p>
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
