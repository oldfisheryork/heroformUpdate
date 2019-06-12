import React, { Component } from 'react';
import '../styles.css';
import moment from 'moment';

class DisplayTable extends Component {
  state = {
    heroClient: [],
    workPlan: [],
    weeks: 0,
    startDate: null,
    endDate: null,
    // should be a list, either this file get or from API
    weekdayCalendar: [],
    scaleFactor: 1,
    currentWeek: 0
  };

  // no viriable
  // why we have this function ?
  componentDidMount = () => {
    const data = this.props.location.state;

    if (data && data.weekdayCalendar) {
        this.setState({ weekdayCalendar: data.weekdayCalendar });
    }

    if (data && data.startDate) {
        this.setState({ startDate: moment(data.startDate).format("MMM DD, YYYY")});
    }
    if (data && data.endDate) {
        this.setState({ endDate: moment(data.endDate).format("MMM DD, YYYY") });
    }

    if (data && data.scaleFactor) {
        this.setState({scaleFactor: data.scaleFactor});
    }

    if (data && data.clientRelation) {
      this.setState({ heroClient: data.clientRelation });
    }

    if (data && data.workPlan) {
      this.setState({ workPlan: data.workPlan });
      // do the data processing
      if (data.workPlan[0]) {
        let len = data.workPlan[0].length - 1;
        // weeks definition
        let weeks = Math.ceil(len / 5);
        this.setState({ weeks });
      }
    }
  };


  getPlanForWeek = workPlanForMan => {
    // how to post the name to the page
    // workPlanForMan是某个hero的list，只不过去掉了名字
    workPlanForMan = workPlanForMan.slice(1); // get rid of name

    console.log(workPlanForMan);

    const start = this.state.currentWeek * 5;
    const end = start + 5;
    // 取到相应部分，当前list指定起始位置
    const row = workPlanForMan.slice(start, end);
    // 只返回这五个结果
    return row;
  };

  renderWorkPlan = () => {
    return this.state.workPlan.map((plan, index) => {
      // 这里index是list的id吗
      // plan指的是某个hero的list, contained name
      // planForWeek是这周工作安排, no name contained
      const planForWeek = this.getPlanForWeek(plan);

      return (
        <tr key = {index} >
          <th class="bg-light" scope="row">{index+1}</th>
          <th class="bg-light" nowrap="nowrap">{plan[0]}</th>

          {planForWeek.map((item, index) => (
            <td key={index}>
                {JSON.stringify(item)}
            </td>
          ))}
        </tr>
      );
    });
  };


  // no variable
  renderHeroClient = () => {
    // listElement is every hero-client list it
    return this.state.heroClient.map((listElement, index) => {
      // get rid of name
      const relationContent = listElement.slice(1);
      return (
        <tr key = {index} >
          <th class="bg-light" scope="row">{index+1}</th>
          <th className="bg-light" nowrap="nowrap">{listElement[0]}</th>

          {relationContent.map((ele, i) => {
            return <td key={i}>{ele}</td>;
          })}
        </tr>
      );
    });
  };


  render() {
    // 这儿写const 什么之类，取数组元素
    const weekdayList= this.state.weekdayCalendar;

    return (
      <>
        <div className="container">
            <br></br>

          <div>
            <h3>Work Plan</h3>

          </div>


          {/*<div>*/}
              {/*<div className="col-md-4">*/}
                {/*<h3>Work Plan</h3>*/}
              {/*<div>*/}
              {/*<div className="col-md-4">*/}
                {/*<p>Start Date : {this.state.startDate} </p>*/}
              {/*</div>*/}
              {/*<div className="col-md-4">*/}
                {/*<p>End Date : {this.state.endDate}</p>*/}
              {/*</div>*/}
              {/*<div className="col-md-4">*/}
                {/*<p>Scale Factor : {this.state.scaleFactor}</p>*/}
              {/*</div>*/}
          {/*</div>*/}

          <table class="table">
            <thead class="thead-light">
               <tr>
                <th scope="col">#</th>
                <th scope="col">Hero Name</th>
                <th scope="col">{weekdayList[this.state.currentWeek * 5]}</th>
                <th scope="col">{weekdayList[this.state.currentWeek * 5 + 1]}</th>
                <th scope="col">{weekdayList[this.state.currentWeek * 5 + 2]}</th>
                <th scope="col">{weekdayList[this.state.currentWeek * 5 + 3]}</th>
                <th scope="col">{weekdayList[this.state.currentWeek * 5 + 4]}</th>
              </tr>
            </thead>

            <tbody>{this.renderWorkPlan()}</tbody>
          </table>


          <div>
            <p>Date Range : {this.state.startDate}  -  {this.state.endDate} </p>
            <p>Scale Factor : {this.state.scaleFactor}</p>
            <p>Total Weeks : {this.state.weeks}</p>
            <p>Current Week : {this.state.currentWeek + 1}</p>
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
          <h3>Hero-Client Relation</h3>

          <table className="table">
              <thead className="thead-light">
                  <tr>
                      <th width="5%">#</th>
                      <th width="15%">Hero Name</th>
                      <th colspan="42">Client ID</th>
                  </tr>
              </thead>
              <tbody>{this.renderHeroClient()}</tbody>
          </table>
        </div>


      </>
    );
  }
}

export default DisplayTable;
