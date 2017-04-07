

var ParkingTableRow = React.createClass({
  render: function() {
    return (
      <tr>


        <td><a href='' onClick={this.onClick}>{this.props.parking} </a></td>

      </tr>
    );
  },
  onClick: function(e) {
    e.preventDefault();
    this.props.handleEditClickPanel(this.props.contact.id);
  }
});

var ParkingsTable = React.createClass({
  render: function() {
    var rows = [];
    if(this.props.parkings.length > 0){
    this.props.parkings.forEach(function(parking) {
      rows.push(<ParkingTableRow key={parking.id} parking={parking} handleEditClickPanel={this.props.handleEditClickPanel}  />);
    }.bind(this));
    }
    return (
      <table>
        <tbody>{rows}</tbody>
      </table>
    );
  }
});

var FindParkings = React.createClass({
  render: function() {
    return(

      <form onSubmit={this.props.handleSubmitClick}>
     {this.props.message?<div className="info"><span className="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>{this.props.message}</div>:null}
       <label forHtml='latitude'>Latitude</label><input placeholder="121"  required={true} ref='latitude' name='latitude' type='text'  onChange={this.onChange}/>
        <label forHtml='longitude'>Radius</label><input ref='longitude' required={true} placeholder="178" name='longitude' type='text'  onChange={this.onChange}/>
        <label forHtml='radius'>Radius in miles</label> <input ref='radius' placeholder="10" name='radius' type='text' onChange={this.onChange}/>

        <br />
        <input type='submit' value="Find" />


      </form>

    );
  },
  onChange: function() {
    var latitude = ReactDOM.findDOMNode(this.refs.latitude).value;
    var longitude = ReactDOM.findDOMNode(this.refs.longitude).value;
    var radius = ReactDOM.findDOMNode(this.refs.radius).value;
    this.props.handleChange(latitude, longitude, radius);
  }
});

var ParkingPanel = React.createClass({
  getInitialState: function() {

    return {
     parkings : [],
     url: window.location.href,
      search:"",
      message:""
    };
  },
  render: function() {
    return(
      <div className="row">

        <div className="one-half column">

          <ParkingsTable parkings={this.state.parkings} handleEditClickPanel={this.handleEditClickPanel} />
        </div>
        <div className="divider mobile-hide"></div>
        <div className="one-half column">
        <h3>Search For a Parking Space Near You!</h3>

          <FindParkings
            parking={this.state.editingParking}
            message={this.state.message}
            handleChange={this.handleChange}
            handleSubmitClick={this.handleSubmitClick}
            handleCancelClick={this.handleCancelClick}
            handleDeleteClick={this.handleDeleteClick}
            validateDate={this.validateDate}
            validatePhone={this.validatePhone}
          />
        </div>
      </div>
    );
  },
  componentDidMount: function() {
    this.reloadContacts('');
  },

  onSearchChanged: function(query) {
  if (this.promise) {
    clearInterval(this.promise)
  }
  this.setState({
    search: query
  });
  this.promise = setTimeout(function () {
    this.reloadContacts(query);
  }.bind(this), 200);
},
onClearSearch: function() {
  this.setState({
    search: ''
  });
  this.reloadContacts('');
},
handleSelectGroupPanel: function(id){
//var contact_group = $.extend({}, this.state.contacts.filter(function(x) {
//    return x.id == id;
//  })[0] );
  this.reloadContacts(id);

},
handleEditClickPanel: function(id) {
  var parking = $.extend({}, this.state.parkings.filter(function(x) {
    return x.id == id;
  })[0] );

  this.setState({
    editingParking: parking,
    message: ''
  });
},
handleChange: function(latitude, longitude, radius) {

    this.setState({
        editingParking: {

            latitude: latitude,
            longitude:longitude,
            radius: radius,

        }
    });
},

reloadContacts: function(query) {
    $.ajax({
      url: this.state.url+'search/'+query,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({
          contacts: data["data"],
          contacts_groups: [],
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.state.url, status, err.toString());
        this.setState({
          message: "",
          search: query
        });
      }.bind(this)
    });

  },
  handleSubmitClick: function(e) {
   e.preventDefault();

      $.ajax({
        url: this.state.url+'api/parkings',
        dataType: 'json',
        method: 'POST',
        data: this.state.editingParking,
        cache: false,
        success: function(data) {
          this.setState({
            message: data["message"]
          });
          this.reloadContacts('');
        }.bind(this),
        error: function(xhr, status, err) {
          console.error(this.state.url, status, err.toString());
          this.setState({
            message: err.toString()
          });
        }.bind(this)
      });

    this.setState({
      editingParking: {}
    });
  },


});



ReactDOM.render(

  <ParkingPanel />,
  document.getElementById('content')
);