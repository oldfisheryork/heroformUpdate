import React, { Component } from 'react';

class DisplayTable extends Component {
  state = {
    heroClient: [],
    workplan: [],
    weeks: 0,
    currentWeek: 0
  };

  componentDidMount = () => {
    const data = this.props.location.state;
    if (data && data.clientRelation) {
      this.setState({ heroClient: data.clientRelation });
    }

    if (data && data.workplan) {
      this.setState({ workplan: data.workplan });
      if (data.workplan[0]) {
        let len = data.workplan[0].length - 1;
        let weeks = len / 5;
        this.setState({ weeks });
      }
    }
  };

  rednerHeroClient = () => {
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
    workPlanForMan = workPlanForMan.slice(1); // get rid of name
    console.log(workPlanForMan);
    const start = this.state.currentWeek * 5;
    const end = start + 5;
    const row = workPlanForMan.slice(start, end);
    return row;
  };

  renderWorkPlan = () => {
    return this.state.workplan.map((plan, index) => {
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
              className="btn btn-info"
              style={{ marginRight: '10px' }}
              onClick={() => {
                const currentWeek = this.state.currentWeek;
                if (currentWeek + 1 < this.state.weeks) {
                  this.setState({ currentWeek: currentWeek + 1 });
                }
              }}
            >
              Next Week
            </button>
            <button
              type="button"
              class="btn btn-dark"
              onClick={() => {
                const currentWeek = this.state.currentWeek;
                if (currentWeek > 0) {
                  this.setState({ currentWeek: currentWeek - 1 });
                }
              }}
            >
              Prev Week
            </button>
          </div>
        </div>

        <div className="container">
          <h3>Client Relation:</h3>
          <table className="table">
            <tbody>{this.rednerHeroClient()}</tbody>
          </table>
        </div>
      </>
    );
  }
}

export default DisplayTable;
