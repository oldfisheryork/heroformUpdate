import React, { Component } from 'react';

class DisplayTable extends Component {
  state = {
    heroClient: [],
    workPlan: [],
    weeks: 0,
    scaleFactor: 1,
    currentWeek: 0
  };

  // no viriable
  // why we have this function ?
  componentDidMount = () => {
    const data = this.props.location.state;
    if (data && data.scaleFactor) {
        this.setState({ scaleFactor: data.scaleFactor });
    }

    if (data && data.clientRelation) {
      this.setState({ heroClient: data.clientRelation });
    }

    if (data && data.workPlan) {
      this.setState({ workPlan: data.workPlan });
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
      // plan指的是某个hero的list
      // planForWeek是这周工作安排
      const planForWeek = this.getPlanForWeek(plan);

      return (
        <tr key = {index} >
          <th scope="row">{index}</th>
            {/*plan[0]就是某个hero名字*/}
          <td>{plan[0]}</td>

          {/*对planForWeek这五个值, index类似循环里的编号，item具体planForWeek每个元素*/}
          {planForWeek.map((item, index) => (
            <td key={index}>{JSON.stringify(item)}</td>
          ))}
        </tr>
      );
    });
  };


  // no variable
  renderHeroClient = () => {
    //  what does map mean ?
    let x = this.state.heroClient.map((listElement, index) => {
      //  here why tr ? , index is what ?
      return (
        <tr key={index}>
          <th scope="row">{index}</th>
          {listElement.map((ele, i) => {
            return <td key={i}>{ele}</td>;
          })}
        </tr>
      );
    });
    return x;
  };


  render() {
    // 这儿写const 什么之类，取数组元素

    return (
      <>
        <div className="container">
            <br></br>
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

              {/*should I write it here ? */}
              {/*<tr>*/}
                {/*<th scope="col"></th>*/}
                {/*<th scope="col"></th>*/}
                {/*<th scope="col">Mon</th>*/}
                {/*<th scope="col">Tue</th>*/}
                {/*<th scope="col">Wed</th>*/}
                {/*<th scope="col">Thu</th>*/}
                {/*<th scope="col">Fri</th>*/}
              {/*</tr>*/}

            </thead>
            <tbody>{this.renderWorkPlan()}</tbody>
          </table>


          <div>
            <p>Total weeks: {this.state.weeks}</p>
              <p>Scale Factor: {this.state.scaleFactor}</p>
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
