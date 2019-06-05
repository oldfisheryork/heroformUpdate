import React, { Component } from 'react';

class DisplayTable extends Component {
  state = {
    heroClient: [],
    workPlan: [],
    weeks: 0,
    currentWeek: 0
  };

  componentDidMount = () => {
    const data = this.props.location.state;
    if (data && data.clientRelation) {
      this.setState({ heroClient: data.clientRelation });
    }

    if (data && data.workPlan) {
      this.setState({ workPlan: data.workPlan });
      if (data.workPlan[0]) {
        let len = data.workPlan[0].length - 1;
        let weeks = Math.ceil(len / 5);
        this.setState({ weeks });
      }
    }
  };

  renderHeroClient = () => {
    let x = this.state.heroClient.map((listElement, index) => {
      return (
        <tr key={index}>
          <th scope="row">{index + 1}</th>
          {listElement.map((ele, i) => {
            return <td key={i}>{ele}</td>;
          })}
        </tr>
      );
    });
    return x;
  };

  getPlanForWeek = workPlanForMan => {
    // how to post the name to the page
    workPlanForMan = workPlanForMan.slice(1); // get rid of name
    console.log(workPlanForMan);
    const start = this.state.currentWeek * 5;
    const end = start + 5;
    const row = workPlanForMan.slice(start, end);
    return row;
  };

  renderWorkPlan = () => {
    return this.state.workPlan.map((plan, index) => {

      const planForWeek = this.getPlanForWeek(plan);
      return (
        <tr key={index}>
          <th scope="row">{index + 1}</th>
          <td>{plan[0]}</td>
          {planForWeek.map((item, index) => (
            <td key={index}>{JSON.stringify(item)}</td>
          ))}
        </tr>
      );
    });
  };

  render() {
    return (
      <>
        <div className="container">
          <h3>Work Plan</h3>
          <table className="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Mon</th>
                <th scope="col">Tue</th>
                <th scope="col">Wed</th>
                <th scope="col">Thu</th>
                <th scope="col">Fri</th>
              </tr>
            </thead>
            <tbody>{this.renderWorkPlan()}</tbody>
          </table>

          <div>
            <p>Total weeks: {this.state.weeks}</p>
            <p>Current week: {this.state.currentWeek + 1}</p>
          </div>

          <div>

            <button
              type="button"
              // class="btn btn-dark"
              className="btn btn-info"
              style={{ marginRight: '20px' }}
              onClick={() => {
                const currentWeek = this.state.currentWeek;
                if (currentWeek > 0) {
                  this.setState({ currentWeek: currentWeek - 1 });
                }
              }}
            >
              Prev Week
            </button>

            <button
              type="button"
              className="btn btn-info"
              style={{ marginRight: '10px' }}
              onClick = {() => {
                const currentWeek = this.state.currentWeek;
                if (currentWeek + 1 < this.state.weeks) {
                  this.setState({ currentWeek: currentWeek + 1 });
                }
              }}
            >
              Next Week
            </button>

          </div>
        </div>
          <br></br>

        <div className="container">
          <h3>Client Relation:</h3>
          <table className="table">
            <tbody>{this.renderHeroClient()}</tbody>
          </table>
        </div>
      </>
    );
  }
}

export default DisplayTable;
