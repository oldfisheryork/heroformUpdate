import * as React from 'react';
import axios from 'axios';
import { config } from '../config';

import { DateRangePicker } from 'react-dates';
import 'react-dates/initialize';
import 'react-dates/lib/css/_datepicker.css';
import '../styles.css';
import moment from 'moment';

class InputForm extends React.Component {
  state = {
    clientTask: null,
    heroNum: null,
    weekdayHours: null,

    startDate: moment(),
    endDate: moment().subtract(-1, "year"),

    focusedInput: null,

    startDateYear: null,
    startDateMonth: null,
    startDateDay: null,

    endDateYear: null,
    endDateMonth: null,
    endDateDay: null
  };

  // it works good but I prefer construcutor
  // componentWillMount () {
  //
  //   if (this.state.startDate) {
  //     var d = new Date(this.state.startDate);
  //     this.setState({startDateMonth: d.getMonth() + 1});
  //     this.setState({startDateYear: d.getFullYear()});
  //     this.setState({startDateDay: d.getDate()});
  //   };
  //
  //   if (this.state.endDate) {
  //     var dd = new Date(this.state.endDate);
  //     this.setState({
  //       endDateMonth: dd.getMonth() + 1,
  //       endDateYear: dd.getFullYear(),
  //       endDateDay: dd.getDate()
  //     });
  //   };
  // };


  //  it works to initialize the state
  //  in constructor, better use this.state rather than this.setState()
  // what's the difference if I use props as variable
  constructor () {
    super();
    var d = new Date(this.state.startDate);
    var dd = new Date(this.state.endDate);

    this.state = {
        startDate: this.state.startDate,
        endDate: this.state.endDate,
        startDateMonth: d.getMonth() + 1,
        startDateYear: d.getFullYear(),
        startDateDay: d.getDate(),
        endDateMonth: dd.getMonth() + 1,
        endDateYear: dd.getFullYear(),
        endDateDay: dd.getDate()
    };
  };


  handleFocusChange = focusedInput => this.setState({ focusedInput });

  // handleDateChange = ({ startDate, endDate }) =>
  //   this.setState({ startDate, endDate });

  isOutsideRange = () => false;

  handleDateChange = ({ startDate, endDate }) => {
    if (startDate) {
      var d = new Date(startDate);
      this.setState({startDate: startDate});
      this.setState({startDateMonth: d.getMonth() + 1});
      this.setState({startDateYear: d.getFullYear()});
      this.setState({startDateDay: d.getDate()});
    };

    if (endDate) {
      var dd = new Date(endDate);
      this.setState({
        endDate : endDate,
        endDateMonth: dd.getMonth() + 1,
        endDateYear: dd.getFullYear(),
        endDateDay: dd.getDate()
      });
    };
  };

  // 每次点击Go按钮就submit，调submitForm
  // 重点是submit传到后台吗?
  submitForm = () => {
    if (
      !!this.state.clientTask &&
      !!this.state.heroNum &&
      !!this.state.weekdayHours &&
      !!this.state.startDate &&
      !!this.state.endDate
    ) {
      //  这里最重要，应该就是传到后台，post到指定API，设置status
      axios.post(`${config.serverUrl}/heroform`, { ...this.state }).then(({ status, data }) => {
        if (status >= 200 && status < 400) {
          //  到props, history
          this.props.history.push('display', data);
        } else {
          alert('Error: ' + status);
        }
      });
    } else {
      alert('Input invalid');
    }
  };

  // 后面每次输入都调OnInput Change
  onInputChange = e => {
    if (e.target && e.target.id) {
      switch (e.target.id) {
        case 'clientTask': {
          try {
            const trylist = JSON.parse(e.target.value);

            if (Array.isArray(trylist)) {
              this.setState({ clientTask: trylist });
            }
          } catch (e) {
            this.setState({ clientTask: null });
          }

          break;
        }

        case 'heroNum':
          this.setState({ heroNum: e.target.value });
          break;

        case 'weekdayHours':
          this.setState({ weekdayHours: e.target.value });
          break;

        default:
      }
    }
  };


  render() {

    return (
      <>
        <div className="container">
          {/*在同一行*/}
          <div className="row">
            {/*在同一列*/}
            <div className="col-md-8">
              {/*输入的都遵循form 要求？*/}
              <form>
                <br />

                <div>
                  <label htmlFor="clientTask">Client Task</label>
                  <input
                    type="text"
                    className="form-control"
                    id="clientTask"
                    placeholder="Client Task List"
                    onInput={this.onInputChange}
                  />
                </div>

                <div>
                  <label htmlFor="heroNum">Hero number</label>
                  <input
                    type="text"
                    className="form-control"
                    id="heroNum"
                    placeholder="Input hero number"
                    onInput={this.onInputChange}
                  />
                </div>

                <div>
                  <label htmlFor="weekdayHours">Weekday hours</label>
                  <input
                    type="text"
                    className="form-control"
                    id="weekdayHours"
                    placeholder="Every weekday working hours"
                    onInput={this.onInputChange}
                  />
                </div>

                <div>
                  <label htmlFor="dateRangeSelector">Date Range</label>
                  <br />

                  <DateRangePicker
                    displayFormat="MMM DD YYYY"
                    startDateId="startDate"
                    endDateId="endDate"

                    startDate={this.state.startDate}
                    endDate={this.state.endDate}


                    onDatesChange={this.handleDateChange}
                    focusedInput={this.state.focusedInput}
                    onFocusChange={this.handleFocusChange}
                    isOutsideRange={this.isOutsideRange}
                  />
                </div>

              </form>
            </div>

            {/*Go这个button点击就将参数传到后台调API*/}
            <div className="col-md-4" style={{ display: 'flex', alignItems: 'flex-end' }}>
              <div style={{ display: 'flex', flex: 1, justifyContent: 'center' }}>
                <button
                  //                  ------very important-------
                  onClick={this.submitForm}
                  type="button"
                  className="btn btn-primary"
                  style={{ paddingLeft: '20px', paddingRight: '20px' }}
                >
                  Go!
                </button>
              </div>
            </div>
          </div>
        </div>

        {/*why have stringify ?*/}

        {/*<div>State: {JSON.stringify(this.state)}</div>*/}
        {/*<div>{JSON.stringify(!!this.state.clientTask)}</div>*/}
        {/*<div>{JSON.stringify(!!this.state.heroNum)}</div>*/}
        {/*<div>{JSON.stringify(!!this.state.weekdayHours)}</div>*/}

        {/*<div>{JSON.stringify(!!this.state.startDate)}</div>*/}
        {/*<div>{JSON.stringify(!!this.state.endDate)}</div>*/}
        {/*<div>{JSON.stringify(this.state.startDateDay)}</div>*/}

      </>
    );
  }
}

export default InputForm;